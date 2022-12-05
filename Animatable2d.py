import pygame

class Object(pygame.sprite.Sprite):
    
    def __init__(self, img_array, w, h, xpos = 0, ypos = 0, getres = True, start_frame = 0, end_frame = 0):
        '''
        Object class
        Args: [image], start_frame, xpos, ypos, height, width, end_frame
        '''
        pygame.sprite.Sprite.__init__(self)
        self.img_array = img_array #image filename array
        self.x = int(xpos)
        self.y = int(ypos)
        self.image = pygame.image.load(self.img_array[start_frame]).convert()
        if(getres):
            self.width = int(self.image.get_size()[0]*w)
            self.height = int(self.image.get_size()[1]*h)
        else:
            self.width = w
            self.height = h
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        self.img_count = len(self.img_array)-1

        if(end_frame == 0):
            self.end_frame = self.img_count
        else: 
            self.end_frame = end_frame
        self.current_frame = 0
       
    def nextFrame(self):
        '''
        Method: nextFrame, updates to next frame
        Args: self
        Returns: none
        '''
        if(self.current_frame < self.end_frame):
            self.current_frame += 1
        else:
            self.current_frame = 0
        self.image = pygame.image.load(self.img_array[self.current_frame]).convert()
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        

    def setFrame(self,frame_number):
        '''
        Method: setFrame, sets the animation to a certain frame.
        Args: self, frame_number (int)
        Returns: none
        '''
        self.current_frame = frame_number
        self.image = pygame.image.load(self.img_array[frame_number]).convert()
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

    def move(self, x , y):
        '''
        Method: move, moves object to new coord
        Args: self, x ,y
        Returns: none
        '''
        self.x, self.y = x,y
        self.rect.center = (x,y)
    
    def setsize(self, width, height):
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.rect = self.image.get_rect()
        
    def __str__(self):
        '''
        Method: str, overwrites str
        Args: self
        Returns: string
        '''
        string = "(x: {}, y:{}) width: {}, height: {}"
        return string