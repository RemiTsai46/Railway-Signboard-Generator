from PIL import ImageFont

lineDir = {
    "e":["東","East"],
    "w":["西","West"],
    "n":["北","North"],
    "s":["南","South"],
    "cw":["順時針","CW"],
    "ccw":["逆時針","CCW"]
    }

fontPads = {
    "resources/fonts/arial.ttf":[-0.06,0.12],
    "resources/fonts/arialn.ttf":[-0.1,0.1],
    "resources/fonts/msjh.ttf":[-0.1,0.1],
}


SAP_posSet = [
    [[106,119,117]],
    [[104, 113, 112],[116, 125, 124]]
]

RTSAE_posSet = [
    [87,97,96],[100,110,109],[113,123,122]
]