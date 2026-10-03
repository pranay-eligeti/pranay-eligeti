# MCP → n8n Agentic Automation Gateway

Current maintained implementation: [MCP Action Gateway](https://github.com/pranay-eligeti/mcp-action-gateway). This directory preserves the earlier snapshot.

> A typed MCP gateway that gives an AI host a controlled interface for validating and dispatching allowlisted workflow actions.

## What this demonstrates

This project is a public portfolio implementation of an MCP-based automation pattern.

It demonstrates:

- MCP server construction with the official Python SDK
- typed tools derived from Python signatures
- explicit workflow allowlisting
- validation before external action
- an n8n HTTP adapter
- deterministic simulated mode for local development and CI
- in-memory MCP protocol tests
- Streamable HTTP deployment shape
- Docker packaging
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

This makes the gateway a policy boundary rather than simply exposing a generic HTTP endpoint to a model.

## Repository structure

```text
mcp-n8n-agent-gateway/
├── .github/workflows/ci.yml
├── Dockerfile
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── n8n.py
│   └── server.py
├── tests/
│   ├── test_http_app.py
│   └── test_server.py
├── .env.example
├── pyproject.toml
└── README.md
```

## Quick start

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

Run the stdio MCP server:

```bash
python -m src.server
```

Run Streamable HTTP locally:

```bash
uvicorn src.app:app --host 127.0.0.1 --port 8000
```

The MCP endpoint is `http://127.0.0.1:8000/mcp`. The official SDK exposes `streamable_http_app()` as an ASGI application that can be served by Uvicorn or another ASGI host. citeturn543646search2turn543646search0

Health endpoint:

```text
GET /health
```

## Local simulated mode

The gateway is intentionally safe by default.

Without `N8N_BASE_URL`, `dispatch_workflow` returns a simulated result and never calls an external service.

Example:

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

Only allowlisted logical workflow names can be dispatched.

Real deployments should add authentication, authorization, audit logging, retries/idempotency, network controls and secret management appropriate to the environment.

## Docker

```bash
docker build -t mcp-n8n-agent-gateway .
docker run --rm -p 8000:8000 mcp-n8n-agent-gateway
```

## Testing

The tests use the official SDK's in-memory client pattern. Tool discovery and real MCP tool calls are exercised without launching a subprocess or opening a port. citeturn764085search0

## Security boundary

Never commit PHI, production credentials, private n8n URLs, employer-only workflow definitions, or sensitive records.

The gateway uses explicit allowlisting and simulated default mode to keep the portfolio project deterministic and safe.

## Portfolio note

The important engineering pattern is:

**AI intent → typed MCP contract → policy boundary → workflow adapter → controlled action**

This is the foundation for the RAG, evaluation and production AI projects in my roadmap.

## Author

**Pranay Eligeti**

[LinkedIn](https://www.linkedin.com/in/pranay-eligeti) · [GitHub](https://github.com/pranay-eligeti)
