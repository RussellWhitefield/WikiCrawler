import pygame, sys, time, csv
import pandas as pd

from bin import Animatable2d


'''
Structure:
Startmenu
    Background
    Title
    Start button
    Exit button
Gamescreen
Mapscreen
Endscreen
'''
class Controller:
    
    def __init__(self):
        #State, determines which screen or menu is open while in the game
        self.STATE = "start"

        #General
        self.window_w = 1200
        self.window_h = 800
        self.window = pygame.display.set_mode((self.window_w,self.window_h))
        self.display = pygame.Surface((self.window_w,self.window_h))
        self.display_w = pygame.display.Info().current_w
        self.display_h = pygame.display.Info().current_h
        self.center_w = self.display_w/2
        self.center_h = self.display_h/2
        self.clock = pygame.time.Clock()
        self.tick = 60
        self.last_time = time.time()
        self.zoom_toggle = 1

        #start_menu

        start_button_offset = [-self.center_w/1.8,0]
        start_exit_button_offset = [-self.center_w/1.8,280]

        offsets = [start_button_offset,start_exit_button_offset]
        for i in offsets:
            i[0] += self.center_w
            i[1] += self.center_h
        
        self.start_background = Animatable2d.Object(["assets/start_background.png"], self.display_w, self.display_h,0,0, False)
        self.start_button = Animatable2d.Object(["assets/start_button.png","assets/start_button1.png"],1,1,start_button_offset[0],start_button_offset[1])
        self.start_exit_button = Animatable2d.Object(["assets/exit_button.png","assets/exit_button1.png"],1,1,start_exit_button_offset[0], start_exit_button_offset[1])

        self.start_group = pygame.sprite.Group()
        self.start_group.add(self.start_button, self.start_exit_button)

        #game_screen
        #self.game_background = Animatable2d.Object(["game_background.png"], self.display_w, self.display_h,0,0,False)

        #end_screen

        #quit

    def mainloop(self):

        while True:
            if (self.STATE == "start"):
                self.start_menu_loop()
            elif (self.STATE == "game"):
                self.game_screen_loop()
            elif (self.STATE == "map"):
                self.map_screen_loop()
            elif (self.STATE == "end"):
                self.end_screen_loop()
            elif (self.STATE == "quit"):
                self.exit_loop()
                sys.exit()

    def start_menu_loop(self):

        self.display.blit(self.start_background.image, self.start_background.rect.center)

        while self.STATE == "start":
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Start buttons
                    if(self.start_button.rect.collidepoint(event.pos)):
                        self.start_button.setFrame(1)
                        self.STATE = "game"
                    elif(self.start_exit_button.rect.collidepoint(event.pos)):
                        self.start_exit_button.setFrame(1)
                        self.STATE = "quit"
                if event.type == pygame.QUIT:
                    self.STATE = "quit"

            #Draw and update
            self.start_group.draw(self.display)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.clock.tick(self.tick)

    def game_screen_loop(self):
        while self.STATE == "game":
            dt = time.time() - self.last_time
            dt *= self.tick
            self.clock.tick(self.tick)

    def map_screen_loop(self):
        while self.STATE == "map":
            pass
        
    def end_screen_loop(self):
        while self.STATE == "end":
            pass
    def exit_loop(self):
        pygame.display.quit()
        pygame.quit()