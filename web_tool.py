from langchain_core.tools import tool

from src.browser import get_page


@tool
def play_youtube_video(query: str) -> str:
    """Search a video/song on YouTube and play the first result.
    Just give the video or song name as the query."""
    page = get_page()
    page.goto(f"https://www.youtube.com/results?search_query={query}")

    try:
        page.wait_for_selector("ytd-video-renderer a#video-title", timeout=10000)
    except Exception:
        return "YouTube search results didn't load in time."

    first_video = page.query_selector("ytd-video-renderer a#video-title")
    if first_video:
        first_video.click()
        return f"Playing '{query}' on YouTube."

    return f"Couldn't find any video for '{query}'."
