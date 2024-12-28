from main.constants import *

def fit_text(text, width=SCREEN_WIDTH-32):
    max_char = int(width / FONT_WIDTH)

    words = iter(text.split())
    lines, current = [], next(words)
    for word in words:
        if len(current) + 1 + len(word) > max_char:
            lines.append(current)
            current = word
        else:
            current += " " + word
    lines.append(current)
    return lines
