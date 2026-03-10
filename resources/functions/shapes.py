from PIL import Image,ImageDraw
from PIL._typing import Coords
from typing import *

def circle(
        im:Image.Image,
        xy:Sequence[float],
        radius:float,
        fill=None,
        outline=None,
        width=1
    ) -> None:
    # return if no color
    if fill == None and outline == None:
        return
    
    #var init
    x0,y0,x1,y1 = (xy[0] - radius, xy[1] - radius, xy[0] + radius, xy[1] + radius)

    print("Four corners:",x0,y0,x1,y1)
    
    W = int(x1 - x0 + 1)
    H = int(y1 - y0 + 1)
    color = Image.new('RGBA', (W*4,H*4), outline)
    color_draw = ImageDraw.Draw(color)
    #main
    if outline == None:
        color_draw.rectangle([0,0,W*4-1,H*4-1],fill=fill)
    else:
        color_draw.ellipse([0,0,W*4-1,H*4-1],fill=fill,outline=outline,width=width*4)
    color = color.resize((W,H),Image.Resampling.BICUBIC)

    #overlay var init
    circle = Image.new('RGBA', (W*4,H*4), (0, 0, 0, 0))
    circle_draw = ImageDraw.Draw(circle)
    #overlay main
    if fill == None:
        circle_draw.ellipse([0,0,W*4-1,H*4-1],outline="#ffffff",width=width*4)
    else:
        circle_draw.ellipse([0,0,W*4-1,H*4-1],fill="#ffffff")
    circle = circle.resize((W,H),Image.Resampling.BICUBIC)

    im.paste(color,(int(x0),int(y0)),circle)
        
def ellipse(
        im:Image.Image,
        xy:Coords,
        fill=None,
        outline=None,
        width=1
    ) -> None:
    # return if no color
    if fill == None and outline == None:
        return
    
    #var init
    if isinstance(xy[0], (list, tuple)):
        (x0, y0), (x1, y1) = cast(Sequence[Sequence[float]], xy)
    else:
        x0, y0, x1, y1 = cast(Sequence[float], xy)
    if x1 < x0:
        msg = "x1 must be greater than or equal to x0"
        raise ValueError(msg)
    if y1 < y0:
        msg = "y1 must be greater than or equal to y0"
        raise ValueError(msg)
    
    W = int(x1 - x0 + 1)
    H = int(y1 - y0 + 1)
    color = Image.new('RGBA', (W*4,H*4), outline)
    color_draw = ImageDraw.Draw(color)
    #main
    if outline == None:
        color_draw.rectangle([0,0,W*4-1,H*4-1],fill=fill)
    else:
        color_draw.ellipse([0,0,W*4-1,H*4-1],fill=fill,outline=outline,width=width*4)
    color = color.resize((W,H),Image.Resampling.BOX)

    #overlay var init
    ellipse = Image.new('RGBA', (W*4,H*4), (0, 0, 0, 0))
    elli_draw = ImageDraw.Draw(ellipse)
    #overlay main
    if fill == None:
        elli_draw.ellipse([0,0,W*4-1,H*4-1],outline="#ffffff",width=width*4)
    else:
        elli_draw.ellipse([0,0,W*4-1,H*4-1],fill="#ffffff")
    ellipse = ellipse.resize((W,H),Image.Resampling.BOX)

    im.paste(color,(int(x0),int(y0)),ellipse)
        
def roundRect(
    im: Image.Image,
    xy: Coords,
    radius: float = 0,
    fill=None,
    outline=None,
    width: int = 1,
    corners: tuple[bool, bool, bool, bool] | None = None
    ) -> None:
    
    #return if no color
    if fill == None and outline == None:
        return

    #var init
    if isinstance(xy[0], (list, tuple)):
        (x0, y0), (x1, y1) = cast(Sequence[Sequence[float]], xy)
    else:
        x0, y0, x1, y1 = cast(Sequence[float], xy)
    if x1 < x0:
        msg = "x1 must be greater than or equal to x0"
        raise ValueError(msg)
    if y1 < y0:
        msg = "y1 must be greater than or equal to y0"
        raise ValueError(msg)
    if corners is None:
        corners = (True, True, True, True)
    
    print(x0,y0,x1,y1)
    
    W = int(x1 - x0 + 1)
    H = int(y1 - y0 + 1)
    color = Image.new('RGBA', (W*4,H*4), outline)
    color_draw = ImageDraw.Draw(color)
    #main
    if outline == None:
        color_draw.rectangle([0,0,W*4-1,H*4-1],fill=fill)
    else:
        color_draw.rounded_rectangle(
            [0,0,W*4-1,H*4-1],
            radius=radius*4,
            fill=fill,
            outline=outline,
            width=width*4,
            corners=corners
        )
    color = color.resize((W,H),Image.Resampling.BOX)

    #overlay var init
    rectangle = Image.new('RGBA', (W*4,H*4), (0, 0, 0, 0))
    rect_draw = ImageDraw.Draw(rectangle)
    #overlay main
    if fill == None:
        rect_draw.rounded_rectangle(
            [0,0,W*4-1,H*4-1],
            radius=radius*4,
            outline="#ffffff",
            width=width*4,
            corners = corners
            )
    else:
        rect_draw.rounded_rectangle(
            [0,0,W*4-1,H*4-1],
            radius=radius*4,
            fill="#ffffff",
            corners = corners
        )
    rectangle = rectangle.resize((W,H),Image.Resampling.BOX)

    im.paste(color,(int(x0),int(y0)),rectangle)

def stripes(
    im:Image.Image,
    direction:str,
    xy:Coords,
    colors: list = None,
    width: int = 4,
    single_width: int = 6,
    max_ttl_width: int | None = None
) -> None:
    """
    Draw multiple lines at the same time.
    Horizontal mode draws from upper to lower.
    Vertical mode draws from left to right.
    """

    # tba param description
    # direction make ValueError: bad direction specified: {direction}
    # anchor l m r, ask stripes from and to ('h' ask x, 'v' ask y)
    # ask anchor pos('h' ask y, 'v' ask x) throw error if 2 of them not the same

    # var init

    if isinstance(xy[0], (list, tuple)):
        (x0, y0), (x1, y1) = cast(Sequence[Sequence[float]], xy)
    else:
        x0, y0, x1, y1 = cast(Sequence[float], xy)

    # bad value handler
    if not (direction == 'h' or direction == 'v'):
        msg = f"bad direction specified: {direction}"
        raise ValueError(msg)

    if x1 < x0:
        if direction == "h":
            msg = "x1 must be greater than or equal to x0 in horizontal stripes"
        else:
            msg = "x1 must be equal to x0 in vertical stripes"
        raise ValueError(msg)
    if y1 < y0:
        if direction == "v":
            msg = "y1 must be greater than or equal to y0 in vertical stripes"
        else:
            msg = "y1 must be equal to y0 in horizontal stripes"
        raise ValueError(msg)
    
    
    if direction == 'h':
        if y0 != y1:
            msg = "y1 must be equal to y0 in horizontal stripes"