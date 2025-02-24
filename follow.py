import pygame
from random import randint
from sys import exit
from math import sin

# Initializing
pygame.init()

#Constant variables
fullscreen = False
SCREEN_SIZE = (800, 600)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
background_color = list(RED)
clock = pygame.time.Clock()
FPS = 60
follower_initialpos = [(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2), (0, 0), (SCREEN_SIZE[0], 0), (0, SCREEN_SIZE[1]), (SCREEN_SIZE[0], SCREEN_SIZE[1])]
follower_radius = 10
followers_speed = 5
font1_size = 70
font2_size = 28
starting_time_to_new_follower = 1000

#Not-so constant variable
time_to_new_follower = starting_time_to_new_follower # in miliseconds

#Texts
font1 = pygame.font.SysFont("comicsans", font1_size)
youlost = font1.render("You lost!", True, BLACK)
youlost_rect = youlost.get_rect(center=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2))

font2 = pygame.font.SysFont("comicsans", font2_size)
playagain = font2.render("Press space to play again", True, BLACK)
playagain_rect = playagain.get_rect(center=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2 + font1_size/2 + 10))

letsstart = font1.render("Follower", True, BLACK)
letsstart_rect = letsstart.get_rect(center=(SCREEN_SIZE[0]/2, 100))

tutorial1 = font2.render("Avoid the circles using the mouse", True, WHITE)
tutorial1_rect = tutorial1.get_rect(center=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2 + font1_size/2 - 20))
tutorial2 = font2.render("Press space to start", True, WHITE)
tutorial2_rect = tutorial2.get_rect(center=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2 + font1_size/2 - 20 + font2_size))

#Time control
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, time_to_new_follower * 1000)

#Display
wn = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Follower")

def toggle_fullscreen():
    global fullscreen
    global wn
    global SCREEN_SIZE
    global follower_initialpos, youlost_rect, playagain_rect, letsstart_rect, tutorial1_rect, tutorial2_rect
    fullscreen = not fullscreen
    if fullscreen:
        wn = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        wn = pygame.display.set_mode(SCREEN_SIZE)
    
    #Variables transform
    follower_initialpos = [(pygame.display.get_window_size()[0]/2, pygame.display.get_window_size()[1]/2), (0, 0), (pygame.display.get_window_size()[0], 0), (0, pygame.display.get_window_size()[1]), (pygame.display.get_window_size()[0], pygame.display.get_window_size()[1])]
    youlost_rect = youlost.get_rect(center=(pygame.display.get_window_size()[0]/2, pygame.display.get_window_size()[1]/2))
    playagain_rect = playagain.get_rect(center=(pygame.display.get_window_size()[0]/2, pygame.display.get_window_size()[1]/2 + font1_size/2 + 10))
    letsstart_rect = letsstart.get_rect(center=(pygame.display.get_window_size()[0]/2, 100))
    tutorial1_rect = tutorial1.get_rect(center=(pygame.display.get_window_size()[0]/2, pygame.display.get_window_size()[1]/2 + font1_size/2 - 20))
    tutorial2_rect = tutorial2.get_rect(center=(pygame.display.get_window_size()[0]/2, pygame.display.get_window_size()[1]/2 + font1_size/2 - 20 + font2_size))



#Follower
class Follower:
    def __init__(self, pos, radius, speed):
        self.pos = [pos[0], pos[1]]
        self.radius = radius
        self.speed = speed
    
    def draw(self, color):
        pygame.draw.circle(wn, color, (self.pos[0], self.pos[1]), follower_radius)

    def move(self):
        mouse_pos = pygame.mouse.get_pos()
        self.diff_x = mouse_pos[0] - self.pos[0]
        self.diff_y = mouse_pos[1] - self.pos[1]
        self.diff = (self.diff_x**2 + self.diff_y**2) ** (1/2)
        self.pos[0] += (self.diff_x / self.diff) * self.speed
        self.pos[1] += (self.diff_y / self.diff) * self.speed
    
    def check_collision(self):
        if self.diff <= self.radius:
            game_over()

def create_follower(pos):
    global time_to_new_follower
    followers_list.append(Follower(pos, follower_radius, followers_speed * randint(90, 135) / 100)) #each circle has a different speed, slightly different from the followers_speed variable
    time_to_new_follower = round(time_to_new_follower * 0.988) #as times passes, new circles are created more frequently
    pygame.time.set_timer(TIMER_EVENT, time_to_new_follower)

#Transitions
def background_fade_white():
    while background_color[1] != 255:
        wn.fill(background_color)
        clock.tick(FPS)
        pygame.display.update()

        background_color[1] += 5
        background_color[2] += 5

def background_fade_red():
    while background_color[1] != 0:
        wn.fill(background_color)
        clock.tick(FPS)    
        pygame.display.update()

        background_color[1] -= 5
        background_color[2] -= 5

#Game Over
def game_over():
    start_ticks = pygame.time.get_ticks()
    global background_color
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                #Screen gets white smoothly
                background_fade_white()
                game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                toggle_fullscreen()
        
        #Screen gets red smoothly
        background_fade_red()
        wn.fill(background_color)
        current_ticks = pygame.time.get_ticks()

        #Game over message
        wn.blit(youlost, youlost_rect)
        if current_ticks - start_ticks >= 1700: #shows play again after 1700 miliseconds
            wn.blit(playagain, playagain_rect)

        display_points(font1_size + font2_size + 10)
        clock.tick(FPS)
        pygame.display.update()

#When game starts
def game_start():
    starting_follower = Follower((0, SCREEN_SIZE[1]/3), follower_radius, followers_speed)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                background_fade_white()
                game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                toggle_fullscreen()
        
        wn.fill(background_color)
        if starting_follower.pos[0] >= SCREEN_SIZE[0]:
            starting_follower.pos[0] = 0
        
        #EASTER EGG
        mouse_pos = pygame.mouse.get_pos()
        if ((mouse_pos[0] - starting_follower.pos[0])**2 + (mouse_pos[1] - starting_follower.pos[1])**2) ** (1/2) <= starting_follower.radius + 10:
            starting_follower.draw(BLACK)
        else:
            starting_follower.draw(WHITE)

        starting_follower.pos[0] += 2.5
        starting_follower.pos[1] = 30 * sin(starting_follower.pos[0] / 25) + 100
        
        wn.blit(letsstart, letsstart_rect)
        wn.blit(tutorial1, tutorial1_rect)
        wn.blit(tutorial2, tutorial2_rect)
        
        clock.tick(FPS)
        pygame.display.update()

def display_points(y_var):
    global points
    points_txt = font2.render(str(points), True, GRAY)
    points_rect = points_txt.get_rect(center=(pygame.display.get_window_size()[0]/2, pygame.display.get_window_size()[1]/2 + y_var))
    wn.blit(points_txt, points_rect)

#Main loop
def game():
    global followers_list
    global time_to_new_follower
    global points
    time_to_new_follower = 1000 #in miliseconds
    points = 0
    followers_list = []
    create_follower(follower_initialpos[0])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

            elif event.type == TIMER_EVENT:
                create_follower(follower_initialpos[randint(0, len(follower_initialpos) - 1)])
                points += 10

        wn.fill(background_color)

        display_points(0)

        for object in followers_list:
            object.move()
            object.draw(RED)
            object.check_collision()

        clock.tick(FPS)    
        pygame.display.update()

if __name__ == "__main__":
    game_start()