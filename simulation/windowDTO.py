from dataclasses import dataclass

@dataclass
class WindowProperties:
    # Window size
    WIN_W: int = 1280
    WIN_H: int = 720

    # Colours
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 192, 203)