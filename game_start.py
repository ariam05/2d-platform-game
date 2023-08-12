import pygame, sys, maps, random
from player import Player
from enemy import Enemy
from items import Item
from particle import Particle
from pygame.locals import *
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Willo')
clock = pygame.time.Clock()


# Window Size set
WINDOW_HEIGHT = 1080
WINDOW_WIDTH = 1920
flags = pygame.FULLSCREEN
screen = pygame.display.set_mode(( WINDOW_WIDTH, WINDOW_HEIGHT), flags, 16)

# World Settings
background = pygame.image.load('Assets/Sprites/background.jpg').convert()
camera_offset = [0, 0]
gravity = 1
max_velocity_x = 10
max_velocity_y = 15
particles = []
score = 0
highscore = 0
font = pygame.font.Font('freesansbold.ttf', 25)
wave = 1
message_timer_max = 200
message_timer = message_timer_max
level_active = False
tile_one = pygame.image.load('Assets/Sprites/Tiles/tile_1.jpg').convert()
tile_two = pygame.image.load('Assets/Sprites/Tiles/tile_2.jpg').convert()
tile_three = pygame.image.load('Assets/Sprites/Tiles/tile_3.jpg').convert()
tile_size = 60

# Initialize "Player" Class
player = Player()
victory = False

# Background sound
pygame.mixer.music.load('Assets/Sounds/Myuu-Angst.mp3')
pygame.mixer.music.play(-1)

# highscore
def update_score(highscore, score):
    score = player.kills * 100 + player.coins_collected * 10
    if score > highscore:
        highscore = score
    return highscore, score

# Show Score
def show_score(x, y, highscore, score):
    screen.blit(font.render("Score: " + str(score), True, (255,255,255)), (x, y))
    screen.blit(font.render("High Score: " + str(highscore), True, (255,255,255)), (x, y+30)) #highscore display
# Enemy Spawn
def spawn_enemy():
    ran_spawn = random.randrange(1,3)
    if ran_spawn == 1:
        enemy_list = [Enemy(1955,1230),Enemy(2350,1230),Enemy(1650,1050)]
    elif ran_spawn == 2:
        enemy_list = [Enemy(1140,1290),Enemy(1290,750),Enemy(1955,1230),]
    elif ran_spawn == 3:
        enemy_list = [Enemy(2350,1230),Enemy(1290,750),Enemy(1650,1050),]
    enemies = enemy_list
    return enemies
enemies = []

# Item SpawnF
def spawn_item():
    items = [
        Item(930,870, "coin"),
        Item(1650,1050, "health"),
        Item(2220,1230, "coin"),
        Item(1555,510, "coin"),
        Item(815, 330, "health"),
        Item(495, 270, "coin"),
        Item(120, 930, "coin"),
    ]
    return items
items = spawn_item()

# Level Reset
def level_reset(player, victory, wave, level_active, enemies, items, message_timer, message_timer_max):
    player.coins_collected = 0
    player.kills = 0
    player.velocity_x = 0
    victory = False
    player.health = player.max_health
    player.alive = True
    player.x = 300
    player.y = 1000
    wave = 1
    level_active = False
    message_timer = message_timer_max
    enemies = []
    items = spawn_item()
    return victory, wave, level_active, enemies, items, message_timer


# FPS counter
def show_fps():
    screen.blit(font.render(str(int(clock.get_fps())), True, (255,255,255)), (WINDOW_WIDTH - 100, 100))

def main_menu():
    click = False
    def create_font(t, s=72, c=(255, 255, 255), b=False, i=False):
        font = pygame.font.Font('freesansbold.ttf', s, bold=b, italic=i)
        text = font.render(t, True, c)
        return text

    while True:

        screen.blit(background, (0,0))
        mouse = pygame.mouse.get_pos()
        start_game_text = create_font('Willo', s=100, b=True, c=(255, 255, 255))
        text_rect = start_game_text.get_rect(center=(int(WINDOW_WIDTH/2), 100))
        screen.blit(start_game_text, text_rect)
        start_game_text = create_font('PLAY', s=40, b=True, c=(255, 255, 255))
        text_rect = start_game_text.get_rect(center=(int(WINDOW_WIDTH/2), 350))
        button_1 = screen.blit(start_game_text, text_rect)
        quit_text = create_font('QUIT', s=40, b=True, c=(255, 255, 255))
        text_rect = quit_text.get_rect(center=(int(WINDOW_WIDTH/2), 425))
        button_2 = screen.blit(quit_text, text_rect)

        movement_text = create_font('Arrow Keys = Movement', s=30, b=True, c=(255, 255, 255))
        text_rect = movement_text.get_rect(center=(int(WINDOW_WIDTH/2), 825))
        movement = screen.blit(movement_text, text_rect)
        attack_text = create_font('Spacebar = Attack', s=30, b=True, c=(255, 255, 255))
        text_rect = movement_text.get_rect(center=(int(WINDOW_WIDTH/2), 875))
        attack = screen.blit(attack_text, text_rect)
        pygame.display.update()
        
        if button_1.collidepoint(mouse):
            if click:
                break # if game_loop is put into a function, call it here.
        if button_2.collidepoint(mouse):
            if click:
                pygame.quit()
                sys.exit()

        click = False 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        clock.tick(60)

