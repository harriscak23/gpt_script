from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=False)
    page = browser.new_page()

    page.goto("https://chatgpt.com/")

    input("Log in, then press Enter...")

    page.locator('a[href^="/c/"]').first.wait_for()

    chats = page.locator('a[href^="/c/"]')

    print(f"Found {chats.count()} chats\n")

    for i in range(chats.count()):
        chat = chats.nth(i)

        title = chat.inner_text().strip()

        aria = chat.get_attribute("aria-label") or ""

        is_pinned = "pinned conversation" in aria.lower()

        print(f"{title} | Pinned: {is_pinned}")

    input("\nPress Enter to close...")
    browser.close()