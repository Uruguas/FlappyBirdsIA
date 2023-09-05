# Import libraries
import pygame
import os
import random 
import neat 

# Setting up AI player and generation
ai_player = True
generation = 0

# Setting up screen dimensions 
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

# Loading images for the game
BARREL_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
FLOOR_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGES_BIRD = [
        pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
        pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
        pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),       
        ]

# Initializing pygame font and setting up font for points
pygame.font.init()
POINTS_FONT = pygame.font.SysFont('arial', 50)

# Class for Birds
class Bird: 
    IMGS = IMAGES_BIRD
    ROTATION_MAX = 25
    SPEED_ROTATION = 20
    TIME_ANIMATION = 5
    
    # Initializing bird with position and image
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.hight = self.y
        self.time = 0
        self.count_imagem = 0
        self.imagem = self.IMGS[0]
    
    # Function for bird to jump
    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.hight = self.y
        
    # Function for bird to move    
    def move(self):
        self.time += 1
        displacament = 1.5 * (self.time**2) + self.speed * self.time
        
        if displacament > 16:
            displacament = 16
        elif displacament < 0:
            displacament -= 2
                
        self.y += displacament
        
        if displacament < 0 or self.y < (self.hight + 50):
            if self.angle < self.ROTATION_MAX:
                self.angle = self.ROTATION_MAX
        else:
            if self.angle > -90:
                self.angle -= self.SPEED_ROTATION  
    
    # Function to paint the bird on the screen
    def paint(self, screen):
        self.count_imagem += 1
        
        if self.count_imagem < self.TIME_ANIMATION:
            self.imagem = self.IMGS[0]
        elif self.count_imagem < self.TIME_ANIMATION*2:
            self.imagem = self.IMGS[1]
        elif self.count_imagem < self.TIME_ANIMATION*3:
            self.imagem = self.IMGS[2]
        elif self.count_imagem < self.TIME_ANIMATION*4:
            self.imagem = self.IMGS[1]
        elif self.count_imagem < self.TIME_ANIMATION*4 + 1:
            self.imagem = self.IMGS[0]
            self.count_imagem = 0
            
        if self.angle <= -80:
            self.imagem = self.IMGS[1]
            self.count_image = self.TIME_ANIMATION*2
            
        image_rotation = pygame.transform.rotate(self.imagem, self.angle)
        pos_image_center = self.imagem.get_rect(topleft=(self.x, self.y)).center
        rectangle = image_rotation.get_rect(center=pos_image_center)
        screen.blit(image_rotation, rectangle.topleft)
    
    # Function to get mask of the bird image
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)
        
# Class for Barrel        
class Barrel:
    distance = 200
    speed = 5
    
    # Initializing barrel with position and image
    def __init__(self, x):
        self.x = x
        self.hight = 0
        self.pos_top = 0
        self.pos_floor = 0
        self.BARREL_TOP = pygame.transform.flip(BARREL_IMAGE, False, True)
        self.BARREL_FLOOR = BARREL_IMAGE
        self.happened = False
        self.def_hight() 
        
    # Function to define height of the barrel
    def def_hight(self):
        self.hight = random.randrange(50, 450)
        self.pos_top = self.hight - self.BARREL_TOP.get_height()
        self.pos_floor = self.hight + self.distance
    
    # Function for move barrel
    def move(self):
        self.x -= self.speed
    
    ## Function to paint the barrel on the screen
    def paint(self, screen):
        screen.blit(self.BARREL_TOP, (self.x, self.pos_top))
        screen.blit(self.BARREL_FLOOR, (self.x, self.pos_floor))
    
    # Function to check collision with the bird
    def collide(self, bird):
        BIRD_IMAGE_mask = bird.get_mask()
        
        top_mask = pygame.mask.from_surface(self.BARREL_TOP)
        base_mask = pygame.mask.from_surface(self.BARREL_FLOOR)
        
        distance_top = (self.x - bird.x, self.pos_top - round(bird.y))
        distance_floor = (self.x - bird.x, self.pos_floor - round(bird.y))
        
        top_point = BIRD_IMAGE_mask.overlap(top_mask, distance_top)
        base_point = BIRD_IMAGE_mask.overlap(base_mask, distance_floor)

        if base_point or top_point:
            return True
        else:
            return False

