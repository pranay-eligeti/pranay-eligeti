"""Streamable HTTP entrypoint for the MCP gateway."""
from __future__ import annotations

from mcp.server import MCPServer
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from .server import mcp


@mcp.custom_route("/health", methods=["GET"])
async def health(_: Request) -> Response:
    return JSONResponse({"status": "ok", "service": "mcp-n8n-agent-gateway"})


app = mcp.streamable_http_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
