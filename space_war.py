# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1000
HEIGHT = 1000
SIZE = (WIDTH, HEIGHT)
TITLE = "Tribe War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (16, 96, 0)


# Fonts
FONT_XS = pygame.font.Font("assets/fonts/RINGM.ttf", 16)
FONT_SM = pygame.font.Font("assets/fonts/RINGM.ttf", 24)
FONT_MD = pygame.font.Font("assets/fonts/RINGM.ttf", 32)
FONT_LG = pygame.font.Font("assets/fonts/RINGM.ttf", 64)
FONT_XL = pygame.font.Font("assets/fonts/RINGM.ttf", 96)
FONT_XXL = pygame.font.Font("assets/fonts/RINGM.ttf", 115)


# Images
ship_img = pygame.image.load('assets/images/Dragon.png').convert_alpha()
ship_img = pygame.transform.scale(ship_img, (150, 149))
ship_damage1_img = pygame.image.load('assets/images/Dragon damage1.png').convert_alpha()
ship_damage1_img = pygame.transform.scale (ship_damage1_img, (150, 149))
ship_damage2_img = pygame.image.load('assets/images/Dragon damage2.png').convert_alpha()
ship_damage2_img = pygame.transform.scale (ship_damage2_img, (150, 149))
laser_img = pygame.image.load('assets/images/Fireball.png')
enemy_img = pygame.image.load('assets/images/Dragon ENEMY.png')
enemy_img = pygame.transform.scale(enemy_img, (100, 99))
bomb_img = pygame.image.load('assets/images/Fireball ENEMY.png')
landscape_river = pygame.image.load('assets/images/Background/rocks.jpg')
landscape_river = pygame.transform.scale(landscape_river, (1200, 1000))
cloud_img = pygame.image.load('assets/images/Background/cloud.png')
cloud_img = pygame.transform.scale(cloud_img, (250, 145))
redscale = pygame.image.load('assets/images/dragon_FRONT.png')

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/hit.ogg')
PEW = pygame.mixer.Sound('assets/sounds/Fire.ogg')
HIT = pygame.mixer.Sound('assets/sounds/hit.wav')

pygame.mixer.music.load('assets/sounds/Second_Strike.WAV')

# game stats

score = 0

# Stages
START = 0
PLAYING = 1
WIN = 2
LOSE = 3

# Make picture

num_clouds = 10
clouds = []
for i in range(num_clouds):
    x = random.randrange(0, 1800)
    y = random.randrange(0, 1000)
    c = [x, y]
    clouds.append(c)

# Game classes
class Ship(pygame.sprite.Sprite):
        
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.shield = 3
        
        self.speed = 7

    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def shoot(self):

        PEW.play()
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self):

        global stage
        
        if self.rect.left < 0:
            self.rect.left= 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        '''check bombs'''
        hit_list = pygame.sprite.spritecollide(self, bombs, True,
                                               pygame.sprite.collide_mask)
        hit_list1 = pygame.sprite.spritecollide(self, mobs, False,
                                               pygame.sprite.collide_mask)
        
        for hit in hit_list:
            HIT.play()
            self.shield -= 1

        if self.shield == 2:
            self.image = ship_damage1_img

        elif self.shield == 1:
            self.image = ship_damage2_img

        elif self.shield == 0:
            self.kill()
            stage = LOSE
            

class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.speed = 12

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        
        PEW.play()
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def draw_mobs(self):
        
        mob1 = Mob(50, 50, enemy_img)
        mob2 = Mob(200, 50, enemy_img)
        mob3 = Mob(350, 50, enemy_img)
        mob4 = Mob(500, 50, enemy_img)
        mob5 = Mob(650, 50, enemy_img)
        mob6 = Mob(800, 50, enemy_img)
        mob7 = Mob(125, 150, enemy_img)
        mob8 = Mob(250, 150, enemy_img)
        mob9 = Mob(375, 150, enemy_img)
        mob10 = Mob(500, 150, enemy_img)
        mob11 = Mob(625, 150, enemy_img)
        mob12 = Mob(750, 150, enemy_img)

        mobs.add(mob1, mob2, mob3, mob4, mob5, mob6,
                 mob7, mob8, mob9, mob10, mob11, mob12)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)

        global score, stage

        if len(hit_list) > 0:
            self.kill()
            score += 1
            EXPLOSION.play()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.speed = 6

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 8
        self.moving_right = True
        self.down_speed = 18

        self.bomb_rate = 45 #lower is faster

        self.wave_num = 0

    def move(self):
        hits_edge = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True

            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            self.move_down()


    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.down_speed

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
           bomber = random.choice(mob_list)
           bomber.drop_bomb()

    def update(self):
        self.move()
        self.choose_bomber()

        if len(mobs) == 0:
            self.wave_num += 1
            self.bomb_rate -= 5
            self.down_speed += 3
            if self.bomb_rate < 1:
                self.bomb_rate = 1
            
            Mob.draw_mobs(Mob)

