import pygame as pg
from random import choice
from config import farger, fargerKey

class tile:
    def __init__(self,number,gridePos, size):
        self.number = number
        self.pos_gride = list(gridePos)
        self.size = list(size)
        self.font = pg.font.Font(None, int(self.size[1] * 0.6))   # scale text to tile height
    
    def update(self):
        pass
    
    def draw(self,surface, pos):
        if self.number == 0:
            return 0
        
        pg.draw.rect(surface, 
        farger[fargerKey[self.number%len(fargerKey)]],
        (
            pos[0] + self.pos_gride[0]*self.size[0],
            pos[1] + self.pos_gride[1]*self.size[1],
            self.size[0],
            self.size[1]
        )
        )
                # --- draw number in center ---
        text_surf = self.font.render(str(self.number), True, (0, 0, 0))

        # center the text inside the tile
        tile_x = pos[0] + self.pos_gride[0] * self.size[0]
        tile_y = pos[1] + self.pos_gride[1] * self.size[1]

        # print(self.number, tile_x,tile_y, self.pos_Gride)
        text_rect = text_surf.get_rect(center=(tile_x + self.size[0] // 2,
                                            tile_y + self.size[1] // 2))
        surface.blit(text_surf, text_rect)



Neghibor = [(-1,0),(1,0),(0,-1),(0,1)]     
class Grid:
    def __init__(self,rutter, windowSize):
        self.rutter = list(rutter)
        self.windowSize = list(windowSize)
        self.tilesize_rect = [
            self.windowSize[0]//self.rutter[0],
            self.windowSize[1]//self.rutter[1]      
            ]
        self.tilesize = min(self.tilesize_rect)
        
        
        self.pos = [
            (self.windowSize[0]-self.tilesize*rutter[0])/2,
            (self.windowSize[1]-self.tilesize*rutter[1])/2
            ]
        
        self.grid = []
        for x in range(self.rutter[0]):
            self.grid.append([])
            for y in range(self.rutter[1]):
                self.grid[x].append([])

        i = 1
        for y in range(self.rutter[1]):
            for x in range(self.rutter[0]):
                self.grid[x][y] = tile(i,(x,y),(self.tilesize,self.tilesize))
                i+=1
        self.grid[-1][-1].number = 0
        self.zeroPos = [self.rutter[0]-1,self.rutter[1]-1]
        self.preMove = []
        self.vinnestate = self.return_gride_state()
        
    def update(self, pos_mous):
        pos = [
            int((pos_mous[0]-self.pos[0])//self.tilesize),
            int((pos_mous[1]-self.pos[1])//self.tilesize)
        ]
        if 0 <= pos[0] < self.rutter[0] and 0 <= pos[1] < self.rutter[1]:
            print("correct")
            print(pos)
            # self.move(pos)
            print(self.testMove(pos))
    
    def move(self, pos):
        if self.grid[pos[0]][pos[1]].number == 0:
            # print(0)
            return False
        
        for x,y in Neghibor:
            Negibor_pos = [pos[0]+x,pos[1]+y]
            # print(Negibor_pos, x,y) 
            if 0 <= Negibor_pos[0] < self.rutter[0] and 0 <= Negibor_pos[1] < self.rutter[1]:
                if self.grid[Negibor_pos[0]][Negibor_pos[1]].number == 0:
                    # print("vellyket")
                    self.preMove.append(self.grid[pos[0]][pos[1]].number)
                    
                    self.grid[Negibor_pos[0]][Negibor_pos[1]],self.grid[pos[0]][pos[1]] = self.grid[pos[0]][pos[1]],self.grid[Negibor_pos[0]][Negibor_pos[1]]
                    
                    self.grid[Negibor_pos[0]][Negibor_pos[1]].pos_gride = Negibor_pos
                    self.grid[pos[0]][pos[1]].pos_gride = pos
                    self.zeroPos = pos
 
    def testMove(self, pos):
        if self.grid[pos[0]][pos[1]].number == 0:
            # print(0)
            return False
        
        in_same_y = (pos[1] == self.zeroPos[1])
        in_same_x = (pos[0] == self.zeroPos[0])
        
        if not (in_same_y or in_same_x):
            return False 
        
        moves = []
        if in_same_x:
            y = self.zeroPos[1] - pos[1]
            print(abs(y)//y)
            for i in range(0,y, abs(y)//y):
                moves.append((pos[0],pos[1]+i))
            return moves,y
        
        if in_same_y:
            x = self.zeroPos[0] - pos[0]
            print(abs(x)//x)
            for i in range(0,x, abs(x)//x ):
                moves.append((pos[0]+i,pos[1]))
            return moves,x
        

        
# '        moves = []
#         edge = False
#         if pos[1] == self.zeroPos[1]:
#             x = 1
#             moves.append(pos)
#             while not edge:
#                 print(pos, "x: ", x,moves)
#                 if not (0 <= pos[0]+x < self.rutter[0] and 0 <= pos[1] < self.rutter[1]):
#                     moves = [pos]
#                     edge = True
#                     break
#                 if self.grid[pos[0]+x][pos[1]].number == 0: return moves,1
#                 moves.append((pos[0]+x,pos[1]))
#                 x+=1
            
#             edge = False
#             x = -1
#             while not edge:
#                 print(pos, "x: ", x,moves)
#                 if not (0 <= pos[0]+x < self.rutter[0] and 0 <= pos[1] < self.rutter[1]):
#                     moves = []
#                     edge = True
#                     break
#                 if self.grid[pos[0]+x][pos[1]].number == 0: return moves,2
#                 moves.append((pos[0]+x,pos[1]))
#                 x-=1
         
#         elif pos[0] == self.zeroPos[0]:
#             y = 1
#             moves.append(pos)
#             while not edge:
#                 print(pos, "y: ", y,moves)
#                 if not (0 <= pos[0] < self.rutter[0] and 0 <= pos[1]+y < self.rutter[1]):
#                     moves = [pos]
#                     edge = True
#                     break
#                 if self.grid[pos[0]][pos[1]+y].number == 0: return moves,3
#                 moves.append((pos[0],pos[1]+y))
#                 y+=1

#             edge = False
#             y = -1
#             while not edge:
#                 print(pos, "y: ", y,moves)
#                 if not (0 <= pos[0] < self.rutter[0] and 0 <= pos[1]+y < self.rutter[1]):
#                     moves = []
#                     edge = True
#                     break
#                 if self.grid[pos[0]][pos[1]+y].number == 0: return moves,4
#                 moves.append((pos[0],pos[1]+y))
#                 y-=1'
        return moves, "inegenting"
    
    def undoMove(self):
        for x in range(self.rutter[0]):
            for y in range(self.rutter[1]):
                # print(x,y)
                if len(self.preMove) == 0:
                    # print(1)
                    return [-1,-1]
                elif self.grid[x][y].number == 0:
                    pass
                elif self.grid[x][y].number == self.preMove[-1]:
                    self.move([x,y])
                    self.preMove.pop()
                    self.preMove.pop()
                    return [x,y]
        
    def shuffel(self, moves):

        for i in range(moves):
            moved = False
            while not moved:
                temp = choice(Neghibor)
                x = self.zeroPos[0] + temp[0]
                y = self.zeroPos[1] + temp[1]
                if not (0 <= x < self.rutter[0] and 0 <= y < self.rutter[1]):
                    pass
                
                elif not self.grid[x][y].number == self.preMove:
                    # print(self.grid[x][y].number,self.preMove)
                    self.move([x,y])
                    moved = True
        self.preMove = []
            
    def return_gride_state(self):
        array = ""
        for y in range(self.rutter[1]):
            for x in range(self.rutter[0]):
                    array = array + str(self.grid[x][y].number)+" "
        return array
    
    def load_gride_state(self, state):
        i = 0
        state = state.split()
        for y in range(self.rutter[1]):
            for x in range(self.rutter[0]):
                self.grid[x][y].number = int(state[i])
                self.grid[x][y].pos_gride = [x,y]
                print(self.grid[x][y].number, self.grid[x][y].pos_gride)
                if state[i] == 0:
                    self.zeroPos = [x,y]
                i+=1
                
    def muligMoves(self, preMove):
        # and preMove != list(( x+self.zeroPos[0], y+self.zeroPos[1]))
        moves = []  
        diraction=[]
        for x,y in Neghibor:
            if (0 <= x+self.zeroPos[0] < self.rutter[0] and 0 <= y+self.zeroPos[1] < self.rutter[1]) and preMove != (x,y) :
                # print(self.zeroPos)
                moves.append((self.zeroPos[0] + x, self.zeroPos[1] + y))
                diraction.append((x*-1,y*-1))
        return moves, diraction

    def win(self):
        if self.return_gride_state() == self.vinnestate:
            return True
        return False

    def return_Image(self):
        pass
    
    def draw(self,surface):
        # print("-------------------------------------------------")
        i = 0
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                self.grid[x][y].draw(surface, self.pos)
    
    def debug(self):
        print(self.grid)
        print("-------------")
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                print(self.grid[x][y].number, "  " , end="")
            print("")
        # print(self.grid)