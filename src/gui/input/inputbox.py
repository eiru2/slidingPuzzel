import pygame
from sys import path
import config as con



class Inputbox:
    def __init__(self,pos:list,size:list, coler:tuple, text:str, font:str = None, fontSize:int = 32):
        """_summary_

        Args:
            pos (list): postios til input boksen
            size (list): storelse til input boksen
            coler (tuple): hvilken farge input boksen skal ha
            text (str): placeholder tekst
            font (str, optional): hviken type font. Defaults to None.
            fontSize (int, optional): storles po fonten. Defaults to 32.
        """
        self.pos = pos
        self.size = size
        
        self.coler = coler
        self.active = False
        
        self.font = pygame.font.Font(font,fontSize)
        self.plassHolderText = text
        self.inputText = ""
    
    def rect(self):
        """_summary_

        Returns:
            pygame rect: lagger en rect for colision
        """
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0],self.size[1])  
    
    def click(self, pos):
        if not self.rect().collidepoint(pos):
            self.active = False
            return False
        self.active = not self.active
        return True
    
    def update(self, key):
        if self.active:
            # print("cat")
            # print(key)
            if key == "return":
                print(self.inputText)
                self.inputText = ""
                self.active = False
            elif key == "del":
                self.inputText = self.inputText[:-1]
            else:
                self.inputText += key
            
        
     
    def draw(self,surface):
        """_summary_

        Args:
            surface (pygame display): hvor input boksen skal tegnes
        """
        box = pygame.Surface((self.size[0],self.size[1]), pygame.SRCALPHA, 32).convert_alpha()
        box.fill(self.coler)
        if self.active or self.inputText != "":
            textimg = self.font.render(self.inputText, True, con.farger["SVART"])
            text_width, text_height = self.font.size(self.inputText)
        else:
            textimg = self.font.render(self.plassHolderText, True, con.farger["SVART"])
            text_width, text_height = self.font.size(self.plassHolderText)
            
        
        # rect = self.rect()
        center_x =  (self.size[0]-text_width)/2
        center_y =  (self.size[1]-text_height)/2
        box.blit(textimg,(center_x, center_y))
        surface.blit(box,self.pos)
        
        # rect = self.rect()
        # pygame.draw.rect(surface, self.coler, rect)