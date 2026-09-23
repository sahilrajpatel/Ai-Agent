"""
All the tools need to work on the SAME browser window (e.g. WhatsApp needs
to stay logged in, YouTube tab should stay open etc.) so this file keeps one
shared browser instance that every tool can grab.
"""
from playwright.sync_api import sync_playwright

from src import config

_playwright = None
_context = None


def get_browser_context():
    """
    Starts the browser the first time it's called, and reuses the same one
    after that. Uses a persistent profile folder so logins (like WhatsApp
    Web) are remembered between runs.
    """
    global _playwright, _context

    if _context is None:
        _playwright = sync_playwright().start()
        _context = _playwright.chromium.launch_persistent_context(
            user_data_dir=config.BROWSER_PROFILE_DIR,
            headless=config.HEADLESS,
        )

    return _context


def get_page():
    """Returns a page (tab) to work with - reuses the first open tab."""
    context = get_browser_context()
    if context.pages:
        return context.pages[0]
    return context.new_page()


def close_browser():
    global _playwright, _context
    if _context:
        _context.close()
    if _playwright:
        _playwright.stop()
    _context = None
    _playwright = None
