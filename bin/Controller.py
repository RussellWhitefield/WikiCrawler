import pygame, sys, time, csv
import pandas as pd

from bin import Animatable2d
from bin import TextDisplay

'''
Parts of the game
All buttons and sprites are done with 2dAnimatable Class
Start Menu - 
    Clicking start button leads to prompt for user input, searches wikipedia, uses WikiDungeonCrawler to generate 2 links, and puts them into an array.
    Sends the player to the game screen.
Game screen - 
    Displays articles for each of the links in the array
    Displays buttons to guess which article is longer or shorter
Exit loop
    Quits the game with pygame functions
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
        pygame.font.init()

        #start_menu
        
        start_button_offset = [-self.center_w/1.8,0]
        start_exit_button_offset = [-self.center_w/1.8,200]

        start_offsets = [start_button_offset,start_exit_button_offset]
        for i in start_offsets:
            i[0] += self.center_w
            i[1] += self.center_h
        
        self.start_background = Animatable2d.Object(["assets/start_background.png"], self.display_w, self.display_h,0,0, False)
        self.start_button = Animatable2d.Object(["assets/start_button.png","assets/start_button1.png"],1,1,start_button_offset[0],start_button_offset[1])
        self.start_exit_button = Animatable2d.Object(["assets/exit_button.png","assets/exit_button1.png"],1,1,start_exit_button_offset[0], start_exit_button_offset[1])

        self.start_group = pygame.sprite.Group()
        self.start_group.add(self.start_button, self.start_exit_button)

        #game_screen
        left_window_offset = [-self.center_w/2,-self.center_h/4]
        right_window_offset = [self.center_w/2,-self.center_h/4]
        question_bar_offset = [0,200]
        left_question_button_offset = [-150,200]
        right_question_button_offset = [150,200]
        
        game_offsets = [left_window_offset,right_window_offset, question_bar_offset, left_question_button_offset, right_question_button_offset]
        for i in game_offsets:
            i[0] += self.center_w
            i[1] += self.center_h

        self.game_background = Animatable2d.Object(["assets/game_background.png"], self.display_w, self.display_h,0,0,False)
        self.left_window = Animatable2d.Object(["assets/question_window.png"], 1, 1,left_window_offset[0],left_window_offset[1])
        self.right_window = Animatable2d.Object(["assets/question_window.png"], 1, 1,right_window_offset[0],right_window_offset[1])
        self.question_bar = Animatable2d.Object(["assets/question_bar.png"], 1, 1,question_bar_offset[0],question_bar_offset[1])
        self.left_question_button = Animatable2d.Object(["assets/guess_button1.png","assets/guess_button2.png"], 1, 1,left_question_button_offset[0],left_question_button_offset[1])
        self.right_question_button = Animatable2d.Object(["assets/guess_button1.png","assets/guess_button2.png"], 1, 1,right_question_button_offset[0],right_question_button_offset[1])
        self.button_click_delta = 0

        self.left_text = TextDisplay.TextDisplay()
        self.right_text = TextDisplay.TextDisplay()

        self.game_group = pygame.sprite.Group()
        self.game_group.add(self.left_window, self.right_window, self.question_bar, self.left_question_button, self.right_question_button)

        #end_screen

        #quit

    def mainloop(self):

        while True:
            if (self.STATE == "start"):
                self.start_menu_loop()
            elif (self.STATE == "game"):
                self.game_screen_loop()
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

        self.display.blit(self.game_background.image, self.game_background.rect.center)

        while self.STATE == "game":
            if self.button_click_delta == 0:
                self.right_question_button.setFrame(0)
                self.left_question_button.setFrame(0)
            else:
                self.button_click_delta -=1
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #buttons
                    if(self.right_question_button.rect.collidepoint(event.pos)):
                        self.right_question_button.setFrame(1)
                        self.button_click_delta = 10
                        #Add guessing functionality
                    if(self.left_question_button.rect.collidepoint(event.pos)):
                        self.left_question_button.setFrame(1)
                        self.button_click_delta = 10
                        #Add guessing functionality
                if event.type == pygame.QUIT:
                    self.STATE = "quit"
            self.game_group.draw(self.display)
            self.display.blit(self.left_text.text,(-100,0))
            self.display.blit(self.right_text.text,(100,0))
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.clock.tick(self.tick)
            
    def end_screen_loop(self):
        while self.STATE == "end":
            pass
    def exit_loop(self):
        pygame.display.quit()
        pygame.quit()