main_menu()
while True: # game loop
    camera_offset[0] += int(player.x-camera_offset[0]-WINDOW_WIDTH/2 + player.image.get_width()/2)
    camera_offset[1] += int(player.y-camera_offset[1]-WINDOW_HEIGHT/2 + player.image.get_height()/2)
    if camera_offset[0] < 0:
        camera_offset[0] = 0
    if camera_offset[1] < 0:
        camera_offset[1] = 0
    if camera_offset[0] > len(maps.map_five[0]) * tile_size - WINDOW_WIDTH:
        camera_offset[0] = len(maps.map_five[0]) * tile_size - WINDOW_WIDTH
    if camera_offset[1] > len(maps.map_five) * tile_size - WINDOW_HEIGHT:
        camera_offset[1] = len(maps.map_five) * tile_size - WINDOW_HEIGHT
    
    # Particles
    if pygame.mouse.get_pressed()[0]:
        particles.append(Particle(pygame.mouse.get_pos()[0] + camera_offset[0], pygame.mouse.get_pos()[1] + camera_offset[1], (255, 255, 255)))

    # Generate Tiles
    solid_tiles = []
    end_tiles = []

    screen.blit(background, (0,0))
    y = 0
    for row in maps.map_five:
        x = 0
        for tile in row:
            if tile == 1:
                screen.blit(tile_one, (x * tile_size - camera_offset[0], y * tile_size - camera_offset[1]))
            if tile == 2:
                screen.blit(tile_two, (x * tile_size - camera_offset[0], y * tile_size - camera_offset[1]))
                end_tiles.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
            if tile == 3:
                screen.blit(tile_three, (x * tile_size - camera_offset[0], y * tile_size - camera_offset[1]))
            if tile != 0 and tile != 2:
                solid_tiles.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
            x += 1
        y += 1

    # Character Controls
    player.last_hit += 1
    player.control(gravity, max_velocity_x, max_velocity_y, particles)
    player.move(solid_tiles)
    player.draw_health(camera_offset, screen)
    # Enemy Controls
    for enemy in enemies:
        enemy.do_movement(player, gravity, max_velocity_y)
        enemy.move(solid_tiles)
        screen.blit(pygame.transform.flip(enemy.image, enemy.flip, False), (enemy.x - camera_offset[0], enemy.y - camera_offset[1]))
        if player.hitbox.colliderect(enemy.hitbox):
            player.hurt(enemy, screen)
        if len(player.attack) > 0: # Attack Check
            if enemy.hitbox.colliderect(player.attack[0]):
                enemy.damage_check(player, items, enemies, particles)

    # Item Controls
    for item in items:
        item.functions(screen, camera_offset, player)

    # Win / Lose Conditions
    keys=pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        main_menu()
    if not player.alive and victory == False:
        text_surface = font.render("Game Over! :( Press 'R' to Play Again.", True, [255,255,255], [0,0,0])
        screen.blit(text_surface, (750, 50))
        if keys[pygame.K_r]: # Player repsawn
            victory, wave, level_active, enemies, items, message_timer = level_reset(player, victory, wave, level_active, enemies, items, message_timer, message_timer_max)
    if player.check_win(end_tiles):
        if victory:
            text_surface = font.render("You win! Press 'R' to Play Again.", True, [255,255,255], [0,0,0])
            screen.blit(text_surface, (800, 50))
            player.kill()
            if keys[pygame.K_r]: # Player repsawn
                victory, wave, level_active, enemies, items, message_timer = level_reset(player, victory, wave, level_active, enemies, items, message_timer, message_timer_max)
        else:
            text_surface = font.render("Defeat All Enemies!", True, [255,255,255], [0,0,0])
            screen.blit(text_surface, (850, 50))

    # Enemy Waves
    if wave <= 5:
        if level_active == False:
            if message_timer > 0:
                text_surface = font.render(f"Wave {wave}", True, [255,255,255], [0,0,0])
                screen.blit(text_surface, (925, 100))
                message_timer -= 1
            elif message_timer == 0:
                enemies = spawn_enemy()
                level_active = True 
        elif level_active and len(enemies) == 0:
            wave += 1 
            level_active = False
            message_timer = message_timer_max
    else:
        victory = True
        if message_timer > 0:
            text_surface = font.render("Proceed To Exit", True, [255,255,255], [0,0,0])
            screen.blit(text_surface, (875, 100))
            message_timer -= 1

    # Player Blit
    screen.blit(pygame.transform.flip(player.image, player.flip, False), (player.x - camera_offset[0], player.y - camera_offset[1]))
    
    # Particle Controls
    for i in range(len(particles)-1, -1, -1):
        particles[i].x += particles[i].velocity_x
        particles[i].y += particles[i].velocity_y
        pygame.draw.circle(screen, particles[i].color, (int(particles[i].x - camera_offset[0]), int(particles[i].y - camera_offset[1])), int(particles[i].radius))
        particles[i].radius -= .1
        if particles[i].radius <= 0:
            particles.pop(i)

    # Exit the Game
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            sys.exit()

    player.attack = []
    highscore, score = update_score(highscore, score)
    show_score(500, 100, highscore, score)
    show_fps()
    pygame.display.update()
    clock.tick(60) # run at 60fps