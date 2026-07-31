import logging

from playwright.sync_api import sync_playwright

from config import CHATGPT_URL, HEADLESS, CHANNEL, USER_AGENT
from auth import get_accounts, get_session_path


CHAT_SELECTOR = 'a[href^="/c/"]'
OPTIONS_SELECTOR = 'button[aria-label^="Open conversation options"]'

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)

def get_chats(page):
    return page.locator(CHAT_SELECTOR)


def is_pinned(chat):
    aria = chat.get_attribute("aria-label") or ""
    return "pinned conversation" in aria.lower()


def delete_chat(page, chat):
    title = chat.inner_text().strip()
    href = chat.get_attribute("href")

    chat.hover()

    chat.locator(OPTIONS_SELECTOR).click()

    page.get_by_test_id(
        "delete-chat-menu-item"
    ).click()

    page.get_by_test_id(
        "delete-conversation-confirm-button"
    ).click()

    page.locator(
        f'a[href="{href}"]'
    ).wait_for(
        state="detached"
    )

    return title


def delete_all_unpinned(page):
    
    # Wait for ChatGPT sidebar to finish rendering
    # Not good practice
    page.wait_for_timeout(3000)

    chats = get_chats(page)

    if chats.count() == 0:
        logger.info("Sidebar empty. Nothing to delete.")
        return

    deleted_count = 0

    while True:
        chats = get_chats(page)
        count = chats.count()

        logger.info(f"Loaded chats: {count}")

        found_unpinned = False

        for i in range(count):
            chat = chats.nth(i)

            try:
                title = chat.inner_text().strip()
                pinned = is_pinned(chat)

                logger.info(f"{title} | Pinned: {pinned}")

                if not pinned:
                    deleted_title = delete_chat(page, chat)

                    deleted_count += 1
                    found_unpinned = True

                    logger.info(
                        f"Deleted: {deleted_title}"
                    )

                    # DOM changed, restart search
                    break

            except Exception:
                logger.exception(
                    "Failed processing chat."
                )

        # We scanned all chats and found nothing to delete
        if not found_unpinned:
            logger.info(
                f"Finished. Deleted {deleted_count} chats."
            )
            return


def open_sidebar(page):

    close_button = page.get_by_test_id(
        "close-sidebar-button"
    )

    # Sidebar already open
    if close_button.count():
        logger.info("Sidebar already open.")
        return

    open_button = page.get_by_role(
        "button",
        name="Open sidebar"
    )

    open_button.wait_for(
        state="visible"
    )

    open_button.click()

    close_button.wait_for()

    logger.info("Sidebar opened.")

def clean_account(browser, account):

    session_path = get_session_path(account)

    if not session_path.exists():
        logger.warning(
            f"Skipping {account}: session not found."
        )
        return

    context = None

    try:
        context = browser.new_context(
            storage_state=session_path,
            user_agent=USER_AGENT,
            viewport={
                "width": 1280,
                "height": 720
            }
        )
        page = context.new_page()

        page.goto(CHATGPT_URL)

        logger.info(
            f"Cleaning account: {account}"
        )

        open_sidebar(page)

        delete_all_unpinned(page)

    except Exception:
        logger.exception(
            f"Cleaner crashed for {account}."
        )

    finally:
        if context:
            context.close()

def main():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            channel=CHANNEL,
            headless=HEADLESS
        )

        try:
            for account in get_accounts():
                clean_account(
                    browser,
                    account
            )

        finally:
            browser.close()

if __name__ == "__main__":
    main()