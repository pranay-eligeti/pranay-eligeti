"""Typed models for workflow dispatch."""
from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field

class WorkflowRequest(BaseModel):
    workflow: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)

class WorkflowResult(BaseModel):
    workflow: str
    status: str
    detail: str