# Game helper functions
def stages():
    
    global stage
    
    if stage == START:
        show_title_screen()
    elif stage == LOSE:
        show_lose()
        
def show_title_screen():
    pygame.draw.rect(screen, BLACK, [0, 0, WIDTH, HEIGHT])
    title_text = FONT_XL.render("Tribe War!", 1, WHITE)
    screen.blit(title_text, [250, 200])
    screen.blit(redscale, [175, 250])

def check_end():
    global stage

    if len(mobs) == 0:
        stage = WIN
    elif len(player) == 0:
        stage = LOSE

def show_lose():
    pygame.draw.rect(screen, BLACK, [0, 0, WIDTH, HEIGHT])
    text4 = FONT_LG.render("Game Over!", True, WHITE)
    screen.blit(text4, [300, 400])

def setup():
    global stage, done
    global player, ship, lasers, mobs, bombs, fleet

    score = 0
    
    ''' Make game objects '''
    ship = Ship(ship_img)
    ship.rect.centerx = WIDTH / 2
    ship.rect.bottom = HEIGHT - 20

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    fleet = Fleet(mobs)

    ''' set stage '''
    stage = START
    done = False

def draw_cloud(loc):
    x = loc[0]
    y = loc[1]

    screen.blit(cloud_img, (x, y))

def update_clouds():
    for c in clouds:
        c[0] += 2

        if c[0] > 1000:
            c[0] = random.randrange(-1000, -100)
            c[1] = random.randrange(0, 900)

def display_stats():
    score_txt = FONT_MD.render(str(score), 1, WHITE)
    screen.blit(score_txt, [10, 10])

    score_txt2 = FONT_XS.render("score", 1, WHITE)
    screen.blit(score_txt2, [940, 18])

    shield_txt = FONT_MD.render(str(ship.shield), 1, WHITE)
    screen.blit(shield_txt, [10, 50])

    shield_txt2 = FONT_XS.render("health", 1, WHITE)
    screen.blit(shield_txt2, [930, 60])

    wave_txt = FONT_MD.render(str(fleet.wave_num), 1, WHITE)
    screen.blit(wave_txt, [10, 90])

    wave_txt2 = FONT_XS.render("wave", 1, WHITE)
    screen.blit(wave_txt2, [940, 102])

pygame.mixer.music.play(-1)
 
# Game loop
setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if pygame.K_q:
                pygame.QUIT
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING

            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()

            elif stage == LOSE:
                if event.key == pygame.K_SPACE:
                    setup()
                    stage = START

    pressed = pygame.key.get_pressed()
    
    if stage == PLAYING:
        if pressed[pygame.K_a]:
            ship.move_left()
        elif pressed[pygame.K_d]:
            ship.move_right()
        elif pressed[pygame.K_w]:
            ship.move_up()
        elif pressed [pygame.K_s]:
            ship.move_down()
    
    # Game logic (Check for collisions, update points, etc.)    
    if stage == PLAYING:
        player.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()
        update_clouds()
        stages()

        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
        screen.fill(GREEN)
        screen.blit(landscape_river, (0, 0))
        for c in clouds:
            draw_cloud(c)
        lasers.draw(screen)
        bombs.draw(screen)
        player.draw(screen)
        mobs.draw(screen)
        display_stats()
        
    if stage == START:
        show_title_screen()
    elif stage == LOSE:
        show_lose()

        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
