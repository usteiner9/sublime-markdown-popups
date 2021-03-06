"""
Image tinting.

Licensed under MIT
Copyright (c) 2015 - 2016 Isaac Muse <isaacmuse@gmail.com>
"""
from .png import Reader, Writer
from .rgba import RGBA
import base64
import io


def tint_raw(byte_string, color, opacity=255):
    """Tint the image and return a byte string."""

    # Read the byte string as a RGBA image.
    width, height, pixels, meta = Reader(bytes=byte_string).asRGBA()

    # Clamp opacity
    if opacity < 0:
        opacity = 0
    elif opacity > 255:
        opacity = 255

    # Tint
    p = []
    y = 0
    for row in pixels:
        p.append([])
        columns = int(len(row) / 4)
        start = 0
        for x in range(columns):
            rgba = RGBA(color)
            rgba.a = opacity
            rgba.apply_alpha(background='#%02X%02X%02XFF' % tuple(row[start:start + 3]))
            p[y] += [rgba.r, rgba.g, rgba.b, row[start + 3]]
            start += 4
        y += 1

    # Create bytes buffer for PNG
    with io.BytesIO() as f:

        # Write out PNG
        img = Writer(width, height, alpha=True)
        img.write(f, p)

        # Read out PNG bytes and base64 encode
        f.seek(0)

        return f.read()


def tint(byte_string, color, opacity=255, height=None, width=None):
    """Base64 encode the tint."""

    style = ''
    if width:
        style = 'style="width: %dpx;"' % width
    if height is not None and style is None:
        style = 'style="height: %dpx;"' % width
    elif height is not None:
        style = style[:-1] + (' height: %dpx;" ' % height)

    return "<img %ssrc=\"data:image/png;base64,%s\">" % (
        style,
        base64.b64encode(tint_raw(byte_string, color, opacity)).decode('ascii')
    )
