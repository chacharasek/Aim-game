import pygame
 
 
SIZE = WIDTH, HEIGHT = 750, 750 #the width and height of our screen
BACKGROUND_COLOR = pygame.Color('white') #The background colod of our window
FPS = 50 #Frames per second
 
class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        super(MySprite, self).__init__()
 
        self.images = []
        self.images.append(pygame.image.load('nyan_cat\\1.png'))
        self.images.append(pygame.image.load('nyan_cat\\2.png'))
        self.images.append(pygame.image.load('nyan_cat\\3.png'))
        self.images.append(pygame.image.load('nyan_cat\\4.png'))
        self.images.append(pygame.image.load('nyan_cat\\5.png'))
        self.images.append(pygame.image.load('nyan_cat\\6.png'))
        self.images.append(pygame.image.load('nyan_cat\\7.png'))
        self.images.append(pygame.image.load('nyan_cat\\8.png'))
        self.images.append(pygame.image.load('nyan_cat\\9.png'))
        self.images.append(pygame.image.load('nyan_cat\\10.png'))
        self.images.append(pygame.image.load('nyan_cat\\11.png'))
        self.images.append(pygame.image.load('nyan_cat\\12.png'))
 
        self.index = 0
 
        self.image = self.images[self.index]
 
        self.rect = pygame.Rect(5, 5, 150, 198)
 
    def update(self):
        self.index += 1
 
        if self.index >= len(self.images):
            self.index = 0
        
        self.image = self.images[self.index]
 
def bg1():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    my_sprite = MySprite()
    my_group = pygame.sprite.Group(my_sprite)
    clock = pygame.time.Clock()
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
        my_group.update()
        screen.fill(BACKGROUND_COLOR)
        my_group.draw(screen)
        pygame.display.update()
        clock.tick(20)