from typing import Callable, Tuple

from PIL import Image
from PIL import ImageDraw


def save_asset(func) -> Callable:
    def deco(*args, filename: str, **kwargs) -> Image.Image:
        ret = func(*args, **kwargs)
        ret = ret.resize((24, 24))
        ret.save("../assets/" + filename)
        return ret

    return deco


@save_asset
def _pacman_open(rotate: int = 0) -> Image.Image:
    im = Image.new("RGBA", (50, 50))
    actual_pacman = Image.new("RGBA", (50, 50))
    draw = ImageDraw.Draw(actual_pacman)
    draw.pieslice(((0.0, 0.0), (50.0, 50.0)), 45, 360 - 45, (255, 251, 0))
    actual_pacman = actual_pacman.rotate(rotate)
    
    actual_pacman = actual_pacman.resize((40, 40))
    im.paste(actual_pacman, (5, 5))
    return im


@save_asset
def _pacman_closed() -> Image.Image:
    im = Image.new("RGBA", (50, 50))
    actual_pacman = Image.new("RGBA", (50, 50))
    draw = ImageDraw.Draw(actual_pacman)
    draw.ellipse([0, 0, 50, 50], fill=(255, 251, 0))
    actual_pacman = actual_pacman.resize((40, 40))
    im.paste(actual_pacman, (5, 5))
    return im


@save_asset
def _ghost(colour: Tuple[int, int, int]) -> Image.Image:
    im = Image.new("RGBA", (50, 50))
    draw = ImageDraw.Draw(im)
    draw.pieslice(((0.0, 0.0), (50.0, 50.0)), 180, 0, fill=colour)
    draw.rectangle((0.0, 25.0, 50.0, 40.0), fill=colour)

    for i in (10, 30):
        draw.ellipse([i, 15, i + 10, 25], fill=(255, 255, 255))
        draw.ellipse([i + 2, 17, i + 8, 23], fill=(0, 72, 255))

    for i in range(1, 4):
        points = [
            (i * (50 / 3) - 50 / 3, 40),
            (i * (50 / 3), 40),
            (i * (50 / 3) - 50 / 3 / 2, 50),
        ]
        # maths which spits out a triangle
        draw.polygon(points, fill=colour)

    return im


@save_asset
def _wall() -> Image.Image:
    im = Image.new("RGBA", (50, 50))
    draw = ImageDraw.Draw(im)
    draw.rectangle(
        (2.0, 2.0, 48.0, 48.0), outline=(18, 50, 239), width=5, fill=(0, 0, 0)
    )
    return im


@save_asset
def _coin() -> Image.Image:
    im = Image.new("RGBA", (50, 50), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    draw.rectangle((21.0, 21.0, 29.0, 29.0), fill=(255, 255, 255))
    im = im.rotate(45)

    return im


@save_asset
def _blank() -> Image.Image:
    im = Image.new("RGBA", (50, 50), (0, 0, 0))
    return im


if __name__ == "__main__":
    # automatically save all the images if we run the file

    _pacman_open(filename="pacman_open_right.png")
    _pacman_open(180, filename="pacman_open_left.png")
    _pacman_open(270, filename="pacman_open_down.png")
    _pacman_open(90, filename="pacman_open_up.png")

    _pacman_closed(filename="pacman_closed.png")

    _ghost((255, 49, 0), filename="ghost_red.png")
    _ghost((255, 204, 0), filename="ghost_orange.png")
    _ghost((0, 252, 255), filename="ghost_blue.png")
    _ghost((254, 171, 210), filename="ghost_pink.png")

    _wall(filename="wall.png")
    _coin(filename="coin.png")
    _blank(filename="blank.png")
