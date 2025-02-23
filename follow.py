import pygame
from random import randint
from sys import exit

# Initializing
pygame.init()

#Constant variables
SCREEN_SIZE = (800, 600)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
background_color = list(WHITE)
clock = pygame.time.Clock()
FPS = 60
follower_initialpos = [(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2), (0, 0), (SCREEN_SIZE[0], 0), (0, SCREEN_SIZE[1]), (SCREEN_SIZE[0], SCREEN_SIZE[1])]
follower_radius = 10
followers_speed = 5
font1_size = 70
font2_size = 28

#Not-so constant variable
time_to_new_follower = 1000 # in miliseconds

#Game over text
font1 = pygame.font.SysFont("comicsans", font1_size)
youlost = font1.render("You lost!", True, BLACK)
youlost_rect = youlost.get_rect(center=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2))

font2 = pygame.font.SysFont("comicsans", font2_size)
playagain = font2.render("Press space to play again", True, BLACK)
playagain_rect = playagain.get_rect(center=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2 + font1_size/2 + 10))

#Time control
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, time_to_new_follower * 1000)

#Display
wn = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Every Breath You Take...")

#Follower
class Follower:
    def __init__(self, pos, radius, speed):
        self.pos = [pos[0], pos[1]]
        self.radius = radius
        self.speed = speed
    
    def draw(self):
        pygame.draw.circle(wn, RED, (self.pos[0], self.pos[1]), follower_radius)

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
    followers_list.append(Follower(pos, follower_radius, followers_speed * randint(90, 130) / 100))
    time_to_new_follower = round(time_to_new_follower * 0.99)
    pygame.time.set_timer(TIMER_EVENT, time_to_new_follower)

#Game Over
def game_over():
    global background_color
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                #Screen gets white smoothly

                while background_color[1] != 255:
                    wn.fill(background_color)
                    clock.tick(FPS)
                    pygame.display.update()

                    background_color[1] += 5
                    background_color[2] += 5

                game()
        
        #Screen gets red smoothly
        while background_color[1] != 0:
            wn.fill(background_color)
            clock.tick(FPS)    
            pygame.display.update()

            background_color[1] -= 5
            background_color[2] -= 5

        #Game over message
        wn.blit(youlost, youlost_rect)
        wn.blit(playagain, playagain_rect)
        clock.tick(FPS)
        pygame.display.update()

#Main loop
def game():
    global followers_list
    followers_list = []
    create_follower(follower_initialpos[0])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

            elif event.type == TIMER_EVENT or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                create_follower(follower_initialpos[randint(0, len(follower_initialpos) - 1)])

        wn.fill(background_color)

        for object in followers_list:
            object.move()
            object.draw()
            object.check_collision()

        clock.tick(FPS)    
        pygame.display.update()


if __name__ == "__main__":
    game()