"""In-memory synthetic tool laboratory. No filesystem/cloud/identity integrations."""

from __future__ import annotations

import secrets
import time
from dataclasses import dataclass
from typing import Literal

from .dataset import TOOLS, Call, Observation

Defense = Literal["baseline", "least_privilege", "policy", "capabilities", "depth"]
DEFENSES: tuple[Defense, ...] = ("baseline", "least_privilege", "policy", "capabilities", "depth")


@dataclass
class Capability:
    call: Call
    session: str
    expires: float
    remaining: int


class CapabilityStore:
    def __init__(self) -> None:
        self._tokens: dict[str, Capability] = {}

    def issue(self, call: Call, session: str, ttl: float = 60.0) -> str:
        token = secrets.token_urlsafe(32)
        self._tokens[token] = Capability(call.model_copy(deep=True), session, time.monotonic() + ttl, 2)
        return token

    def consume(self, token: str, call: Call, session: str) -> bool:
        cap = self._tokens.get(token)
        if (
            not cap
            or cap.expires < time.monotonic()
            or cap.remaining <= 0
            or cap.session != session
            or cap.call != call
        ):
            return False
        cap.remaining -= 1
        return True


class Laboratory:
    def __init__(self, observation: Observation, defense: Defense, session: str = "local") -> None:
        if defense not in DEFENSES:
            raise ValueError("unknown defense")
        self.observation = observation
        self.defense = defense
        self.session = session
        self.capabilities = CapabilityStore()
        self.token = self.capabilities.issue(observation.permitted, session)
        self.state: dict[str, str] = {}
        self.executed: list[Call] = []

    def execute(self, call: Call, token: str | None = None) -> dict[str, object]:
        # Names are synthetic IDs, never OS paths. Reject traversal even in the vulnerable baseline.
        if (
            call.tool not in TOOLS.values()
            or ".." in call.resource
            or "\\" in call.resource
            or call.resource.startswith("/")
            or len(call.resource.split("/")) != 3
        ):
            return {"allowed": False, "reason": "invalid synthetic tool or resource"}
        expected = self.observation.permitted
        if self.defense in ("least_privilege", "depth") and call.tool != expected.tool:
            return {"allowed": False, "reason": "tool is outside least-privilege grant"}
        # The policy uses trusted task scope; tool output cannot change it.
        if self.defense in ("policy", "depth") and (
            call.tool != expected.tool
            or call.resource.split("/")[0] != self.observation.tenant
            or "restricted" in call.resource
            or call.value != "approved"
        ):
            return {
                "allowed": False,
                "reason": "trusted policy denied tool, tenant, classification or argument",
            }
        if self.defense in ("capabilities", "depth") and not self.capabilities.consume(
            token or "", call, self.session
        ):
            return {"allowed": False, "reason": "scoped capability denied"}
        self.executed.append(call)
        self.state[call.resource] = f"{call.tool}:{call.value}"
        return {
            "allowed": True,
            "reason": "synthetic operation executed",
            "content": self.observation.content,
            "classification": "synthetic-only",
        }
