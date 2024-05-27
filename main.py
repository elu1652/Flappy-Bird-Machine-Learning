import neat.config
import neat.population
import pygame
from entities import Bird,Pipe
import neat
import time

#Set up window
window = (600,800)
background = pygame.image.load('bg.png')
screen = pygame.display.set_mode(window)
pygame.display.set_caption('Flappy Bird')
birdImage = pygame.image.load('bird3.png')
pipeImage = pygame.image.load('pipe3.png')

#Initialize bird
bird = Bird(200,400,birdImage)
pipe = Pipe(pipeImage)
pipes = [pipe]
score = 0

pygame.font.init()
font = pygame.font.SysFont('Calibri',30)

def reset():
    #Restart the game
    global bird 
    global pipe
    global pipes
    global score
    bird = Bird(200,400,birdImage)
    pipe = Pipe(pipeImage)
    pipes = [pipe]
    score = 0
    pygame.display.flip()


def grid():
    #Draw lines to locate coordinates
    pygame.draw.line(screen,(255,0,0),(0,400),(600,400))
    pygame.draw.line(screen,(255,0,0),(300,0),(300,800))
    pygame.draw.line(screen,(255,0,0),(0,200),(600,200))
    pygame.draw.line(screen,(255,0,0),(0,600),(600,600))
    pygame.draw.line(screen,(0,255,0),(0,300),(600,300))
    pygame.draw.line(screen,(0,255,0),(0,700),(600,700))
    pygame.draw.line(screen,(0,0,255),(100,0),(100,800))
 
def main(genomes,config):
    nets = []
    ge = []
    birds = []
    t0 = time.time()


    for genome_id,g in genomes:
        #Create neural network
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        #Create birds based on population config
        birds.append(Bird(200,400,birdImage))
        #Default starting fitness set to 0
        g.fitness = 0
        ge.append(g)

    collide = False
    global score
    while not collide:
        #Track time for fitness
        t1 = time.time()
        #Current pipe that is getting tracked
        current_pipe = pipes[-1]
        #Draw background
        screen.blit(background,(-100,0))
        #Draw bird
        
        #Stop if all birds die
        if len(birds) == 0:
            collide = True
            break

        for index, bird in enumerate(birds):
            #Draw and move birds
            bird.render(screen,background)
            bird.update()
            
            #Get inputs for nn and decide whether to jump or not
            dx = bird.x-current_pipe.x
            dy_bot = bird.y - current_pipe.y
            dy_top = bird.y - current_pipe.y-current_pipe.GAP
            net_input = (dx,dy_top,dy_bot)
            output = nets[index].activate(net_input)

            #Threshold for jumping
            if output[0] > 0.8:
                bird.move()

            #Calculate time alive for fitness
            dt = t1-t0
            ge[index].fitness = dt + bird.score

        #Check for collision and move each pipe
        for p in pipes[:]:
            if p.x >= -100:
                p.render(screen)
                p.move()
                for index,bird in enumerate(birds):
                    if bird.collide(p,screen):
                        #Remove bird if fail
                        birds.pop(index)
                        nets.pop(index)
                        ge.pop(index)
            else:
                #Remove pipes that are off the screen
                pipes.remove(p)

        #Create a new pipe once current pipe is passed through
        if not current_pipe.new and current_pipe.x <= 100:
            #Switch pipe that is tracked
            current_pipe = Pipe(pipeImage)
            pipes.append(current_pipe)
            #Increase bird score for passing pipe
            for bird in birds:
                bird.score += 1
            #Increase overall score for visual
            score += 1
        
        if len(birds) == 1:
            birds[0].lines(current_pipe,screen)

        #Display score
        text = font.render(str(score),False,(0,0,0))
        alive = font.render('Birds alive: ' + str(len(birds)),False,(0,0,0))
        screen.blit(text,(0,0))
        screen.blit (alive,(0,30))
        '''
        For manual control to play game
        #Detect if spacebar is pressed to move bird
        #bird.lines(current_pipe,screen)
        #bird.keyPress()
        #grid()
        '''
        pygame.display.flip()
    reset()


def learn(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)
    
    #Create population
    p = neat.population.Population(config)
    #Print data
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #Runs for 50 generation
    p.run(main,50)
    #Get best genome
    winner = stats.best_genome()

file = 'config.txt'
learn(file)