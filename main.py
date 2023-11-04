import pygame, sys
import random

pygame.init()

s_width = 600
s_height = 600

screen = pygame.display.set_mode((s_width, s_height))
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (random.randint(0, s_width - self.rect.width), random.randint(0, s_height - self.rect.height))
        self.speed = 3  # Initial speed value.
        self.power_up_duration = 7 # Duration of the power-up effect in seconds (adjust as needed).
        self.power_up_end_time = 0
        self.speed_boost = False  # Flag to indicate if the player has collected a coin.

    def update(self):
        # Check if the power-up effect has expired.
        current_time = pygame.time.get_ticks() / 1000  # Convert to seconds.
        if current_time > self.power_up_end_time:
            self.speed = 3  # Reset speed to the default value.
            self.speed_boost = False  # Reset the speed boost flag.

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.rect.y -= self.speed
        if keystate[pygame.K_a]:
            self.rect.x -= self.speed
        if keystate[pygame.K_s]:
            self.rect.y += self.speed
        if keystate[pygame.K_d]:
            self.rect.x += self.speed

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.bottom >= s_height:
            self.rect.bottom = s_height
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.right >= s_width:
            self.rect.right = s_width

# Define the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1.05
        self.speed_increase_rate = 0.1  # Speed increase rate per 10 seconds

    def update(self, player):
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        if self.rect.y > player.rect.y:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

# Define the Power-Up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = power_up_image  # Use the loaded power-up image.
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def apply_power_up(self, player):
        # Apply the power-up effect to the player (e.g., increase speed).
        player.speed += 2  # Increase the player's speed.

# Load images
player_img = pygame.image.load('hero.png')
enemy_img = pygame.image.load('ghost.png')
power_up_image = pygame.image.load('coin.png')  # Load the power-up image.
power_up_image = pygame.transform.scale(power_up_image, (40, 40))

# Create sprite groups
allSprites = pygame.sprite.Group()
enemySprites = pygame.sprite.Group()
power_up_sprites = pygame.sprite.Group()  # Create a group for power-ups.

# Create objects
player = Player(player_img)
enemy1 = Enemy(enemy_img, s_width, s_height/2)

# Add objects to groups
allSprites.add(player)
enemySprites.add(enemy1)

# Initialize timers and game state
time = 0
reset = 0
power_up_timer = pygame.time.get_ticks()
game_state = "Play"

# Draw text function
def draw_text(color, text, font, size, x, y, surface):
    font_name = pygame.font.match_font(font)
    Font = pygame.font.Font(font_name, size)
    text_surface = Font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            break

    if game_state == "Lose":
        pygame.quit()   # Ends the game and closes
    else:
        collisions = pygame.sprite.spritecollide(player, enemySprites, False)

        for c in collisions:
            print("GAME OVER")
            game_state = "Lose"
            pygame.quit()   # Closes the game if the ghost hits the player
            sys.exit()
        screen.fill(white)

        # TIMER FOR PLAYER:
        time = pygame.time.get_ticks() / 1000
        draw_text(black, "Score: {:.1f} seconds".format(time), "arial", 18, 110, 20, screen)

        # Increase enemy speed every 10 seconds
        current_time = pygame.time.get_ticks()
        if current_time - reset >= 10000:
            reset += 10000
            for enemy in enemySprites:
                enemy.speed += enemy.speed_increase_rate
            enemy = Enemy(enemy_img, random.randint(0, s_width), random.randint(0, s_height))
            enemySprites.add(enemy)


        # Create power-up objects and add them to the power_up_sprites group
        current_time = pygame.time.get_ticks()
        if current_time - power_up_timer >= 10000:  # 10 seconds (in milliseconds)
            power_up = PowerUp(random.randint(0, s_width), random.randint(0, s_height))
            power_up_sprites.add(power_up)
            power_up_timer = current_time

        # Check for collisions with power-ups
        power_up_collisions = pygame.sprite.spritecollide(player, power_up_sprites, True)

        for power_up in power_up_collisions:
            power_up.apply_power_up(player)  # Apply the power-up effect to the player.
            player.power_up_end_time = (pygame.time.get_ticks() / 1000) + player.power_up_duration
            player.speed_boost = True  # Set the speed boost flag.

        # Update player's speed based on the speed boost flag
        if player.speed_boost:
            player.speed = 4  # Increase the player's speed when they have a speed boost.

        # DRAWING TO SCREEN:
        allSprites.draw(screen)
        enemySprites.draw(screen)
        power_up_sprites.draw(screen)

        # UPDATE GROUPS:
        allSprites.update()
        enemySprites.update(player)

    clock.tick(40)
    pygame.display.update()
