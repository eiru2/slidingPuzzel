from state import State
from objeckt import Grid
import copy

import config as cf

import pygame as pg

Neghibor = [(-1,0),(1,0),(0,-1),(0,1)]  

max_depth =  10

    
def search(depth, max_depth, grid, curentmove,premove,currentPath:list,visited):
    # print(depth)
    if depth >= max_depth:
        # print("Depth")
        return False
    
    state = grid.return_gride_state()
    if state in visited:
        # print("besøkt")

        return False
    
    visited.add(state)
    
    if grid.win():
        # print("dunnet")
        return True
    
    moves, dirction = grid.muligMoves(premove)
    if len(moves) == 0:
        return False
    
    # print(f"{curentmove}:: {moves} ")
    for move, dirction in zip(moves,dirction):
        # print("nest move")
        grid.move(move)
        currentPath.append(move)
        if search(depth+1, max_depth, grid ,move,dirction,currentPath,visited):
            grid.undoMove()
            return True
        grid.undoMove()
        currentPath.pop()
        
    visited.remove(state)
    return False


        
    # grid.

class Game(State):
    def __init__(self, app):
        super().__init__(app)
        self.buttons = []
        self.grid = Grid((24,32), (cf.WIDTH , cf.HEIGHT))
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
            fund = False
            i = 1 
            limet = 50
            while not fund and i < limet:
                visited = set()
                moves, dirction = self.grid.muligMoves([0,0])
                for move, dirction in zip(moves,dirction):
                    # print(move,dirction)
                    self.path.append(move)
                    self.grid.move(move)
                    # visited.append(self.grid.return_gride_state())
                    if search(0,i,self.grid, move, dirction, self.path, visited):
                        fund = True
                        self.grid.undoMove()
                        break
                    self.grid.undoMove()
                    self.path.pop()
                i+=1
                print(i)
                
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
            # self.grid.load_gride_state("012345678")
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