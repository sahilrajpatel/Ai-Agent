import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_MODEL = "gpt-4o-mini"

# playwright saves the browser session (cookies/login) here
# so you don't have to scan the WhatsApp QR code every single time
BROWSER_PROFILE_DIR = "browser_profile"

# set to True once you're done testing / don't need to see the browser
HEADLESS = False
