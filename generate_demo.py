#!/usr/bin/env python3
"""
Generate a professional cyberpunk-styled demo image for CYBER SH
"""
from PIL import Image, ImageDraw

# Create image
width, height = 1280, 720
image = Image.new('RGB', (width, height), (10, 10, 20))
draw = ImageDraw.Draw(image, 'RGBA')

# Cyberpunk colors
cyan = (0, 255, 255)
magenta = (255, 0, 255)
green = (0, 255, 100)
red = (255, 50, 100)
yellow = (255, 255, 0)
white = (255, 255, 255)
dark = (15, 15, 25)

# Grid background
for i in range(0, width, 40):
    draw.line([(i, 0), (i, height)], fill=(30, 30, 50, 100), width=1)
for i in range(0, height, 40):
    draw.line([(0, i), (width, i)], fill=(30, 30, 50, 100), width=1)

# Title with glow effect
title = "CYBER SH"
draw.text((20, 40), title, fill=magenta, font=None)
draw.text((20, 95), "Offline AI CLI • Security Researchers & Developers", fill=cyan, font=None)

# Badges
badges_y = 150
badges = ["🐍 Python 3.10+", "🔒 100% Offline", "⚡ No API Keys", "🚀 Local GGUF", "💻 Pure Python"]
for i, badge in enumerate(badges):
    x = 20 + (i * 240)
    draw.rectangle([(x, badges_y), (x + 230, badges_y + 35)], fill=(30, 30, 50), outline=cyan, width=2)
    draw.text((x + 10, badges_y + 8), badge, fill=cyan, font=None)

# Console mockup
console_y = 210
console_x = 20
console_w = width - 40
console_h = 380

draw.rectangle([(console_x, console_y), (console_x + console_w, console_y + console_h)],
               fill=dark, outline=green, width=3)
draw.rectangle([(console_x, console_y), (console_x + console_w, console_y + 30)],
               fill=(20, 60, 40), outline=green, width=1)
draw.text((console_x + 10, console_y + 8), "$ cyber-sh --agent", fill=green, font=None)

# Console text
lines = [
    ("  ⚡ Initializing CYBER SH v1.0 ...", white),
    ("  🔌 Model: Qwen2.5-1.5B loaded", white),
    ("  🧠 Context: 4096 tokens | Threads: 12", white),
    ("  ", white),
    ("  [AGENT MODE] - What would you like?", yellow),
    ("  ", white),
    ("  > analyze /home/user/target.txt for vulns", yellow),
    ("  🔍 Scanning...", cyan),
    ("  ✓ Found 3 SQL injection points", green),
    ("  ✓ Weak cryptography detected", red),
    ("  ✓ Generated exploit payloads", green),
]

text_y = console_y + 50
for line, color in lines:
    draw.text((console_x + 15, text_y), line, fill=color, font=None)
    text_y += 28

# Features footer
features_y = console_y + console_h + 20
draw.text((console_x, features_y), "🤖 Agent  |  🔐 Sec  |  ✨ Vibe  |  💾 Code  |  💬 Chat", 
          fill=magenta, font=None)

# Info footer
draw.text((console_x, features_y + 40), "No internet • No servers • No data tracking • Pure local AI power", 
          fill=(100, 100, 120), font=None)

image.save('demo_preview.png')
print("✓ Demo image created: demo_preview.png")
