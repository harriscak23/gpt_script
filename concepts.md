# Playwright Concepts Summary

This is a consolidated reference of every Playwright concept learned so far.

---

# 1. Browser Automation

Playwright is a Python library that controls a real web browser.

Architecture:

```
Python Code
      │
      ▼
Playwright
      │
      ▼
Google Chrome
      │
      ▼
Website
```

The script does **not** communicate directly with ChatGPT—it controls Chrome just like a human would.

---

# 2. sync_playwright()

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ...
```

Starts the Playwright engine.

The `with` block automatically initializes and cleans up Playwright.

---

# 3. Browser vs Page

```python
browser = p.chromium.launch(...)
page = browser.new_page()
```

Think of it as:

```
Chrome Application
│
├── Tab 1
├── Tab 2
└── Tab 3
```

- Browser = entire Chrome process.
- Page = one browser tab.

---

# 4. Launching Google Chrome

Instead of the bundled Chromium browser:

```python
browser = p.chromium.launch(
    channel="chrome",
    headless=False
)
```

- `channel="chrome"` → use installed Google Chrome.
- `headless=False` → show the browser window.

---

# 5. Navigation

```python
page.goto(url)
```

Equivalent to typing a URL into the address bar.

---

# 6. Locators

A locator describes **how to find** an element.

Examples:

```python
page.locator("#searchInput")
```

```python
page.get_by_role("button", name="Delete")
```

A locator is **not** the HTML element itself.

It is an object that knows how to locate that element whenever needed.

---

# 7. Lazy Locators

Locators do **not** immediately search the page.

Example:

```python
search = page.locator("#searchInput")
```

Nothing happens yet.

The search occurs only when:

```python
search.fill(...)
```

or

```python
search.click()
```

Benefits:

- Survives page updates.
- Supports automatic waiting.
- Avoids stale element references.

---

# 8. Locator Actions

Common methods:

```python
.fill(text)
.click()
.press(key)
.inner_text()
```

Pattern:

```python
locator.action(...)
```

---

# 9. Auto Waiting

Playwright automatically waits until an element is:

- present
- visible
- enabled
- ready for interaction

Avoid:

```python
time.sleep(...)
```

unless absolutely necessary.

---

# 10. page.pause()

```python
page.pause()
```

Purpose:

- Opens Playwright Inspector.
- Pauses execution.
- Allows locator testing.
- Helps debug scripts.

Use during development.

Remove in production.

---

# 11. HTML Basics

Example:

```html
<input
    id="searchInput"
    name="search"
    type="search">
```

Important concepts:

Tag:

```html
<input>
```

Attributes:

```html
id="..."
name="..."
type="..."
class="..."
```

Playwright uses these to locate elements.

---

# 12. CSS Selectors

Examples:

ID

```python
"#searchInput"
```

Class

```python
".chat"
```

Tag

```python
"button"
```

Attribute

```python
'[data-sidebar-item="true"]'
```

---

# 13. Accessibility Locators

Preferred when possible.

Example:

```python
page.get_by_role(
    "button",
    name="Delete"
)
```

Advantages:

- More readable.
- Closer to user interactions.
- Often more robust.

---

# 14. Finding Multiple Elements

```python
links = page.locator("a")
```

A locator can represent:

- one element
- many elements

---

# 15. count()

```python
count = links.count()
```

Returns the number of matched elements.

Preferred pattern:

```python
count = links.count()

for i in range(count):
    ...
```

instead of repeatedly calling `count()`.

---

# 16. nth()

```python
chat = chats.nth(i)
```

Selects the i-th matched element.

Examples:

```python
nth(0)
```

First.

```python
nth(1)
```

Second.

---

# 17. inner_text()

```python
locator.inner_text()
```

Returns visible text.

Example:

```html
<span>Hello</span>
```

returns

```
Hello
```

Not HTML.

Not attributes.

Only visible text.

---

# 18. Chaining Locators

Instead of searching the entire page:

```python
page.locator(".title")
```

Search inside another locator:

```python
chat.locator(".title")
```

This narrows the search scope.

---

# 19. Scope

Think of the DOM like a tree:

```
Page
│
├── Chat 1
│     ├── Title
│     └── Pin
│
├── Chat 2
│     ├── Title
│     └── Pin
│
└── Chat 3
      ├── Title
      └── Pin
