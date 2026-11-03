"""Typed synthetic resource models and domain-specific operations; no host integrations."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from .core import StrictModel
from .dataset import Call


class FileState(StrictModel):
    kind: Literal["file"] = "file"
    resource: str
    content: str
    reads: int = 0


class TicketState(StrictModel):
    kind: Literal["ticket"] = "ticket"
    resource: str
    status: Literal["open", "resolved"] = "open"
    notes: list[str] = Field(default_factory=list)


class CloudState(StrictModel):
    kind: Literal["cloud"] = "cloud"
    resource: str
    state: Literal["running", "stopped"] = "running"
    transitions: int = 0


class IdentityState(StrictModel):
    kind: Literal["identity"] = "identity"
    resource: str
    roles: list[str] = Field(default_factory=list)


class DocumentState(StrictModel):
    kind: Literal["document"] = "document"
    resource: str
    title: str
    body: str
    retrievals: int = 0


class ClassificationState(StrictModel):
    kind: Literal["classification"] = "classification"
    resource: str
    sample: str
    result: Literal["unclassified", "public", "restricted"] = "unclassified"


ResourceState = FileState | TicketState | CloudState | IdentityState | DocumentState | ClassificationState


def create_resource(resource: str) -> ResourceState:
    domain = resource.split("/")[1]
    if domain == "file":
        return FileState(resource=resource, content=f"Synthetic file contents for {resource}.")
    if domain == "ticket":
        return TicketState(resource=resource)
    if domain == "cloud":
        return CloudState(resource=resource)
    if domain == "identity":
        return IdentityState(resource=resource)
    if domain == "document":
        return DocumentState(
            resource=resource,
            title="Synthetic internal document",
            body=f"Authorized research record {resource}.",
        )
    if domain == "classification":
        marker = "SYNTHETIC_RESTRICTED" if "restricted" in resource else "SYNTHETIC_PUBLIC"
        return ClassificationState(resource=resource, sample=f"{marker}: invented benchmark content.")
    raise ValueError("unknown synthetic domain")


def operate(state: ResourceState, call: Call) -> None:
    """Mutate only a typed in-memory resource after the gateway has authorized it."""
    if isinstance(state, FileState):
        state.reads += 1
    elif isinstance(state, TicketState):
        state.status = "resolved"
        state.notes.append(call.value)
    elif isinstance(state, CloudState):
        if state.state == "running":
            state.transitions += 1
        state.state = "stopped"
    elif isinstance(state, IdentityState):
        role = "reader" if call.value == "approved" else call.value
        if role not in state.roles:
            state.roles.append(role)
    elif isinstance(state, DocumentState):
        state.retrievals += 1
    else:
        state.result = "restricted" if "SYNTHETIC_RESTRICTED" in state.sample else "public"
