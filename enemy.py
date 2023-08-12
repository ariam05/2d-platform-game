import pygame
import random
from items import Item
from particle import Particle

# define colors
GREEN = (0, 255, 0)
global animation_frames
animation_frames = {}

class Enemy():
    def __init__(self, x=100, y=100): # Initialize Enemy
        self.image = pygame.image.load('Assets/Sprites/enemy/walk/walk1.png').convert_alpha()
        self.image.convert()
        self.x = x #pass in window width
        self.y = y #random.randrange(-100, -40)
        self.hitbox = pygame.Rect(self.x, self.y, 50, 60)
        self.airtime = 0
        self.max_airtime = 6
        self.damage = 1
        self.max_velocity_x = 8
        self.velocity_x = 0 # in the future add ai so it'll jump
        self.velocity_y = 0 # in the future add ai so it'll jump
        self.health = 6 # change later and add function to modify

        self.state = "walk"
        self.frame = 0
        self.flip = False
        self.animation_database = {}
        self.animation_database["walk"] = self.load_animation("Assets/Sprites/enemy/walk", [7,7])

    def drop_stuff(self, all_items): # Drop on defeat
        random_num = random.randrange(1,100)
        if 50 < random_num < 76: # 25 % chance to drop coin
            item_drop = Item(self.x, self.y, "coin")
            all_items.append(item_drop)
        elif 75 < random_num < 101: # 25 % chance to drop health
            item_drop = Item(self.x, self.y, "health")
            all_items.append(item_drop)

    def hurt(self, player, all_enemies): # Deal Damage / Defeat Check
        self.health -= player.damage
        if (player.x + player.image.get_width()/2) > (self.x + self.image.get_width()/2):
            self.velocity_x = -20
        else:
            self.velocity_x = 20
        if self.health <= 0:
            player.kills += 1
            all_enemies.remove(self)
    
    def damage_check(self, player, all_items, all_enemies, particles): # Check health for drop
        for i in range(10):
            particles.append(Particle(self.x + self.image.get_width()/2, self.y + self.image.get_height()/2, (255, 255, 255)))
        if (self.health - player.damage) <= 0:
            self.drop_stuff(all_items)
        self.hurt(player, all_enemies)

    def update(self): # Update hitbox
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


    def collision_test(self, tiles): # World Collide
        hit_list = []
        self_rect = self.image.get_rect(left=self.x, top=self.y)
        for tile in tiles:
            if self_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, tiles): # World Collide
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
                self.airtime = 0
                self.y = tile.top - int(self.image.get_height()) # collide on bottom side
                self.velocity_y = 0
            elif self.velocity_y < 0:
                self.y = tile.bottom # collide on top side
                self.velocity_y = 0
        self.hitbox = pygame.Rect(self.x, self.y, 50, 60)
        return self.image.get_rect

    def do_movement(self, player, gravity, max_velocity_y): # Enemy AI
        self.frame += 1
        if self.frame >= len(self.animation_database[self.state]):
            self.frame = 0
        self.image = animation_frames[self.animation_database[self.state][self.frame]]
        if player.x < self.x:
            if self.velocity_x > -self.max_velocity_x:
                self.velocity_x -= 2
            if self.velocity_x <= -self.max_velocity_x:
                self.velocity_x = -self.max_velocity_x
            self.state = self.change_state(self.state, "walk")
            self.flip = True
        elif player.x > self.x:
            if self.velocity_x < self.max_velocity_x:
                self.velocity_x += 2
            if self.velocity_x >= self.max_velocity_x:
                self.velocity_x = self.max_velocity_x
            self.state = self.change_state(self.state, "walk")
            self.flip = False
        if player.y + player.image.get_height() < self.y + self.image.get_height():
            if self.airtime < self.max_airtime:
                self.airtime = self.max_airtime
                self.velocity_y = -20
        if self.velocity_y > 0:
            self.airtime += 1
        self.velocity_y += gravity
        if self.velocity_y > max_velocity_y:
            self.velocity_y = max_velocity_y
    
    def change_state(self, current_state, state): # Checks Animation State
        if current_state != state:
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

