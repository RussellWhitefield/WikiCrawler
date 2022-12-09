import pygame, sys, time, csv
import pandas as pd

from bin import Animatable2d
from bin import TextDisplay
from bin import info

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
        self.tick = 15
        self.last_time = time.time()
        self.zoom_toggle = 1
        pygame.font.init()

        #gameplay:
        self.health = 3
        self.correct = 0

        #start_menu
        
        wikiimage_offset = [-self.center_w/1.4,-self.center_h/1.7]
        start_button_offset = [-self.center_w/1.4,0]
        start_exit_button_offset = [-self.center_w/1.4,200]

        start_offsets = [wikiimage_offset, start_button_offset,start_exit_button_offset]
        for i in start_offsets:
            i[0] += self.center_w
            i[1] += self.center_h
        
        self.wikiimage = Animatable2d.Object(["assets/logo_frame0000.png","assets/logo_frame0001.png","assets/logo_frame0002.png","assets/logo_frame0003.png","assets/logo_frame0004.png", "assets/logo_frame0005.png"],5,5,wikiimage_offset[0],wikiimage_offset[1])
        self.start_background = Animatable2d.Object(["assets/start_background.png"], self.display_w, self.display_h,0,0, False)
        self.start_button = Animatable2d.Object(["assets/start_button.png","assets/start_button1.png"],5,5,start_button_offset[0],start_button_offset[1])
        self.start_exit_button = Animatable2d.Object(["assets/exit_button.png","assets/exit_button1.png"],5,5,start_exit_button_offset[0], start_exit_button_offset[1])

        self.start_group = pygame.sprite.Group()
        self.start_group.add(self.wikiimage, self.start_button, self.start_exit_button)

        #game_screen
        question_button_offset_left = [-self.center_w/2,self.center_h/1.8]
        question_button_offset_right = [self.center_w/2,self.center_h/1.8]
        
        game_offsets = [question_button_offset_left, question_button_offset_right]
        for i in game_offsets:
            i[0] += self.center_w
            i[1] += self.center_h

        self.game_background = Animatable2d.Object(["assets/game_background.png"], self.display_w, self.display_h,0,0,False)
        self.question_button_left = Animatable2d.Object(["assets/guess_button.png","assets/guess_button1.png"], 5, 5,question_button_offset_left[0],question_button_offset_left[1])
        self.question_button_right = Animatable2d.Object(["assets/guess_button.png","assets/guess_button1.png"], 5, 5,question_button_offset_right[0],question_button_offset_right[1])
        self.button_click_delta = 0

        self.caticon = pygame.image.load("assets/Caticon.png")       

        self.text_left= TextDisplay.TextDisplay(self.display, text="", maxlines = 17, x = self.center_w-self.center_w/2-140, y = self.center_h-240)
        self.text_right= TextDisplay.TextDisplay(self.display, text="", maxlines = 17, x = self.center_w+self.center_w/2-140, y = self.center_h-240)

        self.text_title1 = TextDisplay.TextDisplay(self.display, text="", lineheight=27, x = self.center_w-self.center_w/2-140, y = self.center_h-340, fontsize=35)
        self.text_title2 = TextDisplay.TextDisplay(self.display, text="", lineheight=27, x = self.center_w+self.center_w/2-140, y = self.center_h-340, fontsize=35)

        self.stats = TextDisplay.TextDisplay(self.display, text="", width = 27, x = self.center_w-135, y = self.center_h-240, fontsize=20)


        self.game_group = pygame.sprite.Group()
        self.game_group.add(self.question_button_left, self.question_button_right)

        #end_screen

        #quit

    def text_update(self, func, txt):
        func.update(txt)
        func.render()

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
            self.wikiimage.nextFrame()

    def game_screen_loop(self, ans = 1, start1 = "cat", start2 = "dog"):

        print("THIS IS THE LOOP HAPPENING")

        self.display.blit(self.game_background.image, self.game_background.rect.center)

        # self.health: lives = 3 
        # self.correct: num_correct = 0
        # round_count = 1

        #name of the wiki pages:
        page1 = start1
        page2 = start2
        #game_over = False

        wiki1 = info.Wikipedia("Cat")
        wiki2 = info.Wikipedia("Dog")

        #game = Controller.Controller(page1 + "\n" + wiki1.summary(), page2 + "\n" + wiki2.summary())

        #game.start_menu_loop()

        answer = ans
        iteration = 150
        round_count = 1
        proceed = False
        #self.set_text_left("this is test text this is test text this is test text this is test text this is test text this is test text")
        #self.set_text_right("this is test text this is test text this is test text this is test text this is test text this is test text")
        self.text_update(self.text_left, wiki1.summary())
        self.text_update(self.text_right, wiki2.summary())
        self.text_update(self.text_title1, page1)
        self.text_update(self.text_title2, page2)
        self.text_update(self.stats, "Guess Which Wikipedia      Article has more links to other Articles!"+" "*26+"           Try to Guess right 5 times before losing all of your health!"+" "*((26-7) + 26)+"Health: " + str(self.health) + " "*16 + "Number Guessed Correctly:" + str(self.correct))



        while self.STATE == "game":
            if (self.health < 0):
                self.health = 0

            if (round_count != 1 and self.health > 0 and self.correct < 5):
                iteration += 1
                self.display.blit(self.game_background.image, self.game_background.rect.center)
                self.game_group.draw(self.display)
                self.window.blit(self.display, (0,0))
                page1 = rand_links1
                page2 = rand_links2
                page1 += " "*30 #this is temp until i get the code
                page2 += " "*30
                self.text_update(self.text_left, wiki1.summary())
                self.text_update(self.text_right, wiki2.summary())
                self.text_update(self.text_title1, page1)
                self.text_update(self.text_title2, page2)
                self.text_update(self.stats, "Guess Which Wikipedia      Article has more links to other Articles!"+" "*26+"           Try to Guess right 5 times before losing all of your health!"+" "*((26-7) + 26)+"Health: " + str(self.health) + " "*16 + "Number Guessed Correctly:" + str(self.correct))
                #print(f"WIKI PAGE 1: {page1}")
                #print(f"WIKI PAGE 2: {page2}")

            if self.button_click_delta == 0:
                self.question_button_right.setFrame(0)
                self.question_button_left.setFrame(0)
            else:
                self.button_click_delta -=1
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #buttons
                    if(self.question_button_right.rect.collidepoint(event.pos) and answer == 2 and iteration > 7):
                        self.question_button_right.setFrame(1)
                        self.button_click_delta = 10
                        self.correct += 1
                        #self.STATE = None
                        print(self.STATE)
                        proceed = True
                        iteration = 0
                        #Add guessing functionality
                    elif(self.question_button_left.rect.collidepoint(event.pos) and answer == 1 and iteration > 7):
                        self.question_button_left.setFrame(1)
                        self.button_click_delta = 10
                        self.correct += 1
                        #self.STATE = None
                        print(self.STATE)
                        proceed = True
                        iteration = 0
                        #Add guessing functionality
                    elif(self.question_button_left.rect.collidepoint(event.pos) and answer == 2 and iteration > 7): 
                        self.question_button_right.setFrame(1)
                        self.button_click_delta = 10
                        self.health -= 1
                        #self.STATE = None
                        proceed = True
                        iteration = 0
                        print(self.STATE)
                    elif(self.question_button_right.rect.collidepoint(event.pos) and answer == 1 and iteration > 7): 
                        self.question_button_right.setFrame(1)
                        self.button_click_delta = 10
                        self.health -= 1
                        #self.STATE = None
                        proceed = True
                        iteration = 0
                        print(self.STATE)
                if event.type == pygame.QUIT:
                    self.STATE = "quit"
                self.game_group.draw(self.display)
                self.text_left.render()
                self.text_right.render()
                self.text_title1.render()
                self.text_title2.render()
                self.stats.render()
                self.window.blit(self.display, (0,0))
                pygame.display.update()
            self.clock.tick(self.tick)

            if (self.health <= 0):
                self.stats = TextDisplay.TextDisplay(self.display, text="", width = 27, x = self.center_w-135, y = self.center_h-240, fontsize=35)
                self.display.blit(self.game_background.image, self.game_background.rect.center)
                self.game_group.draw(self.display)
                self.window.blit(self.display, (0,0))
                self.text_update(self.stats, "You Lose!"+ " "*(int((26-4)*3.2)) + "Health: " + str(self.health) + " "*(int(16*4.35)) + "Number Guessed"+" "*(int(12*3.2))+"Correctly:" + str(self.correct))
                #self.STATE = "end"
            elif (self.correct >= 5):
                self.stats = TextDisplay.TextDisplay(self.display, text="", width = 27, x = self.center_w-135, y = self.center_h-240, fontsize=35)
                self.display.blit(self.game_background.image, self.game_background.rect.center)
                self.game_group.draw(self.display)
                self.window.blit(self.display, (0,0))
                self.text_update(self.stats, "You Win!" + " "*(int((26-3)*3.1)) + "Health: " + str(self.health) + " "*(int(16*4.35)) + "Number Guessed"+" "*(int(12*3.2))+"Correctly:" + str(self.correct))
                
                self.window.blit(self.caticon,(50, 50))
                pygame.display.update()                                     #CATICON!


            wiki1 = info.Wikipedia(page1.strip())
            wiki2 = info.Wikipedia(page2.strip()) #this is temp, get rid of strip

            if (proceed):
                print(f"Health: {self.health}")
                print(f"Num Correct: {self.correct}")

                links1 = wiki1.links()[1]
                links2 = wiki2.links()[1]

                #print(f"LINKS 1: {links1}")
                #print(f"WIKI: {wiki1}")

                #Selects a random link from one of the pages:
                rand_links1 = wiki1.randomlinks(1)[0][0]
                rand_links2 = wiki2.randomlinks(1)[0][0]

                

                #produces what the correct answer is:
                answer = None
                if (links1 > links2):
                    answer = 1
                else:
                    answer = 2

                #gets rid of the '/wiki/' text from the rand_links variables so it can 
                #be used in the Wikipedia class again for the next iteration of the loop
                rand_links1 = rand_links1[6:]
                rand_links2 = rand_links2[6:]

                self.text_left= TextDisplay.TextDisplay(self.display, text="", maxlines = 17, x = self.center_w-self.center_w/2-140, y = self.center_h-240)
                self.text_right= TextDisplay.TextDisplay(self.display, text="", maxlines = 17, x = self.center_w+self.center_w/2-140, y = self.center_h-240)

                self.text_title1 = TextDisplay.TextDisplay(self.display, text="", width = 24, lineheight=27, x = self.center_w-self.center_w/2-140, y = self.center_h-340, fontsize=35)
                self.text_title2 = TextDisplay.TextDisplay(self.display, text="",width = 24, lineheight=27, x = self.center_w+self.center_w/2-140, y = self.center_h-340, fontsize=35)

                round_count += 1
                proceed = False
            print(iteration)
            
            
    def end_screen_loop(self):
        while self.STATE == "end":
            pass
    def exit_loop(self):
        pygame.display.quit()
        pygame.quit()

"""
game = Controller()
game.set_text_right("pancakes and waffles are good with blueberries and strawberries")
game.set_text_left("pancakes and waffles are good with blueberries and strawberries")


game.mainloop()
"""
