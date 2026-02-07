"""
Human behavior simulation to avoid detection
"""
import random
import time


def random_delay(min_seconds=2, max_seconds=5):
    """Random wait between min and max seconds"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    return delay


def long_random_delay(min_seconds=20, max_seconds=60):
    """Long random wait to appear human between operations"""
    delay = random.uniform(min_seconds, max_seconds)
    print(f"  [HUMAN PAUSE] Waiting {delay:.1f} seconds...")
    time.sleep(delay)
    return delay


def extra_long_pause(min_minutes=3, max_minutes=5):
    """Very long pause between card batches"""
    minutes = random.uniform(min_minutes, max_minutes)
    seconds = minutes * 60
    print(f"\n  [LONG PAUSE] Resting {minutes:.1f} minutes to avoid rate-limit...")
    print(f"  (Cloudflare resets limits during this time)")

    # Show countdown
    for remaining in range(int(seconds), 0, -30):
        mins = remaining // 60
        secs = remaining % 60
        print(f"  Time remaining: {mins}m {secs}s", end='\r')
        time.sleep(min(30, remaining))

    print("\n  [OK] Pause completed, continuing...")
    return seconds


def random_scroll(page):
    """Random scroll on page to appear human"""
    try:
        # Random scroll down
        scroll_amount = random.randint(100, 500)
        page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        time.sleep(random.uniform(0.3, 0.8))

        # Sometimes scroll up
        if random.random() > 0.7:
            scroll_up = random.randint(50, 200)
            page.evaluate(f"window.scrollBy(0, -{scroll_up})")
            time.sleep(random.uniform(0.2, 0.5))
    except:
        pass  # If it fails, no problem


def random_mouse_movement(page):
    """Simulates random mouse movements"""
    try:
        # Move mouse to random positions
        for _ in range(random.randint(1, 3)):
            x = random.randint(200, 1200)
            y = random.randint(200, 800)
            page.mouse.move(x, y)
            time.sleep(random.uniform(0.1, 0.3))
    except:
        pass  # If it fails, no problem


def human_like_typing(element, text):
    """Types text with variable speed like a human"""
    try:
        element.click()
        time.sleep(random.uniform(0.1, 0.3))

        for char in text:
            element.type(char)
            # Random delay between keys (50-200ms)
            time.sleep(random.uniform(0.05, 0.2))
    except:
        # Fallback to normal fill if it fails
        element.fill(text)


def random_read_pause():
    """Pause as if reading the page"""
    pause = random.uniform(1, 3)
    time.sleep(pause)
    return pause


def should_take_long_break(cards_processed, break_interval=8):
    """
    Determines if a long pause should be taken

    Args:
        cards_processed: Number of cards processed
        break_interval: How often to pause

    Returns:
        bool: True if should pause
    """
    return cards_processed > 0 and cards_processed % break_interval == 0


def simulate_human_page_view(page):
    """
    Simulates a human viewing the page
    Combines scroll, mouse movement and pauses
    """
    print("  [SIMULATING HUMAN] Viewing page...")

    # Random scroll
    random_scroll(page)

    # Pause as if reading
    random_read_pause()

    # Mouse movement
    random_mouse_movement(page)

    # Another short pause
    time.sleep(random.uniform(0.5, 1.5))


def add_human_randomness():
    """
    Adds extra randomness occasionally
    Simulates human distractions
    """
    # 20% chance of extra pause (as if distracted)
    if random.random() < 0.2:
        distraction = random.uniform(3, 8)
        print(f"  [HUMAN DISTRACTION] Pause of {distraction:.1f}s")
        time.sleep(distraction)
        return True
    return False


def get_delay_settings(mode='balanced'):
    """
    Returns delay configuration according to mode

    Modes:
    - 'fast': Faster, more detection risk
    - 'balanced': Balance between speed and security (recommended)
    - 'safe': Very slow, maximum security
    """
    settings = {
        'fast': {
            'between_cards': (10, 20),
            'break_interval': 15,
            'break_duration': (2, 3),
        },
        'balanced': {
            'between_cards': (17, 37),
            'break_interval': 8,
            'break_duration': (3, 5),
        },
        'safe': {
            'between_cards': (40, 90),
            'break_interval': 5,
            'break_duration': (5, 8),
        }
    }

    return settings.get(mode, settings['balanced'])
