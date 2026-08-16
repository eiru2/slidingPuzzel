import pygame as pg

WIDTH = 1600
HEIGHT = 800

#frame rate
tick = 0

#click values 
TrasholdHolde = 0.3 # sekkunder
TresholdDubleClik = 0.2

ScrollSpeed = 10

# Farger
farger = {
    "HVIT": (255, 255, 255),
    "SVART": (0, 0, 0),
    "MØRK GRÅ": (70, 91, 91),
    "RØD": (255, 0, 0),
    "GRØNN": (0, 255, 0),
    "BLÅ": (0, 0, 255),
    "GUL": (255, 255, 0),
    "ORANSJE": (255, 165, 0),
    "LILLA": (128, 0, 128),
    "GRÅ": (128, 128, 128),
    "BRUN": (165, 42, 42)
}
fargerKey = []
for key in farger:
    if not key == "MØRK GRÅ" and not key == "SVART":
        fargerKey.append(key)
        
        
# løser
max_depth =  50

# text
text_medium = 44


# deffult controlls
undoMove = [pg.K_u]
solver = [pg.K_s]
debuger = [pg.K_d] 
