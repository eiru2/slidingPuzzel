import pygame as pg
from random import choice
from config import farger, fargerKey,imageBorder,pading
from gui import Shadow,imageFram,imageBorderCut

class Tile:
    def __init__(self,number,gridePos, size, picture=False):
        self.number = number
        self.pos_gride = list(gridePos)
        self.size = list(size)
        self.font = pg.font.Font(None, int(self.size[1] * 0.6))   # scale text to tile height

        self.image = picture

        self.showNumber = False

    
    def update(self):
        pass
    
    def draw(self,surface, pos):
        if self.number == 0:
            return 0
        if not self.image:
            pg.draw.rect(surface,
            farger[fargerKey[self.number%len(fargerKey)]],
            (
                pos[0] + self.pos_gride[0]*self.size[0],
                pos[1] + self.pos_gride[1]*self.size[1],
                self.size[0],
                self.size[1])
                )
        rect = (pos[0] + self.pos_gride[0]*self.size[0],pos[1] + self.pos_gride[1]*self.size[1],self.size[0],self.size[1])

        surface.blit(self.image,rect)
        #pg.draw.rect(surface,(0,0,0),rect,1)

        if self.showNumber:
            # --- draw number in center ---
            text_surf = self.font.render(str(self.number), True, (255, 0, 0))

            # center the text inside the tile
            tile_x = pos[0] + self.pos_gride[0] * self.size[0]
            tile_y = pos[1] + self.pos_gride[1] * self.size[1]

            # print(self.number, tile_x,tile_y, self.pos_Gride)
            text_rect = text_surf.get_rect(center=(tile_x + self.size[0] // 2,
                                                   tile_y + self.size[1] // 2))
            surface.blit(text_surf, text_rect)



Neghibor = [(-1,0),(1,0),(0,-1),(0,1)]     
class Grid:
    def __init__(self,rutter, windowSize, picture):
        self.border = imageBorder

        self.rutter = list(rutter)
        self.windowSize = list(windowSize)

        self.tileSizeRect = [
            (self.windowSize[0] - self.border-pading) // self.rutter[0],
            (self.windowSize[1] - self.border-pading) // self.rutter[1]
            ]
        self.tileSize = min(self.tileSizeRect)


        self.pos = [
            (self.windowSize[0] - self.tileSize * rutter[0]) / 2,
            (self.windowSize[1] - self.tileSize * rutter[1]) / 2
            ]
        # includer ikke border
        self.gridSize = [self.tileSize*rutter[0],self.tileSize*rutter[1]]

        self.image = picture
        imageSize = self.image.get_size()
        x,y =  (self.tileSize*rutter[0]+self.border*2)/imageSize[0], (self.tileSize*rutter[1]+self.border*2)/imageSize[1]
        self.image = pg.transform.scale_by(self.image,max(x,y))
        self.imageCroped = pg.Surface((self.gridSize[0]+self.border*2,self.gridSize[1]+self.border*2))
        self.imageCroped.blit( self.image,(0,0,self.gridSize[0]+self.border*2,self.gridSize[1]+self.border*2))
        self.image = self.imageCroped


        self.imgInner = imageBorderCut(self.image, self.border)
        self.imgborder = imageFram(self.image, self.border)
        self.imgborder = Shadow((self.pos[0]-self.border,self.pos[1]-self.border),self.imgborder,10)

        self.grid = []
        for x in range(self.rutter[0]):
            self.grid.append([])
            for y in range(self.rutter[1]):
                self.grid[x].append([])

        i = 1
        for y in range(self.rutter[1]):
            for x in range(self.rutter[0]):
                tilePicture = pg.Surface((self.tileSize,self.tileSize))
                tilePicture.blit(self.imgInner, (0,0),(x*self.tileSize,y*self.tileSize,self.tileSize,self.tileSize))
                self.grid[x][y] = Tile(i, (x, y), (self.tileSize, self.tileSize),tilePicture)
                i+=1
        self.grid[-1][-1].number = 0
        self.zeroPos = [self.rutter[0]-1,self.rutter[1]-1]
        self.preMove = []
        self.vinnestate = self.return_gride_state()
        
    def update(self, pos_mous):
        pos = [
            int((pos_mous[0]-self.pos[0]) // self.tileSize),
            int((pos_mous[1]-self.pos[1]) // self.tileSize)
        ]
        if 0 <= pos[0] < self.rutter[0] and 0 <= pos[1] < self.rutter[1]:
            print("correct")
            print(pos)
            # self.move(pos)
            moves, numbers = self.FindMoves(pos)
            # self.preMove.append(numbers)
            # print(numbers)
            # print(moves.reverse())
            self.preMove.append([])
            moves.reverse()
            for move in moves:
                self.preMove[-1].append(self.move(move))
    
    def move(self, move):
        if self.grid[move[0]][move[1]].number == 0:
            # print(0)
            return []
        moves = None
        for x,y in Neghibor:
            Negibor_pos = (move[0]+x,move[1]+y)
            # print(Negibor_pos, x,y) 
            if 0 <= Negibor_pos[0] < self.rutter[0] and 0 <= Negibor_pos[1] < self.rutter[1]:
                if self.grid[Negibor_pos[0]][Negibor_pos[1]].number == 0:
                    # print("vellyket")
                    # self.preMove.append(self.grid[move[0]][move[1]].number)
                    self.grid[Negibor_pos[0]][Negibor_pos[1]],self.grid[move[0]][move[1]] = self.grid[move[0]][move[1]],self.grid[Negibor_pos[0]][Negibor_pos[1]]
                    
                    self.grid[Negibor_pos[0]][Negibor_pos[1]].pos_gride = Negibor_pos
                    self.grid[move[0]][move[1]].pos_gride = move
                    self.zeroPos = move
                    moves = Negibor_pos

        return moves
 
    def FindMoves(self, pos):
        if self.grid[pos[0]][pos[1]].number == 0:
            # print(0)
            return [], []
        
        in_same_y = (pos[1] == self.zeroPos[1])
        in_same_x = (pos[0] == self.zeroPos[0])
        
        if not (in_same_y or in_same_x):
            return [], []
        
        moves = []
        numberTile = []
        if in_same_x:
            y = self.zeroPos[1] - pos[1]
            print(abs(y)//y)
            for i in range(0,y, abs(y)//y):
                moves.append((pos[0],pos[1]+i))
                numberTile.append(self.grid[pos[0]][pos[1]+i].number)
            return moves, numberTile
        
        if in_same_y:
            x = self.zeroPos[0] - pos[0]
            print(abs(x)//x)
            for i in range(0,x, abs(x)//x ):
                moves.append((pos[0]+i,pos[1]))
                numberTile.append(self.grid[pos[0]+i][pos[1]].number)
            return moves, numberTile

        return []
    
    def undoMove(self):
        if len(self.preMove) == 0:
            return False
        self.preMove[-1].reverse()
        for move in self.preMove[-1]:
            print(move)
            if len(self.preMove[-1]) == 0:
                # print(1)
                return False
            elif self.grid[move[0]][move[1]].number == 0:
                pass
            else:
                self.move(move)

        self.preMove.pop()
        return False


        
    def shuffel(self, moves):
        self.preMove=[[]]
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
        if self.image:
            self.imgborder.draw(surface)
            #surface.blit(self.imginner,self.pos)

        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                self.grid[x][y].draw(surface, self.pos)
    
    def debug(self):
        # print(self.grid)
        print("-------------")
        for y in range(self.rutter[1]):
            for x in range(self.rutter[0]):
                print(self.grid[x][y].number, "  " , end="")
            print("")
        # print(self.grid)