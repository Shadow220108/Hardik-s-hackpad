import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB, AnimationModes

# Initialize the Keyboard
keyboard = KMKKeyboard()

# --- HARDWARE CONFIGURATION ---

# 1. SWITCH MATRIX
# Update these pins to match your KiCad Routing!
# Based on our design:
keyboard.col_pins = (board.D2, board.D3, board.D4, board.D5) # Columns
keyboard.row_pins = (board.D0, board.D1)                     # Rows
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# 2. ROTARY ENCODER
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)
# Pin A = D9, Pin B = D10 (Check your schematic!)
encoder_handler.pins = ((board.D9, board.D10, None, False),)

# 3. RGB LEDS (Underglow)
rgb = RGB(
    pixel_pin=board.D8,    # Where your LED Data In is connected
    num_pixels=8,          # You have 8 LEDs
    val_limit=100,         # Brightness limit (max 255)
    hue_default=0,
    sat_default=255,
    val_default=100,
    animation_mode=AnimationModes.RAINBOW
)
keyboard.extensions.append(rgb)

# 4. MODULES
keyboard.modules.append(Layers())
keyboard.extensions.append(MediaKeys())

# --- KEYMAPS ---

# Define special keys
# MO(1) means "Momentary Layer 1" - hold to switch layers
L1_KEY = KC.MO(1)

# Layer 0: Normal Shortcuts (Copy, Paste, Save, etc.)
# Layer 1: Media Control (Volume, Play/Pause)

keyboard.keymap = [
    # LAYER 0 (Default)
    [
        KC.A,    KC.B,     KC.C,     KC.D,
        KC.E,    KC.F,     KC.G,     L1_KEY, # Bottom right key switches layers
    ],
    # LAYER 1 (Held down)
    [
        KC.N1,   KC.N2,    KC.N3,    KC.N4,
        KC.MUTE, KC.VOLU,  KC.VOLD,  KC.TRNS,
    ]
]

# --- ENCODER MAP ---
# [Layer 0 behavior, Layer 1 behavior]
encoder_handler.map = [
    ((KC.VOLU, KC.VOLD, KC.MUTE),), # Layer 0: Vol Up, Vol Down, Mute(if clicked)
    ((KC.UP,   KC.DOWN, KC.ENT),),  # Layer 1: Arrow Up, Arrow Down, Enter
]

if __name__ == '__main__':
    keyboard.go()