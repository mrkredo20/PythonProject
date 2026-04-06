import os
from pathlib import Path

import pytest
from playwright.sync_api import Browser

from pages.session_page import SessionPage


VALID_EMAIL = os.getenv("BILETEBI_EMAIL")
VALID_PASSWORD = os.getenv("BILETEBI_PASSWORD")
ARTIFACTS_DIR = Path("test-artifacts")
ENABLE_ARTIFACTS = os.getenv("ENABLE_ARTIFACTS", "").lower() in {"1", "true", "yes"}


def _sanitize_nodeid(nodeid: str) -> str:
    return "".join(char if char.isalnum() or char in "-._" else "_" for char in nodeid)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def auth_storage_state(browser: Browser, tmp_path_factory) -> str:
    if not VALID_EMAIL or not VALID_PASSWORD:
        pytest.skip("Set BILETEBI_EMAIL and BILETEBI_PASSWORD to build biletebi auth state.")

    state_dir = tmp_path_factory.mktemp("auth")
    state_path = Path(state_dir) / "biletebi-auth.json"

    context = browser.new_context()
    page = context.new_page()

    session_page = SessionPage(page)
    session_page.open()
    session_page.login(VALID_EMAIL, VALID_PASSWORD)
    session_page.expect_logged_in_home()

    context.storage_state(path=str(state_path))
    context.close()

    return str(state_path)


@pytest.fixture
def auth_page(browser: Browser, auth_storage_state: str):
    context = browser.new_context(storage_state=auth_storage_state)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(autouse=True)
def capture_playwright_artifacts(request):
    if "page" not in request.fixturenames and "auth_page" not in request.fixturenames:
        yield
        return

    page_fixture_name = "page" if "page" in request.fixturenames else "auth_page"
    page = request.getfixturevalue(page_fixture_name)
    yield

    if not ENABLE_ARTIFACTS:
        return

    context = page.context
    failed = bool(getattr(request.node, "rep_call", None) and request.node.rep_call.failed)
    node_name = _sanitize_nodeid(request.node.nodeid)

    if not hasattr(context, "_codex_tracing_started"):
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        setattr(context, "_codex_tracing_started", True)

    if failed:
        screenshots_dir = ARTIFACTS_DIR / "screenshots"
        traces_dir = ARTIFACTS_DIR / "traces"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        traces_dir.mkdir(parents=True, exist_ok=True)

        page.screenshot(path=str(screenshots_dir / f"{node_name}.png"), full_page=True)
        context.tracing.stop(path=str(traces_dir / f"{node_name}.zip"))
    else:
        context.tracing.stop()
