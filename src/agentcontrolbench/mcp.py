"""MCP 2025-06-18 stdio subset: initialization, ping, tools/list and tools/call.

Explicit legacy protocol version, no network transport or modern 2026 extension claims.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from .dataset import TOOLS, Call, load_dataset
from .lab import Laboratory


class MCPServer:
    def __init__(self, scenario_id: str | None = None) -> None:
        self.initialized = False
        self.ready = False
        cases = load_dataset()
        selected = next((s for s in cases if s.id == scenario_id), None) if scenario_id else cases[0]
        if selected is None:
            raise ValueError("unknown synthetic scenario scope")
        self.lab = Laboratory(selected.observation, "depth")

    def handle(self, message: dict[str, Any]) -> dict[str, Any] | None:
        request_id = message.get("id")
        method = message.get("method")
        error: dict[str, Any] | None = None
        result: dict[str, Any] = {}
        if message.get("jsonrpc") != "2.0" or not isinstance(method, str):
            error = {"code": -32600, "message": "invalid JSON-RPC request"}
        elif method == "notifications/initialized" and self.initialized:
            self.ready = True
            return None
        elif method == "initialize":
            params = message.get("params", {})
            if params.get("protocolVersion") != "2025-06-18":
                error = {"code": -32602, "message": "only protocol 2025-06-18 is supported"}
            else:
                self.initialized = True
                result = {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": "agentcontrolbench-synthetic-lab", "version": "0.1.1"},
                }
        elif not self.ready:
            error = {"code": -32002, "message": "initialize and initialized notification required"}
        elif method == "ping":
            result = {}
        elif method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": tool,
                        "description": "Synthetic in-memory operation; exact default-deny task scope enforced.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "resource": {"type": "string"},
                                "value": {"type": "string", "default": "approved"},
                            },
                            "required": ["resource"],
                            "additionalProperties": False,
                        },
                    }
                    for tool in TOOLS.values()
                ]
            }
        elif method == "tools/call":
            try:
                params = message["params"]
                args = params["arguments"]
                if not isinstance(args, dict) or set(args) - {"resource", "value"}:
                    raise ValueError("unexpected arguments")
                call = Call.model_validate({"tool": params["name"], **args})
                outcome = self.lab.execute(call, self.lab.token)
                result = {
                    "content": [{"type": "text", "text": json.dumps(outcome)}],
                    "isError": not outcome["allowed"],
                }
            except (ValueError, KeyError, TypeError):
                error = {"code": -32602, "message": "invalid tool arguments"}
        else:
            error = {"code": -32601, "message": "method not supported"}
        if request_id is None:
            return None
        return {"jsonrpc": "2.0", "id": request_id, **({"error": error} if error else {"result": result})}


def serve_stdio(scenario_id: str | None = None) -> None:
    server = MCPServer(scenario_id)
    for _ in range(10000):
        line = sys.stdin.buffer.readline(16385)
        if not line:
            return
        try:
            if len(line) > 16384:
                return
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("object required")
            response = server.handle(value)
        except (ValueError, TypeError, AttributeError):
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}
        if response is not None:
            print(json.dumps(response), flush=True)
