from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(user_data_dir="./chrome_profile", headless=False)
    page = context.new_page()

    page.goto("https://chatgpt.com/")

    input("If ready, press Enter...")

    chats = page.locator('a[href^="/c/"]')
    chats.first.wait_for()

    print(f"Found {chats.count()} chats\n")
    count = chats.count()
    for i in range(count):
        chat = chats.nth(i)

        title = chat.inner_text().strip()

        aria = chat.get_attribute("aria-label") or ""

        is_pinned = "pinned conversation" in aria.lower()

        options_button = chat.locator('button[aria-label^="Open conversation options"]')
        options_button.wait_for()

        print(f"{title} | Pinned: {is_pinned} | Options button: {options_button.count()} |")

        chat.hover()
        options_button.click()
        delete_button = page.get_by_test_id("delete-chat-menu-item")
        delete_button.wait_for()
        print(f"Delete button: {delete_button.count()}")
        page.keyboard.press("Escape")
        
        # if is_pinned:
            

    input("\nPress Enter to close...")
    context.close()