import pygame
import random
import neat
class Bird():
    
    def __init__(self,x,y,image):
        self.x = x
        self.y = y
        self.speed = 0.001

        self.angleMax = 30
        self.angleMin = -30
        self.speedMax = 1
        self.speedMin = -0.3

        self.image = image
        self.score = 0        

    def render(self,screen,background):

        #Gets rotated image
        rotated = self.rotate()

        #screen.blit(self.rotate(image),(center_x,center_y))
        screen.blit(rotated[0],rotated[1])
    
    def move(self):
        #Set speed to -0.5 if spacebar is pressed
        self.speed = self.speedMin
    
    def rotate(self):
        #Calculate angle based on speed
        angle = self.angleMin + ((self.speed-self.speedMax)*(self.angleMax-self.angleMin)/(self.speedMin-self.speedMax))
        rotated_image = pygame.transform.rotate(self.image,angle)
        new_rect = rotated_image.get_rect(center = self.image.get_rect(center = (self.x, self.y)).center)
        #Return proper image and rectangle
        return rotated_image,new_rect

    def update(self):
        #Cap speed at 1
        if self.speed < self.speedMax:
            self.speed += 0.001
        #Increase speed to simulate gravity
        self.y += self.speed
        self.center_x = self.x - (self.image.get_width()/2)
        self.center_y = self.y - (self.image.get_height()/2)
    
    def collide(self,pipe,screen):
        #Creates mask for bird and pipes
        bottomPipe,topPipe = pipe.getPipes()
        bird_mask = pygame.mask.from_surface(self.image)
        bottom_mask = pygame.mask.from_surface(bottomPipe)
        top_mask = pygame.mask.from_surface(topPipe)
        #Return true if masks overlap or bird is out of bounds
        if (bird_mask.overlap(bottom_mask,(pipe.x-self.center_x,pipe.y-self.center_y)) or bird_mask.overlap(top_mask,(pipe.x-self.center_x,pipe.top_y-self.center_y))
            or self.center_y <0 or self.center_y > 800):
            return True
        return False
    
    def keyPress(self):
    #Detects which events occur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #Update bird speed if spacebar is pressed
                    self.move()
    
    def lines(self,pipe,screen):
        #Visual design
        pygame.draw.line(screen,(255,0,0),(self.x,self.y),(pipe.x+(pipe.image.get_width()/2),pipe.y),2)
        pygame.draw.line(screen,(255,0,0),(self.x,self.y),(pipe.x+(pipe.image.get_width()/2),pipe.y-pipe.GAP),2)


class Pipe:
    GAP = 100
    SPEED = 0.3
    SPAWN = 600
    NEW = False
    def __init__(self,image):
        self.x = self.SPAWN
        #Randomize pipe height
        self.y = random.randint(300,700)
        self.new = False
        
        self.image = image
        self.top_y = self.y-self.GAP-self.image.get_height()
        
    def render(self,screen):
        bottomPipe,topPipe = self.getPipes()
        screen.blit(bottomPipe,(self.x,self.y))
        #Adjusts top pipe
        screen.blit(topPipe,(self.x,self.top_y))
    
    def getPipes(self):
        bottomPipe = self.image
        copy = self.image.copy()
        #Flips bottom pipe around to form top pipe
        topPipe = pygame.transform.flip(copy,False,True)
        #Returns bottom and top pipe images
        return bottomPipe,topPipe

    def move(self):
        self.x -= self.SPEED
    


        
        
        
