import pygame

'''
Class displays text to a certain width and shifts to new lines, and allows updating of existing text with new.
'''

class TextDisplay:
    def __init__(self, surface, text="test", width = 32, maxlines = 10, lineheight = 15, fontsize = 20, color = (0,0,0), x = 0, y = 0):
        #Variables
        self.surface = surface
        self.width = width
        self.maxlines = maxlines
        self.lineheight = lineheight
        self.fontsize = fontsize
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont("timesnewroman", fontsize)
        #Text sizing
        textline = ""
        self.textlines = []
        lastpos = 0
        for index,i in enumerate(text):    
            if index+1-lastpos<self.width:
                textline += i
                if index==len(text)-1:
                    self.textlines.append(textline) 
            elif len(self.textlines)<self.maxlines:
                lastpos = index
                textline += i
                self.textlines.append(textline)
                textline = ""

    def update(self,text):
        #Text sizing
        textline = ""
        self.textlines = []
        lastpos = 0
        for index,i in enumerate(text):    
            if index+1-lastpos<self.width:
                textline += i
                if index==len(text)-1:
                    self.textlines.append(textline) 
            elif len(self.textlines)<self.maxlines:
                lastpos = index
                textline += i
                self.textlines.append(textline)
                textline = ""

    def render(self):
        for index, i in enumerate(self.textlines):
            self.surface.blit(self.font.render(i, True, self.color),(self.x,self.y+((index)*self.lineheight)))