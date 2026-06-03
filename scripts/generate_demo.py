#!/usr/bin/env python3
"""Generate cyberpunk demo image for CYBER SH"""
from PIL import Image, ImageDraw

width, height = 1280, 720
image = Image.new('RGB', (width, height), (10, 10, 20))
draw = ImageDraw.Draw(image)

cyan = (0, 255, 255)
magenta = (255, 0, 255)
green = (0, 255, 100)
white = (255, 255, 255)

# Grid background
for i in range(0, width, 40):
    draw.line([(i, 0), (i, height)], fill=(30, 30, 50), width=1)

# Title
draw.text((20, 40), "CYBER SH", fill=magenta)
draw.text((20, 95), "Offline AI CLI - Security Researchers & Developers", fill=cyan)

# Badges
badges = ["Python 3.10+", "100% Offline", "No API Keys", "Local GGUF", "Pure Python"]
for i, badge in enumerate(badges):
    x = 20 + (i * 240)
    draw.rectangle([(x, 150), (x + 230, 185)], fill=(30, 30, 50), outline=cyan, width=2)
    draw.text((x + 10, 158), badge, fill=cyan)

# Console window
draw.rectangle([(20, 210), (1260, 590)], fill=(15, 15, 25), outline=green, width=3)
draw.rectangle([(20, 210), (1260, 240)], fill=(20, 60, 40))
draw.text((30, 218), "$ cyber-sh --agent", fill=green)

# Console output
output = [
    "  Initializing CYBER SH v1.0...",
    "  Model: Qwen2.5-1.5B loaded",
    "  [AGENT MODE] Ready for commands",
    "  > analyze target.txt for vulnerabilities",
    "  SQL injection detected - 3 points",
    "  Weak crypto usage found",
    "  Exploit payloads generated",
]

y = 260
for line in output:
    draw.text((30, y), line, fill=white)
    y += 30

# Features footer
draw.text((20, 620), "Agent | Sec | Vibe | Code | Chat", fill=magenta)
draw.text((20, 660), "No internet - No servers - No API keys - Pure local AI", fill=(100, 100, 120))

image.save('assets/demo.png')
print("Generated assets/demo.png successfully!")
