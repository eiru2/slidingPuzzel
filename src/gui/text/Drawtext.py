import pygame as pg
import config as cf

class Text:
    def __init__(self, pos:list,text:str, font:str=None ,fontSize:int=45, fontColor:tuple=cf.farger["HVIT"]):
        """Lager et tekst objekt

        Args:
            pos (list): posisjn med der x er mitt i og y er po toppen
            text (str): Hav som skal stå
            font (str, optional): font på teksten. Defaults to None som gir pygame defult font.
            fontSize (int, optional): størelse på fonten. Defaults to 45.
            fontColor (tuple, optional): Farge på fonten i rgb verdier. Defaults to cf.farger["HVIT"].
        """
        self.text = text
        self.font = pg.font.SysFont(font, fontSize)
        self.font_color = fontColor
        
        
        self.pos = list(pos) 
        x,y = self.font.size(self.text)
        # print(x)
        self.render_pos = list(pos)
        # self.render_pos[0] = self.pos[0] - x/2 # center med bredden
        
    def update(self):
        """oppdater teksten
        """
        pass
        
    def draw(self,surface:pg.Surface, offset:list = [0,0]):
        # offset senner arbied ikke bruk for
        """Tegner teksten på vindue 

        Args:
            surface (pygame.Surface): hvor tekste blir tegnet
            offset: Brukt til å skifte på text med en beveglig kammera
        """
        img = self.font.render(self.text, True, self.font_color)
        surface.blit(img,self.render_pos)
        
        
        

class Text_FPS(Text):
    

    def __init__(self, pos, text, font = None, fontSize = 45, fontColor = cf.farger["HVIT"]):
        """Spesfikt tekst objekt for poeng

        Args:
            pos (list): posisjn med der x er mitt i og y er po toppen
            text (str): Hav som skal stå
            font (str, optional): font på teksten. Defaults to None som gir pygame defult font.
            fontSize (int, optional): størelse på fonten. Defaults to 45.
            fontColor (tuple, optional): Farge på fonten i rgb verdier. Defaults to cf.farger["HVIT"].
        """
        super().__init__(pos, text, font, fontSize, fontColor)
        self.render_pos = pos
        
    def update(self,timer):
        """oppdater teksten

        Args:
            poeng (int, optional): poeng til kampen. Defaults to None.
            score (int, optional): score til kampen. Defaults to None.
        """

        self.text = f"FPS {round(timer,2)}"

