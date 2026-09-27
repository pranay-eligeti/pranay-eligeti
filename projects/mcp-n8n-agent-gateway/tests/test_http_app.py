def test_http_app_exposes_mcp_route():
    from src.app import app
    paths = {getattr(route, "path", None) for route in app.routes}
    assert "/mcp" in paths
    assert "/health" in paths
