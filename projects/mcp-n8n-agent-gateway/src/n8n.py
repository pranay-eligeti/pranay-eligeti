"""Allowlisted n8n adapter with deterministic simulated mode."""
from __future__ import annotations
import os
from typing import Any
import httpx

class N8nWorkflowAdapter:
    def __init__(self, base_url: str | None = None, token: str | None = None, allowed_workflows: set[str] | None = None):
        self.base_url = (base_url or os.getenv("N8N_BASE_URL", "")).rstrip("/")
        self.token = token or os.getenv("N8N_API_TOKEN", "")
        configured = os.getenv("N8N_ALLOWED_WORKFLOWS", "")
        self.allowed_workflows = allowed_workflows or {x.strip() for x in configured.split(",") if x.strip()}

    def assert_allowed(self, workflow: str) -> None:
        if workflow not in self.allowed_workflows:
            raise ValueError(f"Workflow is not allowlisted: {workflow}")

    async def dispatch(self, workflow: str, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_allowed(workflow)
        if not self.base_url:
            return {"status": "simulated", "detail": f"Simulated dispatch to {workflow}", "payload_keys": sorted(payload)}

        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["X-N8N-API-KEY"] = self.token
        url = f"{self.base_url}/webhook/{workflow}"
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return {"status": "delivered", "detail": f"n8n accepted workflow {workflow}", "response": response.text[:1000]}
