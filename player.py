import pygame
from particle import Particle

#colors:
RED = (255, 0, 0)
GREEN = (0, 255, 0)
global animation_frames
animation_frames = {}

class Player():
    def __init__(self):
        self.image = pygame.image.load('Assets/Sprites/player/idle/idle0.png').convert_alpha()
        self.max_airtime = 6
        self.airtime = 0
        self.x = 300
        self.y = 1000
        self.hitbox = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.velocity_x = 0
        self.velocity_y = 0
        self.alive = True
        self.health = 10
        self.max_health = 10
        self.last_hit = 0
        self.damage = 3
        self.attack_delay = 0
        self.attack = []
        # self.weapon = ['sword']

        self.state = "idle"
        self.frame = 0
        self.flip = False
        self.animation_database = {}
        self.animation_database["walk"] = self.load_animation("Assets/Sprites/player/walk", [7,7])
        self.animation_database["jump"] = self.load_animation("Assets/Sprites/player/jump", [1])
        self.animation_database["idle"] = self.load_animation("Assets/Sprites/player/idle", [1])
        self.animation_database["attack"] = self.load_animation("Assets/Sprites/player/attack", [7,8])
        self.animation_database["fall"] = self.load_animation("Assets/Sprites/player/fall", [1])
        # self.max_jumps = 1
        self.kills = 0
        self.coins_collected = 0

    def hurt(self, enemy, screen): # Damages Player
        if self.last_hit > 30:
            if (self.x + self.image.get_width()/2) < (enemy.x + enemy.image.get_width()/2):
                self.velocity_x = -20
            else:
                self.velocity_x = 20
            self.health -= enemy.damage
            self.last_hit = 0
            if self.health <= 0:
                self.kill()
    
    def kill(self):
        self.alive = False

    def collision_test(self, tiles): # World Collision
        hit_list = []
        player_rect = self.image.get_rect(left=self.x, top=self.y)
        for tile in tiles:
            if player_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def draw_health(self, camera_offset, screen): # Draws Health Bar
        pygame.draw.rect(screen, RED, (50, 50, self.max_health * 20, 10)) # *20 to increase health bar length
        if self.health > 0:
            pygame.draw.rect(screen, GREEN, (50, 50, self.health * 20, 10))

    def move(self, tiles): # World Collision
        self.x += self.velocity_x
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.velocity_x > 0:
                self.x = tile.left - int(self.image.get_width()) # collide on right side
            elif self.velocity_x < 0:
                self.x = tile.right # collide on left side
        self.y += self.velocity_y
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.velocity_y > 0:
                self.y = tile.top - int(self.image.get_height()) # collide on bottom side
                self.velocity_y = 0
                self.airtime = 0
            elif self.velocity_y < 0:
                self.y = tile.bottom # collide on top side
                self.velocity_y = 0
        self.hitbox = pygame.Rect(self.x, self.y, 50, 60)
        return self.image.get_rect

    def check_win(self, tiles): # Checks if Player is at Exit
        player_rect = self.image.get_rect(left=self.x, top=self.y)
        for tile in tiles:
            if player_rect.colliderect(tile):
                return True

    def control(self, gravity, max_velocity_x, max_velocity_y, particles): # Player Controls
        self.frame += 1
        if self.frame >= len(self.animation_database[self.state]):
            self.frame = 0
        self.image = animation_frames[self.animation_database[self.state][self.frame]]
        keys=pygame.key.get_pressed()
        if self.alive:
            if keys[pygame.K_LEFT]:
                if self.velocity_x > -max_velocity_x:
                    self.velocity_x -= 2
                else: 
                    velocity_x = -max_velocity_x
                self.state = self.change_state(self.state, "walk")
                if self.airtime == 0:
                    particles.append(Particle(self.x + self.image.get_width()/2, self.y + self.image.get_height(), (96,100,170)))
                self.flip = True
            elif keys[pygame.K_RIGHT]:
                if self.velocity_x < max_velocity_x:
                    self.velocity_x += 2
                else: 
                    velocity_x = max_velocity_x
                if self.airtime == 0:
                    particles.append(Particle(self.x + self.image.get_width()/2, self.y + self.image.get_height(), (96,100,170)))
                self.state = self.change_state(self.state, "walk")
                self.flip = False
            else:
                if self.velocity_x > 0:
                    self.velocity_x -= 1
                elif self.velocity_x < 0:
                    self.velocity_x += 1
                else:
                    self.velocity_x = 0
                self.state = self.change_state(self.state, "idle")
            if self.attack_delay > 0:
                self.attack_delay -= 1
            if keys[pygame.K_SPACE]:
                if self.attack_delay == 0:
                    self.state = self.change_state(self.state, "attack")
                    if self.flip:
                        attack1 = pygame.Rect(self.x - self.image.get_width(), self.y, self.image.get_width(), self.image.get_height())
                        # Insert attack animation here
                        self.attack.append(attack1)
                    else:
                        attack1 = pygame.Rect(self.x + self.image.get_width(), self.y, self.image.get_width(), self.image.get_height())
                        # Insert attack animation here
                        self.attack.append(attack1)
                    self.attack_delay = 15 # Sets max attack delay
            if self.velocity_y < 0:
                self.state = self.change_state(self.state, "jump")
            elif self.velocity_y > 0:
                self.state = self.change_state(self.state, "fall")
            if self.airtime < self.max_airtime:
                self.airtime += 1
                if keys[pygame.K_UP]:
                    self.airtime = self.max_airtime
                    self.velocity_y = -25
        # elif keys[pygame.K_r]: # Player repsawn TEMP DISABLED
        #     self.health = self.max_health
        #     self.alive = True
        #     self.x = 300
        #     self.y = 1000
        self.velocity_y += gravity
        if self.velocity_y > max_velocity_y:
            self.velocity_y = max_velocity_y

    def change_state(self, current_state, state): # Animation states
        if current_state == "attack" and self.frame != 9:
            pass
        elif current_state != state:
            current_state = state
            self.frame = 0
        return current_state

    def load_animation(self, path, frame_durations): # Loads Animation
        global animation_frames
        animation_name = path.split('/')[-1]
        animation_frame_data = []
        n = 0
        for frame in frame_durations:
            animation_frame_id = animation_name + str(n)
            img_loc = path + "/" + animation_frame_id + ".png"
            animation_image = pygame.image.load(img_loc).convert_alpha()
            animation_frames[animation_frame_id] = animation_image.copy()
            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1
        return animation_frame_data