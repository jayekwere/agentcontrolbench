"""Documented command line entry points."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .adapters import HTTPModel, ProviderConfig
from .core import Experiment, write_json
from .dataset import load_dataset
from .engine import evaluate


def main() -> None:
    parser = argparse.ArgumentParser(description="AgentControlBench: synthetic AI safety experiments")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="execute a bounded experiment")
    run.add_argument("--config", type=Path)
    run.add_argument(
        "--provider-config", type=Path, help="explicit opt-in provider config; never used by dashboard"
    )
    run.add_argument("--output", type=Path, default=Path("runs/experiment.json"))
    data = sub.add_parser("dataset", help="validate and export the labeled synthetic dataset")
    data.add_argument("--output", type=Path, default=Path("runs/dataset.json"))
    serve = sub.add_parser("serve", help="serve the local dashboard")
    serve.add_argument("--port", type=int, default=8080)
    mcp = sub.add_parser("mcp", help="run isolated MCP stdio laboratory")
    mcp.add_argument("--scenario-id", help="trusted task scope selected from the synthetic dataset")
    args = parser.parse_args()
    try:
        if args.command == "run":
            config = Experiment.model_validate_json(args.config.read_text()) if args.config else Experiment()
            model = (
                HTTPModel(ProviderConfig.model_validate_json(args.provider_config.read_text()))
                if args.provider_config
                else None
            )
            result = evaluate(config, model)
            write_json(args.output, result.model_dump())
            print(
                json.dumps(
                    {
                        "output": str(args.output),
                        "mode": result.mode,
                        "rows": len(result.rows),
                        "summary": result.summary,
                    }
                )
            )
        elif args.command == "dataset":
            cases = load_dataset()
            write_json(args.output, [s.model_dump() for s in cases])
            print(json.dumps({"cases": len(cases), "output": str(args.output)}))
        elif args.command == "serve":
            import uvicorn

            if not 1024 <= args.port <= 65535:
                raise ValueError("port must be between 1024 and 65535")
            uvicorn.run(
                "agentcontrolbench.web:app",
                host="127.0.0.1",
                port=args.port,
                log_level="warning",
                limit_concurrency=32,
                timeout_keep_alive=5,
            )
        else:
            from .mcp import serve_stdio

            serve_stdio(args.scenario_id)
    except (ValueError, OSError) as exc:
        print(
            json.dumps(
                {"error": type(exc).__name__, "detail": "invalid configuration or inaccessible local path"}
            ),
            file=sys.stderr,
        )
        raise SystemExit(2) from None


if __name__ == "__main__":
    main()