```

Searching from:

```python
page.locator(...)
```

looks through the whole page.

Searching from:

```python
chat.locator(...)
```

looks only inside one chat.

This is one of the most important concepts in Playwright.

---

# 20. Typical Locator Pattern

```python
elements = page.locator(...)

count = elements.count()

for i in range(count):
    element = elements.nth(i)

    # interact with element
```

This pattern is used constantly.

---

# 21. ChatGPT Sidebar Structure (Discovered)

Conversation:

```html
<a data-sidebar-item="true">
```

Title:

```html
<span>
```

Pin button:

```html
<button aria-label="Pin ...">
```

Options button:

```html
<button aria-label="Open conversation options ...">
```

Likely locator:

```python
page.locator('[data-sidebar-item="true"]')
```

---

# 22. Locator Strategy

General strategy:

```
Page
 ↓
Find all chats
 ↓
Pick one chat
 ↓
Search inside that chat
 ↓
Read title
 ↓
Check pin
 ↓
Open menu
 ↓
Delete if appropriate
```

---

# 23. Development Philosophy

Always build automation in this order:

1. Open browser.
2. Navigate.
3. Inspect HTML.
4. Identify reliable locators.
5. Print information.
6. Verify correctness.
7. Perform safe actions.
8. Perform destructive actions (delete) **last**.

Never automate deletion before confirming the script is identifying the correct elements.

---

# 24. Mental Models

### Browser hierarchy

```
Browser
│
└── Page
     │
     └── HTML
```

### Locator hierarchy

```
Page
│
└── Locator
      │
      └── Action
```

### DOM hierarchy

```
Page
│
├── Conversation
│      ├── Title
│      ├── Pin
│      └── Menu
│
├── Conversation
│      ├── Title
│      ├── Pin
│      └── Menu
│
└── ...
```

---

# 25. General Playwright Workflow

Almost every Playwright script follows this lifecycle:

```python
# 1. Start Playwright
with sync_playwright() as p:

    # 2. Launch browser
    browser = ...

    # 3. Create page
    page = ...

    # 4. Navigate
    page.goto(...)

    # 5. Locate element(s)
    locator = page.locator(...)

    # 6. Read or interact
    locator.click()
    locator.fill()
    locator.inner_text()

    # 7. Repeat as needed

    # 8. Close browser
    browser.close()
```

# 26. Locator vs ElementHandle

Playwright has two ways to reference elements:

- **Locator**
- **ElementHandle**

They are different objects with different purposes.

---

## Locator

Created using:

```python
locator = page.locator(...)
```

A **Locator** describes **how to find** an element.

A Locator can represent:

- One element
- Many elements

Examples:

```python
locator.count()
locator.nth(i)
locator.click()
locator.inner_text()
locator.get_attribute(...)
```

Locators are preferred because they:

- Are lazy (they find the element only when needed)
- Automatically wait for elements
- Handle dynamic pages well
- Avoid stale element problems

---

## ElementHandle

Created using:

```python
element = page.wait_for_selector(...)
```

An **ElementHandle** represents **one specific element** that was found at that moment.

Example:

```python
element = page.wait_for_selector("button")
```

Unlike Locators, ElementHandles do **not** support:

```python
.count()
.nth()
```

because they represent only one element.

### Lesson

Use:

```python
page.locator(...)
```

for almost all automation tasks.

Use:

```python
page.wait_for_selector(...)
```

only when you specifically need a single element reference.

---

# 27. Reading HTML Attributes

`inner_text()` retrieves **visible text**.

Example:

```python
locator.inner_text()
```

HTML:

```html
<span>Hello</span>
```

Returns:

```
Hello
```

It does **not** return:

- HTML
- Attributes
- Hidden values

Many important values are stored inside HTML attributes.

Example:

```html
<button aria-label="Delete conversation">
```

Read the attribute using:

```python
locator.get_attribute("aria-label")
```

Returns:

```
Delete conversation
```

### Rule

Use:

```python
inner_text()
```

for visible text.

Use:

```python
get_attribute()
```

for information stored inside HTML attributes.

---

# 28. Waiting for Specific Elements

Initially used:

```python
page.wait_for_load_state("networkidle")
```

However, modern websites like ChatGPT are dynamic applications.

`networkidle` only means network activity has temporarily stopped.

It does **not** guarantee:

- The UI is fully rendered
- Dynamic elements exist
- The sidebar has loaded

A better approach is to wait for the exact element your script needs.

Example:

```python
page.locator('a[href^="/c/"]').first.wait_for()
```

Meaning:

Wait until the first conversation link appears.

### General Principle

Don't wait for the page to finish loading.

Wait for the thing your script actually needs.

---

# 29. Testing Locator Accuracy

Never trust a locator just because it matches one inspected element.

Correct workflow:

```
Inspect HTML
      ↓
