"""
Bot Configuration

Adjust these parameters according to your needs
"""

# ==========================================
# OPERATION MODE
# ==========================================
# 'fast': Faster but higher risk of captcha
#   - Delays: 10-20s between cards
#   - Pause every 15 cards (2-3 minutes)
#
# 'balanced': Balance between speed and security (RECOMMENDED)
#   - Delays: 17-37s between cards
#   - Pause every 8 cards (3-5 minutes)
#
# 'safe': Very slow but minimum risk of captcha
#   - Delays: 40-90s between cards
#   - Pause every 5 cards (5-8 minutes)
#
BOT_MODE = 'balanced'


# ==========================================
# CUSTOM CONFIGURATION (ADVANCED)
# ==========================================
# If you want to manually adjust timings, uncomment and modify:

# CUSTOM_SETTINGS = {
#     'between_cards': (30, 60),    # (min, max) seconds between each card
#     'break_interval': 10,          # How often to take a long pause
#     'break_duration': (4, 6),     # (min, max) minutes of long pause
# }


# ==========================================
# STEALTH MODE
# ==========================================
# Anti-detection techniques (don't change unless you know what you're doing)
STEALTH_ENABLED = True


# ==========================================
# DEBUG
# ==========================================
# Show debug messages
DEBUG = False
