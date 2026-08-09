from state import State
from objeckt import Grid
from logic import start_search, start_search_shortes

import config as cf

import pygame as pg



class Game(State):
    def __init__(self, app):
        super().__init__(app)
        self.buttons = []
        
        self.grid = Grid((3,3), (cf.WIDTH , cf.HEIGHT))
        self.grid.shuffel(100000)
        print(self.grid.muligMoves([-1,-1]))
        self.path = []
        self.fundPath = False

    def update(self, action, actioHold):
        if action["left_click"]:
            print("click")
            mous_pos = pg.mouse.get_pos()
            self.grid.update(mous_pos)
        
        if action["textInput"] =="q":
            self.grid.debug()
            
        if action["textInput"] =="p":
            self.path = start_search(self.grid)
                
                
            print(self.path, "Path")

            cf.tick = 5
            self.fundPath = True

        if action["textInput"] =="t":
            print(self.grid.preMove)
        
        if action["textInput"] =="u":
            print("fdgfhdfg")
            self.grid.undoMove()

            
        if action["textInput"] =="w":
            print(self.grid.win())
            
        if action["textInput"] =="l":
            self.grid.load_gride_state("0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15")
            
        if self.fundPath:
            if len(self.path) == 0:
                self.fundPath = False
                cf.tick = 0
            else:    
                self.grid.move(self.path[0])
                print(self.path)
                self.path.pop(0)
            

    
    def render(self, surface):
        self.grid.draw(surface)
        # self.grid.debug()