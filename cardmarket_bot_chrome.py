"""
Alternative bot version that uses your installed Chrome
This helps avoid Cloudflare detection
"""
import csv
import time
import sys
import os


# Import the original class and stealth techniques
sys.path.insert(0, os.path.dirname(__file__))
from cardmarket_bot import CardmarketBot as BotOriginal
from stealth import get_stealth_scripts, get_browser_args, get_context_options

# Import configuration
try:
    from config import BOT_MODE
except ImportError:
    BOT_MODE = 'balanced'  # Default value if config.py doesn't exist


class CardmarketBotChrome(BotOriginal):
    """Bot version that uses system's installed Chrome with real profile"""

    def start(self):
        """Starts Chrome browser with advanced anti-detection techniques"""
        print("Starting Chrome with STEALTH MODE (anti-Cloudflare)...")
        from playwright.sync_api import sync_playwright

        self.playwright = sync_playwright().start()

        # Try using installed Chrome with stealth techniques
        try:
            # On Windows, Chrome is usually here
            chrome_paths = [
                "C:/Program Files/Google/Chrome/Application/chrome.exe",
                "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
                os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
            ]

            chrome_path = None
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_path = path
                    break

            if not chrome_path:
                print("[WARNING] Chrome installation not found")
                print("Using Playwright's Chromium...")
                super().start()
                return

            print(f"[OK] Chrome found: {chrome_path}")

            # Create separate profile for the bot
            user_data_dir = os.path.join(os.path.dirname(__file__), "chrome_bot_profile")

            if not os.path.exists(user_data_dir):
                os.makedirs(user_data_dir)
                print(f"[INFO] Creating stealth profile...")
            else:
                print(f"[INFO] Using existing stealth profile")

            time.sleep(1)

            # Get stealth options
            context_options = get_context_options()
            browser_args = get_browser_args()

            print("[INFO] Applying 21 anti-detection techniques...")

            # Use persistent_context with all stealth options
            context = self.playwright.chromium.launch_persistent_context(
                user_data_dir,
                executable_path=chrome_path,
                headless=self.headless,
                slow_mo=500,
                args=browser_args,
                **context_options
            )

            # Get page
            if len(context.pages) > 0:
                self.page = context.pages[0]
            else:
                self.page = context.new_page()

            # Save context reference
            self.browser = context

            # Inject ALL anti-detection scripts
            stealth_script = get_stealth_scripts()
            self.page.add_init_script(stealth_script)

            self.page.set_default_timeout(30000)

            print("[OK] Chrome STEALTH MODE activated")
            print("[OK] [+] Webdriver hidden")
            print("[OK] [+] Plugins spoofed")
            print("[OK] [+] Canvas fingerprint randomized")
            print("[OK] [+] WebGL vendor spoofed")
            print("[OK] [+] 21 anti-Cloudflare techniques active")
            print("[OK] Cloudflare should NOT detect you as a bot")

        except Exception as e:
            print(f"[ERROR] Could not launch Chrome stealth: {e}")
            print("\nTrying with Playwright's Chromium...")
            super().start()


def main():
    print("=" * 60)
    print("CARDMARKET BOT - STEALTH MODE (ANTI-CLOUDFLARE)")
    print("=" * 60)
    print("[+] 21 anti-detection techniques active")
    print("[+] Webdriver hidden + Fingerprints spoofed")
    print("[+] Persistent profile (cookies saved)")
    print("=" * 60)
    print("\nFirst time: Captcha may appear (solve it)")
    print("Following times: NO MORE CAPTCHA (cookies saved)")
    print("=" * 60)

    if len(sys.argv) < 2:
        print("\n[ERROR] Missing CSV file")
        print("\nUsage: python cardmarket_bot_chrome.py <csv_path>")
        print("Or use: run_bot_chrome.bat example_cards.csv")
        sys.exit(1)

    csv_path = sys.argv[1]

    if not os.path.exists(csv_path):
        print(f"\n[ERROR] File not found: {csv_path}")
        sys.exit(1)

    # Mode is loaded from config.py
    bot = CardmarketBotChrome(headless=False, mode=BOT_MODE)

    try:
        bot.start()
        bot.login_manual()
        bot.upload_cards(csv_path)

        print("\n" + "=" * 60)
        print("[OK] PROCESS COMPLETED")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n[INFO] Process cancelled by user")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nPress Enter to close browser...")
        bot.stop()


if __name__ == "__main__":
    main()
