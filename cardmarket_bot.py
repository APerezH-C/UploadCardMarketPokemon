"""
Bot to upload Pokemon cards to Cardmarket from a CSV file
"""
import csv
import time
from playwright.sync_api import sync_playwright, Page, TimeoutError as PlaywrightTimeoutError
from human_behavior import (
    random_delay, long_random_delay, extra_long_pause,
    random_scroll, random_mouse_movement, simulate_human_page_view,
    should_take_long_break, add_human_randomness, get_delay_settings
)


class CardmarketBot:
    def __init__(self, headless=False, mode='balanced'):
        self.headless = headless
        self.browser = None
        self.page = None
        self.base_url = "https://www.cardmarket.com/en/Pokemon"
        self.delay_settings = get_delay_settings(mode)
        self.mode = mode
        print(f"[INFO] Behavior mode: {mode.upper()}")
        print(f"[INFO] Delays between cards: {self.delay_settings['between_cards'][0]}-{self.delay_settings['between_cards'][1]}s")
        print(f"[INFO] Long pause every {self.delay_settings['break_interval']} cards")

    def start(self):
        """Starts the browser with anti-detection configuration"""
        print("Starting anti-detection browser...")
        self.playwright = sync_playwright().start()

        # Configure browser to avoid Cloudflare detection
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=500,
            args=[
                '--disable-blink-features=AutomationControlled',  # Hide automation
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )

        # Create context with realistic configuration
        context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['geolocation', 'notifications'],
            color_scheme='light'
        )

        self.page = context.new_page()

        # Inject script to hide webdriver
        self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // Override plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            // Override languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });

            // Chrome runtime
            window.chrome = {
                runtime: {}
            };
        """)

        # Increase default timeout
        self.page.set_default_timeout(30000)
        print("[OK] Browser started (anti-detection mode)")

    def login_manual(self):
        """Allows manual user login"""
        print("\n" + "=" * 60)
        print("MANUAL LOGIN + CLOUDFLARE")
        print("=" * 60)
        print("1. Cardmarket will open in the browser")
        print("2. SOLVE THE CLOUDFLARE CAPTCHA (if it appears)")
        print("3. Login manually to Cardmarket")
        print("4. Return to this console and press Enter")
        print("=" * 60)

        # Navigate to Cardmarket
        print("\nOpening Cardmarket...")
        self.page.goto(self.base_url, wait_until='networkidle')

        # Wait a bit for Cloudflare to load
        time.sleep(3)

        print("\n[INFO] If you see the Cloudflare captcha:")
        print("  1. Check the 'Verify you are human' box")
        print("  2. Wait for it to let you through")
        print("  3. Login to Cardmarket")

        input("\nPress Enter when you have logged in...")
        print("[OK] Session started")

    def parse_csv(self, csv_path):
        """Reads the CSV and returns a list of cards"""
        cards = []

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse price (replace comma with dot)
                price = row['UNIT_PRICE'].replace(',', '.')

                # Determine if it's REVERSE HOLO or HOLO
                quality = row['QUALITY'].strip().upper()
                is_reverse_holo = quality == 'REVERSE HOLO'
                is_holo = quality == 'HOLO'

                card = {
                    'code': row['CODE'].strip(),
                    'quantity': int(row['QUANTITY']),
                    'price': float(price),
                    'quality': 'NORMAL' if (is_reverse_holo or is_holo) else quality,
                    'condition': row['CONDITION'].strip(),
                    'language': row['LANGUAGE'].strip(),
                    'reverse_holo': is_reverse_holo,
                    'comments': 'HOLO' if is_holo else ''
                }

                cards.append(card)

        print(f"[OK] Read {len(cards)} cards from CSV")
        return cards

    def add_card(self, card):
        """Adds a card to the Cardmarket inventory"""
        print(f"Adding: {card['code']} x{card['quantity']} - {card['price']} EUR")

        try:
            # Human behavior: view current page
            simulate_human_page_view(self.page)

            # Step 1: Go to main page if we're not there
            if self.page.url != self.base_url:
                self.page.goto(self.base_url)
                random_delay(1, 2)

            # Step 2: Search for card by code in the search box
            print(f"  [1/6] Searching for card: {card['code']}")

            # Try various common selectors for the search box
            search_selectors = [
                "input[id='ProductSearchInput']"
            ]

            search_box = None
            for selector in search_selectors:
                try:
                    search_box = self.page.wait_for_selector(selector, timeout=3000)
                    if search_box:
                        break
                except:
                    continue

            if not search_box:
                raise Exception("Search box not found. Check the selector.")

            # Clear and write in the search box (simulate human typing)
            search_box.fill("")
            random_delay(0.3, 0.7)
            search_box.fill(card['code'])
            random_delay(0.5, 1.2)

            # Press Enter or wait for results
            search_box.press("Enter")
            random_delay(2, 3.5)

            # Step 3: Click on first result
            print(f"  [2/6] Selecting first result")

            # Try clicking on the first search result
            first_result_selectors = [
                f"text={card['code']}",
                ".search-result:first-child a",
                ".product-item:first-child a",
                ".table-body .row:first-child a"
            ]

            for selector in first_result_selectors:
                try:
                    # Random scroll before clicking
                    random_scroll(self.page)
                    random_delay(0.5, 1)
                    self.page.click(selector, timeout=3000)
                    break
                except:
                    continue

            random_delay(2, 4)

            # Human behavior: view product page
            simulate_human_page_view(self.page)

            # Step 4: Click "Sell" button
            print(f"  [3/6] Clicking Sell button")

            sell_button_selectors = [
                ".tab-sell",  # Correct selector for Sell button
                "li.tab-sell",
                ".nav-item.tab-sell",
                "li.nav-item.tab-sell",
                "text=Sell",
                "button:has-text('Sell')",
                "a:has-text('Sell')"
            ]

            for selector in sell_button_selectors:
                try:
                    random_delay(0.5, 1)
                    self.page.click(selector, timeout=3000)
                    print(f"    -> Button found with selector: {selector}")
                    break
                except:
                    continue

            random_delay(2, 3.5)

            # Simulate viewing the form
            random_scroll(self.page)
            random_delay(1, 2)

            # Step 5: Fill out the form
            print(f"  [4/6] Filling out form")

            # 1. QUANTITY -> input type="number" name="amount"
            print(f"    -> Setting quantity: {card['quantity']}")
            try:
                random_delay(0.3, 0.7)
                self.page.fill('input[type="number"][name="amount"]', str(card['quantity']), timeout=3000)
                print(f"    -> Quantity filled: {card['quantity']}")
            except Exception as e:
                print(f"    [ERROR] Error filling quantity: {e}")

            random_delay(0.5, 1)

            # 2. UNIT_PRICE -> input id="price"
            print(f"    -> Setting price: {card['price']}")
            try:
                # Format price with decimal point
                price_str = str(card['price']).replace(',', '.')
                self.page.fill('input#price', price_str, timeout=3000)
                print(f"    -> Price filled: {price_str}")
            except Exception as e:
                print(f"    [ERROR] Error filling price: {e}")

            random_delay(0.5, 1)

            # 3. QUALITY
            # - NORMAL: No hacer nada
            # - HOLO: Escribir "HOLO" en observaciones
            # - REVERSE HOLO: Marcar la casilla isReverseHolo
            if card['reverse_holo']:
                print(f"    -> Checking Reverse Holo checkbox")
                try:
                    self.page.check('input[type="checkbox"][name="isReverseHolo"]', timeout=3000)
                    print(f"    -> Reverse Holo checked")
                except Exception as e:
                    print(f"    [ERROR] Could not check Reverse Holo: {e}")

            if card['comments']:  # If HOLO, write in comments
                print(f"    -> Writing comments: {card['comments']}")
                try:
                    # Try different selectors for comments field
                    comments_selectors = [
                        "input[name='comments']",
                        "textarea[name='comments']",
                        "input[name*='comment']",
                        "textarea[name*='comment']",
                        "#comments"
                    ]
                    for selector in comments_selectors:
                        try:
                            self.page.fill(selector, card['comments'], timeout=2500)
                            print(f"    -> Comments filled with selector: {selector}")
                            break
                        except:
                            continue
                except Exception as e:
                    print(f"    [ERROR] Could not fill comments: {e}")

            random_delay(0.5, 1)

            # 4. CONDITION -> select name="idCondition"
            print(f"    -> Selecting condition: {card['condition']}")
            try:
                # Exact mapping of conditions to select values
                condition_map = {
                    "Mint": "1",
                    "Near Mint": "2",
                    "Excellent": "3",
                    "Good": "4",
                    "Light Played": "5",
                    "Lightly Played": "5",
                    "Played": "6",
                    "Poor": "7"
                }

                condition_value = condition_map.get(card['condition'], None)
                if condition_value:
                    self.page.select_option('select[name="idCondition"]', value=condition_value, timeout=3000)
                    print(f"    -> Condition selected: {card['condition']} (value={condition_value})")
                else:
                    # Try by label if not in mapping
                    self.page.select_option('select[name="idCondition"]', label=card['condition'], timeout=3000)
                    print(f"    -> Condition selected by label: {card['condition']}")
            except Exception as e:
                print(f"    [ERROR] Error selecting condition: {e}")

            random_delay(0.5, 1)

            # 5. LANGUAGE -> select name="idLanguage"
            # Los idiomas pueden ir tanto en español como en inglés
            print(f"    -> Selecting language: {card['language']}")
            try:
                # Exact mapping of languages to select values (English and Spanish)
                lang_map = {
                    # English
                    "English": "1",
                    "French": "2",
                    "German": "3",
                    "Spanish": "4",
                    "Italian": "5",
                    "Portuguese": "8",
                    "Japanese": "7",
                    "Korean": '10',
                    # Español
                    "Inglés": "1",
                    "Francés": "2",
                    "Alemán": "3",
                    "Español": "4",
                    "Italiano": "5",
                    "Portugués": "8",
                    "Coreano": "10",
                    "Japonés": "7"
                }

                lang_value = lang_map.get(card['language'], None)
                if lang_value:
                    self.page.select_option('select[name="idLanguage"]', value=lang_value, timeout=3000)
                    print(f"    -> Language selected: {card['language']} (value={lang_value})")
                else:
                    # Try by label if not in mapping
                    self.page.select_option('select[name="idLanguage"]', label=card['language'], timeout=3000)
                    print(f"    -> Language selected by label: {card['language']}")
            except Exception as e:
                print(f"    [ERROR] Error selecting language: {e}")

            # Step 6: Click "Poner en venta" button
            print(f"  [5/6] Putting up for sale")

            # Pause as if reviewing the form
            random_delay(1.5, 3)
            random_scroll(self.page)

            # Exact selector for the submit button
            # <input type="submit" value="Poner en venta" title="Poner en venta" class="btn btn-primary btn-sm">
            try:
                random_delay(0.5, 1)
                self.page.click('input[type="submit"][value="Poner en venta"]', timeout=3000)
                print(f"    -> Submit button clicked")
            except Exception as e:
                print(f"    [ERROR] Could not click submit button: {e}")
                # Try alternative selector as fallback
                try:
                    self.page.click('input[type="submit"].btn-primary.btn-sm', timeout=2500)
                    print(f"    -> Submit button clicked (fallback selector)")
                except Exception as e2:
                    print(f"    [ERROR] Fallback also failed: {e2}")

            random_delay(2, 4)

            # Add extra randomness occasionally
            add_human_randomness()

            print(f"  [6/6] Card added successfully")

        except Exception as e:
            print(f"  [ERROR] Error adding card: {e}")
            raise

    def upload_cards(self, csv_path):
        """Complete card upload process"""
        cards = self.parse_csv(csv_path)

        print("\n" + "=" * 60)
        print(f"UPLOADING {len(cards)} CARDS - {self.mode.upper()} MODE")
        print("=" * 60)
        print(f"[INFO] Long pause every {self.delay_settings['break_interval']} cards")
        print(f"[INFO] Delay between cards: {self.delay_settings['between_cards'][0]}-{self.delay_settings['between_cards'][1]}s")
        print("=" * 60)

        successful = 0
        failed = 0

        for i, card in enumerate(cards, 1):
            print(f"\n[{i}/{len(cards)}] {card['code']}")

            # Check if we need a long pause
            if should_take_long_break(successful, self.delay_settings['break_interval']):
                extra_long_pause(
                    self.delay_settings['break_duration'][0],
                    self.delay_settings['break_duration'][1]
                )

            try:
                self.add_card(card)
                successful += 1

                # Long delay between cards to avoid rate-limiting
                if i < len(cards):  # Don't wait after last card
                    min_delay, max_delay = self.delay_settings['between_cards']
                    long_random_delay(min_delay, max_delay)

            except Exception as e:
                print(f"  [ERROR] Error adding card: {e}")
                failed += 1

                # Ask whether to continue
                try:
                    continue_input = input("\n  Continue with next card? (y/n): ").strip().lower()
                    if continue_input != 'y':
                        print("\n[INFO] Process stopped by user")
                        break
                except EOFError:
                    # If no interactive terminal, continue automatically
                    print("\n  [AUTO] Continuing with next card...")
                    time.sleep(2)

        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total processed: {successful + failed}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print("=" * 60)

    def stop(self):
        """Closes the browser"""
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()
        print("[OK] Browser closed")


def main():
    import sys
    import os

    print("=" * 60)
    print("CARDMARKET BOT - AUTOMATIC CARD UPLOAD")
    print("=" * 60)

    if len(sys.argv) < 2:
        print("\n[ERROR] Missing CSV file")
        print("\nUsage: python cardmarket_bot.py <csv_path>")
        print("Example: python cardmarket_bot.py example_cards.csv")
        sys.exit(1)

    csv_path = sys.argv[1]

    # Verify file exists
    if not os.path.exists(csv_path):
        print(f"\n[ERROR] File not found: {csv_path}")
        sys.exit(1)

    # Mode: 'fast', 'balanced', 'safe'
    # balanced = recommended (delays 20-45s, pause every 8 cards)
    bot = CardmarketBot(headless=False, mode='balanced')

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