Create locator
      ↓
Test against entire page
      ↓
Check results
      ↓
Refine locator
```

Example:

Initially discovered:

```html
<a data-sidebar-item="true">
```

Using:

```python
page.locator('[data-sidebar-item="true"]')
```

matched more elements than expected.

It also matched unrelated sidebar items.

### Lesson

A selector that matches one element is not necessarily specific enough for the entire page.

---

# 30. Finding ChatGPT Conversations

Initial assumption:

```html
<a data-sidebar-item="true">
```

represented conversations.

This selector was too broad.

Further inspection showed conversation URLs always begin with:

```
/c/
```

Example:

```
/c/6a58856f-d628-83e8-aa06-c1edcf899e90
```

Final locator:

```python
chats = page.locator('a[href^="/c/"]')
```

Explanation:

```
a
↓
Find all links

href^="/c/"
↓
Only links whose href starts with /c/
```

This correctly identifies only conversation links.

---

# 31. Conversation Title Extraction

Originally planned:

```python
chat.locator("span").inner_text()
```

because the title appeared inside:

```html
<span dir="auto">
    Test 1
</span>
```

After further inspection:

The conversation link itself already contains the visible title.

Simply use:

```python
title = chat.inner_text().strip()
```

### Lesson

Don't create unnecessary nested locators.

If the parent element already contains the information you need, read it directly.

---

# 32. Detecting Pinned Conversations

Pinned conversation:

```html
<a aria-label="Test 1, pinned conversation">
```

Unpinned conversation:

```html
<a aria-label="Test 2">
```

The pinned state is stored inside the conversation's `aria-label`.

Detection:

```python
label = chat.get_attribute("aria-label") or ""
is_pinned = "pinned conversation" in label.lower()
```

Example:

Pinned:

```
Test 1, pinned conversation
```

Contains:

```
pinned conversation
```

Result:

```
True
```

Unpinned:

```
Test 2
```

Result:

```
False
```

---

# 33. Locator Selection Strategy

When multiple locator options exist, choose the one that describes **what an element represents**, not what it looks like.

Preferred order:

1. Semantic attributes
   - `href`
   - `role`
   - `aria-label`

2. Stable data attributes
   - `data-testid`
   - `data-*`

3. Visible text

4. CSS classes

5. Visual details
   - SVGs
   - Icons
   - Generated classes
   - DOM position

Example:

Good:

```python
page.locator('a[href^="/c/"]')
```

because it identifies conversation links.

Less reliable:

```python
page.locator(".icon-sm")
```

because it only describes appearance.

### General Rule

Automate what an element **means**, not what it **looks like**.

---

# 34. Current ChatGPT Cleanup Workflow

Current planned workflow:

```
Launch Chrome
      ↓
Open ChatGPT
      ↓
Log in
      ↓
Wait for conversation links
      ↓
Find all conversations
      ↓
Read conversation title
      ↓
Determine pinned status
      ↓
Print and verify results
      ↓
Open conversation options
      ↓
Delete only unpinned conversations
```

---

# 35. Current Detection Logic

Current detection stage:

```python
chats = page.locator('a[href^="/c/"]')

for i in range(chats.count()):
    chat = chats.nth(i)

    title = chat.inner_text().strip()

    label = chat.get_attribute("aria-label") or ""

    is_pinned = "pinned conversation" in label.lower()

    print(title, is_pinned)
```

Expected output:

```text
Test 1 True
Test 2 False
```

---
