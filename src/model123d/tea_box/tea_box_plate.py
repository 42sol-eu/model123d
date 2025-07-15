#%%
from build123d import *
from ocp_vscode import show
from copy import copy
#%%

thickness = 3.12
slotThickness = thickness - .08

modulesX = 6
modulesY = 6

moduleWidth = 100
moduleDepth = 80

inWidth = modulesX*moduleWidth + thickness*(modulesX-1)
inDepth = modulesY*moduleDepth + thickness*(modulesY-1)
inHeight = 120

wallHeight = 100

slotsX = 6
slotsY = 6
slotLength = 25

with BuildPart() as Bottom:
    with BuildSketch() as bottom:
        bottomBaseW = inWidth + thickness*2
        bottomBaseH = inDepth + thickness*2
        bottomBase = Rectangle(bottomBaseW, bottomBaseH)

        bottomSlotXW = slotLength
        bottomSlotXH = slotThickness
        for i in range(slotsX):
            spacing = (inWidth - bottomSlotXW*slotsX)/(slotsX+1)
            x = -inWidth/2 + spacing+bottomSlotXW/2 + i*(spacing+bottomSlotXW)
            for j in range(modulesY-1):
                spacing = (inDepth - bottomSlotXH*(modulesY-1))/(modulesY)
                y = -inDepth/2 + spacing+bottomSlotXH/2 + j*(spacing+bottomSlotXH)
                
                if slotsX >= 4:
                    if i > 0 and i < slotsX-1:
                        if i % (slotsX-1) != (j%(slotsX-2))+1: 
                            continue 
                
                with Locations((x,y)):
                    Rectangle(bottomSlotXW,bottomSlotXH, mode=Mode.SUBTRACT)

        bottomSlotYW = slotThickness
        bottomSlotYH = slotLength
        for i in range(slotsY):
            spacing = (inDepth - bottomSlotYH*slotsY)/(slotsY+1)
            y = -inDepth/2 + spacing+bottomSlotYH/2 + i*(spacing+bottomSlotYH)
            for j in range(modulesX-1):
                
                if slotsY >= 3:
                    if i % 2 == 0:
                        continue
                
                spacing = (inWidth - bottomSlotYW*(modulesX-1))/(modulesX)
                x = -inWidth/2 + spacing+bottomSlotYW/2 + j*(spacing+bottomSlotYW)
                with Locations((x,y)):
                    Rectangle(bottomSlotYW,bottomSlotYH, mode=Mode.SUBTRACT)

    extrude(bottom.sketch,thickness)
bottom1 = copy(Bottom.part)
show(bottom1)