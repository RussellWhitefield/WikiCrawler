import pygame

'''
Class displays text to a certain width and shifts to new lines, and allows updating of existing text with new.
'''

class TextDisplay:
    def __init__(self, text = "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Amet libero aliquam eius provident mollitia voluptatibus. Eos, eligendi quasi libero autem quo in velit molestias fugit distinctio rerum soluta corporis laudantium, consequuntur sequi? Aspernatur magni recusandae maiores id distinctio, debitis ipsam inventore autem sapiente doloremque, vitae facilis laboriosam! Nesciunt, quia ad!", width = 50, fontsize = 30, color = (0,0,0)):
        #Variables
        self.width = width
        self.fontsize = fontsize
        self.color = color
        #Text sizing
        formatted_text = ""
        for i in text:
            
            if len(text[0:i])<self.width:
                formatted_text.append(i)
            else:
                formatted_text.append("/n" + "-"+ i)
        #Fond and rendering
        self.font = pygame.font.SysFont("timesnewroman", fontsize)
        self.text = self.font.render(formatted_text, True, self.color)
        
    def update(self, text):
        #Text sizing
        formatted_text = ""
        for i in text:
            if len(text[0:i])<self.width:
                formatted_text.append(i)
            else:
                formatted_text.append("/n" + "-"+ i)
        #Updating text
        self.text = self.font.render(formatted_text, True, self.color, )