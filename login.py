import sys

from playwright.sync_api import sync_playwright

from config import CHATGPT_URL, CHANNEL
from auth import get_session_path


def main():

    if len(sys.argv) != 2:
        print(
            "Usage: python login.py <account>"
        )
        sys.exit(1)

    account = sys.argv[1]

    session_path = get_session_path(account)

    session_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with sync_playwright() as p:

        browser = p.chromium.launch(
            channel=CHANNEL,
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled"
            ] # Might not always work to bypass Google automation detection
        )

        context = browser.new_context()

        try:
            page = context.new_page()

            page.goto(CHATGPT_URL)

            input(
                "Log in, then press Enter..."
            )

            context.storage_state(
                path=session_path
            )

        finally:
            context.close()
            browser.close()

    print(
        f"Saved session to {session_path}"
    )

if __name__ == "__main__":
    main()