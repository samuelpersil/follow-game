import pygame #init

# Initializing
pygame.init()

#Constant variables
wnsize = (800, 600)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
speed = 5
clock = pygame.time.Clock()
FPS = 60

#Display
wn = pygame.display.set_mode(wnsize)
pygame.display.set_caption("Every Breath You Take...")

#Follower
follower_pos = [wnsize[0]/2, wnsize[1]/2]
follower_radius = 10
def move():
    global mouse_pos
    global follower_pos
    diff_x = mouse_pos[0] - follower_pos[0]
    diff_y = mouse_pos[1] - follower_pos[1]
    diff = (diff_x**2 + diff_y**2) ** (1/2)
    follower_pos[0] += (diff_x / diff) * speed
    follower_pos[1] += (diff_y / diff) * speed

#Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    mouse_pos = pygame.mouse.get_pos()
    move()

    wn.fill(WHITE)
    pygame.draw.circle(wn, RED, follower_pos, follower_radius)
    pygame.display.update()
    clock.tick(FPS)