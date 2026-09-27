# MCP → n8n Agentic Automation Gateway

> A typed MCP gateway that gives an AI host a controlled interface for validating and dispatching allowlisted workflow actions.

## What this demonstrates

This project is the public portfolio implementation of an MCP-based automation pattern.

It demonstrates:

- MCP server construction with the official Python SDK
- typed tools derived from Python signatures
- explicit workflow allowlisting
- validation before external action
- an n8n HTTP adapter
- deterministic simulated mode for local development and CI
- in-memory MCP protocol tests
- a clear boundary between AI intent and operational actions

The official MCP Python SDK currently documents v2 as the stable release and supports MCP servers, clients, tools and standard transports. Its testing guidance uses an in-memory `Client(mcp)` connection so the actual protocol path can be tested without launching a server process. citeturn764085search5turn764085search0

## Architecture

```text
AI host / MCP client
        |
        v
   MCP Server
        |
        +--> list_workflows
        |
        +--> validate_workflow
        |
        +--> dispatch_workflow
                   |
                   v
             Allowlist check
                   |
          +--------+--------+
          |                 |
          v                 v
      simulated          n8n HTTP
        mode              adapter
          |                 |
          +--------+--------+
                   |
                   v
             workflow action
```

## Why the allowlist matters

An agent should not receive unrestricted access to arbitrary workflow endpoints.

The gateway accepts a logical workflow name and checks that the name is explicitly configured as allowed before it can dispatch anything.

```text
model intent
    ↓
typed MCP tool call
    ↓
allowlist validation
    ↓
approved workflow
    ↓
external action
```

This makes the gateway a useful safety and architecture boundary rather than simply exposing an HTTP endpoint to a model.

## Repository structure

```text
mcp-n8n-agent-gateway/
├── .github/workflows/ci.yml
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── n8n.py
│   └── server.py
├── tests/
│   └── test_server.py
├── .env.example
├── pyproject.toml
└── README.md
```

## Quick start

From this profile repository:

```bash
cd projects/mcp-n8n-agent-gateway
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# macOS/Linux
source .venv/bin/activate

pip install -e ".[dev]"
pytest -q
```

Run the MCP server over stdio:

```bash
python -m src.server
```

The official SDK also supports Streamable HTTP. `MCPServer.streamable_http_app()` returns an ASGI application that can be served by an ASGI server such as Uvicorn. citeturn543646search2

## Local simulated mode

The gateway is intentionally safe by default.

Without `N8N_BASE_URL`, `dispatch_workflow` returns a simulated result and never calls an external service.

Example configuration:

```env
N8N_BASE_URL=
N8N_API_TOKEN=
N8N_ALLOWED_WORKFLOWS=demo_sync,demo_report
```

## Optional n8n integration

For a permitted local n8n instance:

```env
N8N_BASE_URL=http://localhost:5678
N8N_API_TOKEN=...
N8N_ALLOWED_WORKFLOWS=demo_sync,demo_report
```

Only allowlisted logical workflow names can be dispatched. The adapter sends a POST request to:

```text
{N8N_BASE_URL}/webhook/{workflow}
```

Real deployments should add authentication, authorization, audit logging, retries/idempotency and deployment-specific network controls.

## Testing

Tests use the official SDK's in-memory client pattern. This lets CI exercise tool discovery and real MCP tool calls without opening a port or launching a subprocess. citeturn764085search0

## Security boundary

Never commit:

- PHI or other sensitive healthcare data
- n8n credentials or API keys
- production webhook URLs that should remain private
- employer-only workflow definitions
- session data or secrets

The public project uses explicit allowlisting and simulated mode to keep the demo deterministic and safe.

## Portfolio note

The important engineering pattern is:

**AI intent → typed MCP contract → policy boundary → workflow adapter → controlled action**

This is the foundation for the more advanced agentic systems in my roadmap.

## Author

**Pranay Eligeti**

[LinkedIn](https://www.linkedin.com/in/pranay-eligeti) · [GitHub](https://github.com/pranay-eligeti)
