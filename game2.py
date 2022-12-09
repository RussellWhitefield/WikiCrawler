from bin import Controller

answer = 1

page1 = "Cat"
page2 = "Dog"

game = Controller.Controller()

game.start_menu_loop()
game.game_screen_loop(answer, page1, page2)
print("ok")


#game.mainloop(answer, page1, page2)