# Class for floor
class Floor:
    SPEED = 5
    WIDTH = FLOOR_IMAGE.get_width()
    IMAGEM = FLOOR_IMAGE
    
    # Initializing floor with position and image
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        
    # Function for floor to move
    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED
        
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH # WATCH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    # Function to paint the floor on the screen        
    def paint(self, screen):
        screen.blit(self.IMAGEM, (self.x1, self.y))
        screen.blit(self.IMAGEM, (self.x2, self.y))

# Function to paint the screen
def paint_screen(screen, birds, barrels, floor, points):
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    for bird in birds:
        bird.paint(screen) 
    for barrel in barrels:
        barrel.paint(screen)       
        
    text = POINTS_FONT.render(f'Points: {points}', 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
    if ai_player:
         text = POINTS_FONT.render(f'Geração: {generation}', 1, (255, 255, 255))
         screen.blit(text, (10, 10))
    floor.paint(screen)
    pygame.display.update()
    
    
    
def main(genomes, config): # Main function for the game
    global generation
    generation += 1
    
    if ai_player:
        nets = []
        list_genomes = []
        birds = []
        for _, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            genome.fitness = 0
            list_genomes.append(genome)
            birds.append(Bird(230, 350))
    else: 
         birds  = [Bird(230, 350)]
    floor = Floor(730)
    barrels = [Barrel(700)]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    points = 0
    watch = pygame.time.Clock()
    
    # Game loop
    runing = True
    while runing:
        watch.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False
                pygame.quit()
                quit()
            if not ai_player:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for bird in birds:
                            bird.jump()
        index_barrel = 0
        if len(birds) > 0:
            if len(barrels) > 1 and birds[0].x > (barrels[0].x + barrels[0].BARREL_TOP.get_width()):
                index_barrel = 1
        else: 
            runing = False
            break    
        for i, bird in enumerate(birds):
            bird.move()
            list_genomes[i].fitness += 0.1
            output = nets[i].activate((bird.y, 
                                       abs(bird.y - barrels[index_barrel].hight), 
                                       abs(bird.y - barrels[index_barrel].pos_floor)))
            # -1 e 1 --> If output > 0.5 then brid jump
            if output[0] > 0.5:
                bird.jump()
        floor.move()
        
        add_barrel = False
        remove_barrel = []
        for barrel in barrels:
            for i, bird in enumerate(birds):
                if barrel.collide(bird):
                    birds.pop(i)
                    if ai_player:
                        list_genomes[i].fitness -= 1
                        list_genomes.pop(i)
                        nets.pop(i)
                if not barrel.happened and bird.x > barrel.x:
                    barrel.happened = True
                    add_barrel = True
            barrel.move()
            if barrel.x + barrel.BARREL_TOP.get_width() < 0:
                remove_barrel.append(barrel)          
                
        if add_barrel:
            points += 1
            barrels.append(Barrel(600))
            for genome in list_genomes:
                genome.fitness += 5
        for barrel in remove_barrel: 
            barrels.remove(barrel)
        
        for i, bird in enumerate(birds):
            if (bird.y + bird.imagem.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)
                if ai_player:
                    list_genomes.pop(i)
                    nets.pop(i)
                
        paint_screen(screen, birds, barrels, floor, points)            
    
def running(adress_config):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                adress_config)
    
    population  = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    
    if ai_player:
        population.run(main, 50)  
    else:
        main(None, None)
if __name__ == '__main__':
    adress = os.path.dirname(__file__)
    adress_config = os.path.join(adress,'config.txt') 
    running(adress_config)