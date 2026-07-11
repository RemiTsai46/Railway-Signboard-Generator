from PIL import Image,ImageColor,ImageDraw
from PIL._typing import Coords
from typing import *
from math import *

def stripes(
    im: Image.Image,
    xy: Coords,
    colors: list = None,
    direction: str = 'h',
    anchor: str = 'm',
    width: int = 4,
    single_width: int = 6,
    max_ttl_width: int | None = None
) -> None:
    """
    Draw multiple lines at the same time.
    Horizontal mode draws from the upper to the lower.
    Vertical mode draws from the left to the right.

    :param im: The image to draw on.
    :param xy: Coords to draw on, note that  
        **horizontal** mode requires **y0 == y1**; 
        **vertical** mode requires **x0 == x1**.
    :param colors: List of colors to be drawn.
    :param direction: Whether to draw stripes horizontally or vertically. Defaults to `\'h\'`
    :param anchor: Anchor of the stripe object.
        **horizontal** mode supports `t`, `m` and `b`
        **vertical** mode supports `l`, `m` and `r`
        Defaults to `m`.
    :param width: Width of each stripe. Defaults to `4`.
    :param single_width: Width of a stripe when there's only 1 color. Defaults to `6`
    :param max_ttl_width: Maximum total width of stripes.
        If exceeded, the stripes will be compressed to fit the size.
        Colors may be indistinguishable if too many colors are given. Defaults to `None`
    """

    # anchor l m r, ask stripes from and to ('h' ask x, 'v' ask y)
    # ask anchor pos('h' ask y, 'v' ask x) throw error if 2 of them not the same

    # var init
    if isinstance(xy[0], (list, tuple)):
        (x0, y0), (x1, y1) = cast(Sequence[Sequence[float]], xy)
    else:
        x0, y0, x1, y1 = cast(Sequence[float], xy)

    # bad value handler
    msg = None
    if not (direction == 'h' or direction == 'v'):
        msg = f"bad direction specified: {direction}"
    
    if direction == 'h':
        x0 = int(x0); x1 = int(x1) # fixed int stripe length
        if y0 != y1:
            msg = "y1 must be equal to y0 in horizontal stripes"
        if x1 < x0:
            msg = "x1 must be greater than or equal to x0 in horizontal stripes"
        if anchor not in ['t','m','b']:
            msg = f"bad anchor specified: {anchor}"
    if direction == 'v':
        y0 = int(y0); y1 = int(y1) # fixed int stripe length
        if x1 != x0:
            msg = "x1 must be equal to x0 in vertical stripes"
        if y1 < y0:
            msg = "y1 must be greater than or equal to y0 in vertical stripes"
        if anchor not in ['l','m','r']:
            msg = f"bad anchor specified: {anchor}"

    if single_width > max_ttl_width:
        msg = "single_width must be less than or equal to max_ttl_width"
        
    if msg != None:
        raise ValueError(msg)
    
    # VAR INIT
    
    cnt = len(colors)
    colors.append("#00000000")

    # switch if horizontal for optimising(ix is ptr, iy fixed width)
    # if direction == 'h': ix0,ix1,iy0,iy1 = y0,y1,x0,x1 # if horizontal iy is x
    # else: ix0,ix1,iy0,iy1 = x0,x1,y0,y1

    # Width calc
    if max_ttl_width == None: max_ttl_width = width*cnt  
    if width*cnt > max_ttl_width: width = (max_ttl_width/cnt)
    wd = min(width*cnt,max_ttl_width)
    if cnt == 1:
        wd = single_width
        width = single_width

    # Anchor calc
    # anchor in ['t','l'] pass
    if direction == 'h':
        if anchor == 'm':
            y0 -= wd/2
        elif anchor == 'b':
            y0 -= wd
    else:
        if anchor == 'm':
            x0 -= wd/2
        elif anchor == 'r':
            x0 -= wd

    l,r = -1,-1

    if direction == 'h':
        X_SIZE,Y_SIZE = x1-x0+1,ceil(wd)+1
        ix0,ix1 = 0,X_SIZE-1
        iy0,iy1 = l,r
        split = y0-floor(y0)
    else:
        X_SIZE,Y_SIZE = ceil(wd)+1,y1-y0+1
        ix0,ix1 = l,r
        iy0,iy1 = 0,Y_SIZE-1
        split = x0-floor(x0)

    icoords = [ix0,iy0,ix1,iy1]

    print(x0,y0)

    print(X_SIZE,Y_SIZE)
    imstrp = Image.new("RGBA",(X_SIZE,Y_SIZE),"#00000000")
    drawstrp = ImageDraw.Draw(imstrp)

    def color_calc(c1, c2, a): # a 0 prev 1 next
        if a == 0: return c1
        # a == 1 impossible

        r1,g1,b1,a1 = ImageColor.getcolor(c1, "RGBA")
        r2,g2,b2,a2 = ImageColor.getcolor(c2, "RGBA")

        w1 = a1*a
        w2 = a2*a
        wt = w1+w2

        r = (r1*w1 + r2*w2)/wt
        g = (g1*w1 + g2*w2)/wt
        b = (b1*w1 + b2*w2)/wt
        a = wt

        return (int(r),int(g),int(b),int(a))

    def move_lr(l,r,ic):
        if direction == 'h':
            ic[1],ic[3] = l,r
        else:
            ic[0],ic[2] = l,r
        # print(icoords)

    c = 0 # color ptr
    print(cnt,wd)
    for i in range(0,ceil(wd)+1):
        if i <= split < i+1:
            # draw plain color
            if l <= r and l>=0 and r>=0:
                drawstrp.rectangle(icoords,fill=colors[c-1])
            
            l=i;r=i
            move_lr(l,r,icoords)
            if split != floor(split):
                color = color_calc(colors[c-1],colors[c],split-floor(split))
                drawstrp.rectangle(icoords,fill=color)
                l+=1;r+=1
                move_lr(l,r,icoords)

            print(c, split, split+width)
            c+=1
            split += width
        else:
            r+=1
            move_lr(l,r,icoords)

    x0,y0 = int(x0),int(y0)

    # imstrp.save("outputstr.png")
    
    print(x0,y0)
    im.alpha_composite(imstrp,(x0,y0))

# ===================================



# ===================================

im = Image.new('RGBA',(64,64),"#FFFFFF")
draw = ImageDraw.Draw(im)

colors = ["#FF0000"] #,"#00FF00","#0000FF","#FF00FF","#00FFFF","#FFFF00","#FF9900"
stripes(im,[27,32,36,32],colors=colors,direction='h',anchor='m',width=4,single_width=6,max_ttl_width=24)
im.show()
im.save("output2.png")

# im = Image.new('RGBA',(9,9),"#00000000")
# draw = ImageDraw.Draw(im)

# draw.rectangle([0,0,2,9],"#F00")
# draw.rectangle([3,0,5,9],"#0F0")
# draw.rectangle([6,0,8,9],"#00F")

# ims2 = Image.new('RGBA',(10,9),"#00000000")
# ims3 = ims2.copy()

# ims2.paste(ims,(0,0))
# ims3.paste(ims,(1,0))

# ims2 = Image.blend(ims2,ims3,0.8) # 1 is right, 0 is left
# ims2.save("output2.png")