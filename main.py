import pygame
import bin.Controller

def main():
    pygame.init()
    game = bin.Controller.Controller()
    game.mainloop()

main()