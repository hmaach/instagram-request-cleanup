import json
import time
from playwright.sync_api import sync_playwright

JSON_PATH = "pending_follow_requests.json"

def load_usernames(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    users = []
    for item in data.get("relationships_follow_requests_sent", []):
        for entry in item.get("string_list_data", []):
            username = entry.get("value")
            if username:
                users.append(username)
    return users


def cancel_requests(usernames):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Login manually
        page.goto("https://www.instagram.com/accounts/login/")
        input("Login, then press ENTER...")

        for username in usernames:
            url = f"https://www.instagram.com/{username}/"
            print(f"[+] Processing {username}")

            page.goto(url)
            page.wait_for_timeout(3000)

            btn = page.locator("button:has-text('Requested')")

            if btn.count() > 0:
                btn.first.click()
                page.wait_for_timeout(1500)

                confirm = page.locator("button:has-text('Unfollow')")
                if confirm.count() > 0:
                    confirm.first.click()
                    page.wait_for_timeout(2000)
                    print(f"[✓] Cancelled {username}")
                else:
                    print(f"[!] Confirm dialog not found for {username}")
            else:
                print(f"[!] No request found for {username}")

            time.sleep(2)  # avoid rate limits

        browser.close()


if __name__ == "__main__":
    usernames = load_usernames(JSON_PATH)
    cancel_requests(usernames)