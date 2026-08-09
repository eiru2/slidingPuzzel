import pygame
from config import farger, text_medium


pygame.font.init()


class Button:
    def __init__(self,pos,text="none",textCooler=farger["SVART"], fontSize = text_medium, font="Arial" , buttonsize=(100,100), buttonCooler =farger["HVIT"] , returnValue=True, state_ref=None):
        """_summary_
            for å lagge en knap som returner
        Args:
            pos (list): kordinater til knapen
            text (str, optional): Hva som skal sto po kanpen. Defaults to "none".
            textCooler (tuple, optional): farge po teksten. Defaults to (0,0,0).
            fontSize (int, optional): storelse po teksten. Defaults to 11.
            font (str, optional): hvilken type font po texten. Defaults to "Arial".
            buttonsize (bool, optional): dimisionen po kanppen. Defaults to True.
            buttonCooler (tuple, optional): farge po knapen. Defaults to (255,255,255).
            returnValue (bool, optional): hvilken verdi den returner. Defaults to True.
        """
        self.pos = list(pos)
        self.buttonsize = list(buttonsize)
        self.renderButtonColer = buttonCooler
        
        self.textCooler = textCooler
        self.fontSize = fontSize
        self.font = pygame.font.SysFont(font, fontSize)
        self.text = returnTextWithLine(self,text)
        
        self.state_ref = state_ref

        self.returnValue = returnValue # For å velge hvilken verdie som retunerer
        
        # if buttonsize == True: 
        #     text_width, text_height = self.font.size(self.text)
        #     self.buttonsize = [round(text_width,-1)+50,round(text_height,-1)+10]
        # else:
        #     self.buttonsize = list(buttonsize)
        # print(self.buttonsize)
    
    def rect(self):
        """_summary_

        Returns:
            pygame rect: return rectangl values for the button
        """
        return  pygame.Rect(self.pos[0],self.pos[1],self.buttonsize[0],self.buttonsize[1])
    
    def click(self, pos):
        """SJekker om knappen er kliket

        Args:
            pos (list:(float, float)): list av mus kordinater

        Returns:
            _type_: retuner ennten en retuner verdi eller True når knappen blir trykt
        """
        

        # Sjekker om musen er over knappen  
        if not self.rect().collidepoint(pos):
            return False
        return self.returnValue

    
    def update(self,offset):
        pass


    def draw(self,surface, offset=[0,0]):
        """Tegner knappen

        Args:
            surface (pygame display): hvilken surface som skal bli tegnet po
            offset (list, optional): en offset på hvor knappe skal bli tegnet. Defaults to [0,0].
        """
        button = pygame.Surface((self.buttonsize[0],self.buttonsize[1]), pygame.SRCALPHA, 32).convert_alpha()
        button.fill(self.renderButtonColer)
        textSize_y = 0
        for text in self.text:
            textSize_y += self.font.size(text)[1]+1
        y = (self.buttonsize[1]-textSize_y)/2
        for text in self.text:
            textimg = self.font.render(text, True, self.textCooler)
            
            text_width, text_height = self.font.size(text)
            center_x =  (self.buttonsize[0]-text_width)/2
            button.blit(textimg,(center_x, y))
            y +=  text_height
        surface.blit(button,(self.pos[0] + offset[0], self.pos[1]+ offset[1]))


class ButtonToggel(Button):
    def __init__(self, pos, text="none", textCooler=farger["SVART"], fontSize=text_medium, font="Arial", buttonsize=(100,100), buttonCooler=(farger["RØD"],farger["BLÅ"]), returnValue=True ,active=True):
        self.active=active
        self.buttonColer = buttonCooler
        self.renderColer = self.buttonColer[1] if self.active else self.buttonColer[0]
        super().__init__(pos, text, textCooler, fontSize, font, buttonsize,self.renderColer , returnValue,)
        
    def click(self, pos):
        """SJekker om knappen er kliket

        Args:
            pos (list:(float, float)): list av mus kordinater

        Returns:
            _type_: retuner ennten en retuner verdi eller True når knappen blir trykt
        """
        

        # Sjekker om musen er over knappen  
        if not self.rect().collidepoint(pos):
            return False
        
        
        # Toggle state
        self.update(not self.active)


        
        return self.returnValue


    
    def update(self, set_active:bool):
        """KJekker om kanpen skal være aktive

        Args:
            set_active (bool): Sjekker hva som er aktive
        """
        self.active = set_active
        self.renderButtonColer = self.buttonColer[1] if self.active else self.buttonColer[0]


class ButtonFunk(Button):
        def __init__(self, pos, funk, text="none", textCooler=(0, 0, 0), fontSize=11, font="Arial", buttonsize=True, buttonCooler=(255, 255, 255)):
            super().__init__(pos, text, textCooler, fontSize, font, buttonsize)
            self.funk = funk
            self.buttoncooler = buttonCooler
           
        def click_Funk(self, pos):
            """_summary_
                utfører en funksjon når knappen blir trykt
            Args:
                pos (list:(float, float)): list av mus kordinater
            """
            if self.funk == None:
                print("Error: Det er ikke git en funksjon til knappen")
                return
            rect = self.rect()
            if rect.collidepoint(pos):
                self.funk()

    
def returnTextWithLine(self, InText:str):
    """
    self (list): classe
    text (str): txt som skal opp deles.
    
    return (list): en list av strenger som er opp delt i flere linjer hvis det ikke får plass på knappen
    """
    
    text = list(InText.split())
    new = []
    i = 0
    while i  < len(text):
        try: 
            int(new[-1][-1])
            int(text[i][0])
            new.append(str(new[-1])+ " "+ str(text[i]))
            new.pop(-2)
            i+=1
        except:
            new.append(text[i])
            i+=1

    text = new

    arrTextSize = []
    for tex in text:
        arrTextSize.append(self.font.size(tex))


    new = [text[0]]
    y = 0
    for i in range(len(arrTextSize)-1):

        if self.font.size(new[y])[0] + arrTextSize[i+1][0] < self.buttonsize[0]-5:

                new[y] = (str(new[y])+ " "+ str(text[i+1]))

        else:
            new.append(text[i+1])
            y+=1


    return new