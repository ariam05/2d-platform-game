import pygame

#List of Available Items in Current Build
item_type_list = ["coin", "health"]

class Item():
    def __init__(self, position_x, position_y, item_type=""): # Initialize Item
        self.x = position_x
        self.y = position_y
        self.width = 64
        self.height = 64
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.pickup_delay = 20
        # Item Status
        self.active = True 
        self.isCoin = False
        self.isHealth = False
        # For animation
        self.move_count = 0
        self.isFloating = False
        # Image Load
        if item_type in item_type_list:
            self.image = pygame.image.load(f"Assets\Sprites\items\{item_type}.png").convert_alpha()
            self.image.convert()
            if item_type == "coin":
                self.isCoin = True
            if item_type == "health":
                self.isHealth = True
        else: # Sets Default Image
            self.image = pygame.image.load(f"Assets\Sprites\items\default.png").convert_alpha()
            self.image.convert()
        
    def player_contact(self, player): # Collision Check with player model
        if self.hitbox.colliderect(player.hitbox) and self.active:
            if self.isCoin == True: # If item is a Coin, increases coins collected in player model
                player.coins_collected += 1
            if self.isHealth == True: # if Item is Health, increases health to player model
                player.health += 2
            self.active = False

    def floating(self): # Floating Animation
        if self.isFloating:
            if self.move_count == 0:
                self.y += 10
                self.isFloating = False
            if self.move_count == 5:
                self.y += 10
                self.move_count -= 1
            else:
                self.move_count -= 1
        else:
            if self.move_count == 10:
                self.y -= 10
                self.isFloating = True
            if self.move_count == 5:
                self.y -= 10
                self.move_count += 1
            else:
                self.move_count += 1
    
    def show(self, screen, camera_offset): # Item blit to screen
        if self.active:
            screen.blit(self.image, (self.x - camera_offset[0], self.y - camera_offset[1]))

    def functions(self, screen, camera_offset, player): # access all Item functions
        if self.pickup_delay > 0:
            self.pickup_delay -=1
        elif self.pickup_delay == 0:
            self.player_contact(player)
        self.floating()
        self.show(screen, camera_offset)

    def sword(self):
        pass