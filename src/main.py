import pygame as pg
import config as cf

from controlls import LeftClick

from gui.text.Drawtext import Text_FPS

from state import Menu, Test, InputDebuger, Game


class App:
    def __init__(self):
        """Starter spill objekte
        """
        pg.init()
        self.screen = pg.display.set_mode((cf.WIDTH,cf.HEIGHT))
        # self.screen_render = pg.display.set_mode((cf.BREDDE,cf.Hoyte))
        self.run = True
        
        self.input = {"left_click":False, "left_duble_click":False, "arrow_left": False, "arrow_right": False, "scroll_wheel": 0, "textInput": "", "undoMove": False, "solver": False , "debug": False}
        self.inputHold = {"left_click":False}
        
        self.clock = pg.time.Clock()
        self.time = False
        self.timer = 0
        self.FPScounter = Text_FPS((0,0), (f"Fps: {str(round(self.clock.get_fps(),2))}"))
        
        
        self.state_stack = []
        self.state_dict = {
            "inputDebuger" : InputDebuger,
            "menu": Menu,
            "test": Test,
            "game": Game,
        }
        
        self.leftclick = LeftClick()
        self.clicked = False
        self.clickCunter = 0
        
        self.load_state()
        
    def app_loop(self):
        """Hovedspill loop
        """
        while self.run:
            # print(self.state_stack)
            self.get_input()
            self.update()
            self.render()
            self.rest_keys()
            # print("click:",self.input, "hold:",self.inputHold, self.timer)
        
    def get_input(self):
    
        
        """Henter input fra spillerne
        """
        # click event
        if self.time:
            self.timer += self.clock.get_time()/1000
            

            # left click
            self.leftclick.click(self)            
            
        for event in pg.event.get():     
            if event.type == pg.QUIT:
                self.run = False
                exit()
                pg.quit()
                
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clickCunter += 1
                    self.clicked = True
                    self.time = True


            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.inputHold["left_click"] = False 
                    self.clicked = False

            
            if event.type == pg.MOUSEWHEEL:
                # print(event)
                self.input["scroll_wheel"] = event.y

            
            if event.type == pg.KEYDOWN:
                # normal input
                if event.key in cf.undoMove:
                    self.input["undoMove"] = True
                if event.key in cf.solver:
                    self.input["solver"] = True
                if event.key in cf.debuger:
                    self.input["debug"] = True
                
                # text input
                if  event.key == pg.K_LEFT:
                    self.input["arrow_left"] = True
                if  event.key == pg.K_RIGHT:
                    self.input["arrow_right"] = True
                    
                if event.key == pg.K_RETURN:
                    self.input["textInput"] = "return"
                elif event.key == pg.K_BACKSPACE:
                    self.input["textInput"] = "del"
                else:
                    self.input["textInput"] = event.unicode
                    
                    
                          
                                    
            if event.type == pg.KEYUP:
                if  event.key == pg.K_LEFT:
                    self.input["arrow_left"] = False
                if  event.key == pg.K_RIGHT:
                    self.input["arrow_right"] = False    
                    
            
            
    def update(self):
        """KJøre update methoden for den sit lagt til state i stacken
        """
        # print(self.spiller1_input,self.spiller2_input)
        self.state_stack[-1].update(self.input,self.inputHold)
        
              
    def render(self):
        """KJøre render methoden for den sit lagt til state i stacken
        """
        self.screen.fill(cf.farger["MØRK GRÅ"])
        self.state_stack[-1].render(self.screen)
        self.showFPS(self.screen)
        self.clock.tick(cf.tick)
        pg.display.update()
        
        
    def load_state(self):
        """laster in den første staten
        """
        # self.title_screen = self.state_dict["lagre_kap"](self)
        self.title_screen = self.state_dict["game"](self)
        
        self.state_stack.append(self.title_screen)
        
    def rest_keys(self):
        """rester input fra spiller
        """
        for key in self.input.keys():
            # For ikke bolske input
            if key == "textInput" or key == "scroll_wheel":
                self.input["textInput"] = ""
                self.input["scroll_wheel"] = 0
            else:
                self.input[key] = False
    
    def showFPS(self, surface):
        self.FPScounter.update(self.clock.get_fps())
        self.FPScounter.draw(surface)
            


if __name__ == "__main__":
    a = App()
    while a.run:
        # profile.run('a.app_loop()')
        a.app_loop()
        pass