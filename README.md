# ChatGPT Cleaner

Automates deletion of **unpinned** ChatGPT conversations with Playwright. Pinned chats are left alone. Supports multiple accounts via saved session files, and can run locally or on a schedule with GitHub Actions.

## Requirements

- Python 3.12+
- [Google Chrome](https://www.google.com/chrome/) installed (used via Playwright’s `channel="chrome"`)
- A ChatGPT account

## Setup

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
playwright install chrome
```

## Quick start

### 1. Log in once per account

```bash
python login.py <account>
```

Example:

```bash
python login.py personal
```

1. Chrome opens to ChatGPT.
2. Log in manually in the browser.
3. Return to the terminal and press Enter.

This saves session state to `sessions/<account>.json` (cookies and storage). That file is gitignored — do not commit it.

### 2. Clean unpinned chats

```bash
python clean.py
```

The cleaner discovers every `*.json` file under `sessions/`, opens ChatGPT with that session, expands the sidebar if needed, and deletes unpinned conversations one by one until none remain among the currently loaded chats.

## Multiple accounts

Each account needs its own login:

```bash
python login.py personal
python login.py work
```

That creates:

```text
sessions/
  personal.json
  work.json
```

Running `python clean.py` cleans every account that has a session file. Accounts without a session are skipped with a warning.

## Configuration

Shared settings live in `config.py`:

| Setting       | Default              | Meaning                                      |
|---------------|----------------------|----------------------------------------------|
| `CHATGPT_URL` | `https://chatgpt.com`| Target URL                                   |
| `SESSION_DIR` | `sessions`           | Directory for account session files          |
| `CHANNEL`     | `chrome`             | Browser channel for Playwright               |
| `HEADLESS`    | `True`               | Run without a visible window (`clean.py`)    |
| `USER_AGENT`  | Chrome UA string     | User agent applied when loading a session    |

`login.py` always runs with a visible browser (`headless=False`) so you can sign in. To watch the cleaner locally, set `HEADLESS = False` in `config.py`.

## Project layout

```text
gpt_script/
├── login.py              # Interactive login → sessions/<account>.json
├── clean.py              # Delete unpinned conversations
├── auth.py               # Session path helpers
├── config.py             # Shared settings
├── requirements.txt
├── sessions/             # Local session files (gitignored)
└── .github/workflows/
    └── clean.yml         # Scheduled / manual CI run
```

## How cleaning works

1. Load each account’s Playwright `storage_state`.
2. Open ChatGPT and ensure the sidebar is expanded.
3. Scan currently loaded conversation links (`a[href^="/c/"]`).
4. Skip chats whose `aria-label` includes `"pinned conversation"`.
5. For each unpinned chat: hover → open options → Delete → confirm → wait until that chat disappears.
6. Restart the scan after each deletion (avoids broken indexes when the sidebar updates).

## GitHub Actions

The workflow in `.github/workflows/clean.yml` runs:

- on a schedule (`0 8 * * *` UTC — daily at 08:00)
- manually via **Actions → ChatGPT Cleaner → Run workflow**

It restores session archives from repository secrets, then runs `python clean.py`.

### Preparing session secrets

On your machine, after logging in:

```bash
# Example for one account named "cse"
cd sessions
zip cse.zip cse.json
base64 cse.zip   # copy the output into a GitHub secret
```

Create a repository secret for each account (for example `CSE_SESSION_ZIP`, `UW_SESSION_ZIP`, `F04_SESSION_ZIP`) with those base64 strings.

For **each** ChatGPT account you want cleaned in CI, also add a restore-session block in `.github/workflows/clean.yml` under the **Restore sessions** step:

```yaml
echo "${{ secrets.ACCOUNT_SESSION_ZIP }}" | base64 -d > account.zip
unzip -o account.zip -d sessions
```

Replace `ACCOUNT_SESSION_ZIP` / `account` with that account’s secret name and zip filename (matching the pattern already used for `cse`, `uw`, and `f04`). Without this, the session file never appears in `sessions/` and that account is skipped.

Sessions expire when ChatGPT invalidates cookies. If CI starts skipping accounts or failing auth, re-run `login.py` locally and refresh the secrets.

## Notes

- Only **unpinned** conversations are deleted. Pin anything you want to keep.
- ChatGPT’s UI can change; if selectors break, update the locators in `clean.py`.
- Session files are credentials — treat `sessions/` like passwords.
- `concepts.md` is a learning notebook for Playwright patterns used in this project; it is not required to run the scripts.
