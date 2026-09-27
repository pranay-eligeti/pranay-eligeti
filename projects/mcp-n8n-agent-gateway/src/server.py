"""MCP server exposing typed, allowlisted workflow actions."""
from __future__ import annotations
from typing import Any
from mcp.server import MCPServer
from .n8n import N8nWorkflowAdapter

mcp = MCPServer(
    "AI Automation Gateway",
    instructions="Use only allowlisted workflow names. Do not transmit secrets or sensitive records through demo workflows.",
)
adapter = N8nWorkflowAdapter()

@mcp.tool(title="List allowed workflows")
def list_workflows() -> list[str]:
    """Return workflow names explicitly allowed by configuration."""
    return sorted(adapter.allowed_workflows)

@mcp.tool(title="Validate workflow request")
def validate_workflow(workflow: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Validate a workflow request without dispatching it."""
    adapter.assert_allowed(workflow)
    return {"workflow": workflow, "valid": True, "payload_keys": sorted((payload or {}).keys())}

@mcp.tool(title="Dispatch workflow")
async def dispatch_workflow(workflow: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Dispatch an explicitly allowlisted workflow through the n8n adapter."""
    return {"workflow": workflow, **await adapter.dispatch(workflow, payload or {})}

if __name__ == "__main__":
    mcp.run()
