import pytest
from mcp import Client
from src.server import mcp

@pytest.mark.anyio
async def test_tools_are_exposed():
    async with Client(mcp, raise_exceptions=True) as client:
        result = await client.list_tools()
        names = {tool.name for tool in result.tools}
        assert {"list_workflows", "validate_workflow", "dispatch_workflow"} <= names

@pytest.mark.anyio
async def test_allowlisted_dispatch(monkeypatch):
    from src import server
    monkeypatch.setattr(server.adapter, "allowed_workflows", {"demo_sync"})
    monkeypatch.setattr(server.adapter, "base_url", "")
    async with Client(mcp, raise_exceptions=True) as client:
        result = await client.call_tool("dispatch_workflow", {"workflow": "demo_sync", "payload": {"source": "synthetic"}})
        data = result.structured_content
        assert data["status"] == "simulated"
        assert data["workflow"] == "demo_sync"

@pytest.mark.anyio
async def test_disallowed_workflow_is_rejected(monkeypatch):
    from src import server
    monkeypatch.setattr(server.adapter, "allowed_workflows", {"demo_sync"})
    async with Client(mcp, raise_exceptions=True) as client:
        with pytest.raises(ValueError):
            await client.call_tool("dispatch_workflow", {"workflow": "not_allowed", "payload": {}})
