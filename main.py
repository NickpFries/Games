import pygame
import os
import random
from powerups import HealthBoost, ExtraLife, RapidFire, TriShot

pygame.font.init()

# Create Window

WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Space Shooter Tutorial")
WIDTH = WIN.get_width()
HEIGHT = WIN.get_height()
SIZE = WIDTH * HEIGHT * .0001  # Expect a value around 140
# Load images

# Ships
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
PLAYER_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
# Background
BG = pygame.transform.scale((pygame.image.load(os.path.join("assets", "background-black.png")).convert()),
                            (WIDTH, HEIGHT))
# PowerUps
EXTRALIFE = pygame.image.load(os.path.join("assets", "life.png"))
TRISHOT = pygame.image.load(os.path.join("assets", "trishot.png"))
RAPIDFIRE = pygame.image.load(os.path.join("assets", "rapidfire.png"))
HEALTHBOOST = pygame.image.load(os.path.join("assets", "health.png"))


# Lasers for both the player and enemy ships
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, speed):
        self.y += speed

    def off_screen(self, height):
        return self.y > height + self.img.get_height() or self.y < -self.img.get_height()

    def collision(self, obj):
        return collide(obj, self)


class Ship:
    COOLDOWN = 30   # Determines fire rate of the player

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.tri_shot = False
        self.rapid_fire = False

    def draw(self, window):
        for laser in self.lasers:
            laser.draw(window)
        window.blit(self.ship_img, (self.x, self.y))

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def width(self):
        return self.ship_img.get_width()

    def height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter <= 0:
            self.cool_down_counter = 0
        else:
            self.cool_down_counter -= 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            if self.tri_shot:
                self.lasers.append(Laser(self.x + self.ship_img.get_width() / 2 - 5, self.y + 30, self.laser_img))
                self.lasers.append(Laser(self.x - self.ship_img.get_width() / 2 + 5, self.y + 30, self.laser_img))
            if self.rapid_fire:
                self.cool_down_counter = 10
            else:
                self.cool_down_counter = self.COOLDOWN


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objects):
        self.cooldown()
        for laser in self.lasers:
            laser.move(-vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objects:
                    if laser.collision(obj):
                        obj.health -= 10
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        for laser in self.lasers:
            laser.draw(window)
        window.blit(self.ship_img, (self.x, self.y))
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                               self.ship_img.get_width() * (
                                                   (1 - ((self.max_health - self.health) / self.max_health))), 10))


class EnemyShip(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)}

    def __init__(self, x, y, color, health):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, speed):
        self.y += speed

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = self.COOLDOWN


def main():
    # General variables
    run = True
    FPS = 60
    level = 0   # Increments by one before the first wave appears
    lives = 5
    speed = int(SIZE * 0.08)
    enemy_speed = int(HEIGHT * 0.0025)
    laser_speed = int(HEIGHT * 0.006)
    temp_lasers = []
    main_font = pygame.font.SysFont("comicsans", int(SIZE * 0.6))
    lost_font = pygame.font.SysFont("comicsans", int(SIZE * 0.65))
    player = Player(WIDTH / 2 - PLAYER_SPACE_SHIP.get_width() / 2, HEIGHT * 0.8)
    clock = pygame.time.Clock()
    pause = False
    lost = False

    # Enemy variables
    enemies = []
    wave_length = 4

    # Power up variables
    power_ups = []
    rapid_fire_counter = 0
    tri_shot_counter = 0


    def redraw_window():
        # Draw Background
        WIN.blit(BG, (0, 0))

        # Draw Text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - 10 - level_label.get_width(), 10))

        # Draw Objects
        for i in range(0, len(enemies)):
            enemies[i].draw(WIN)
        for j in temp_lasers:
            j.draw(WIN)

        # Draw PowerUps
        for p_up in power_ups:
            p_up.draw(WIN)

        player.draw(WIN)

        if lost:
            pause_font = pygame.font.SysFont("comicsans", int(SIZE * 0.4))
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            pause_label = pause_font.render("Press Q to Quit    Press R to Restart", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))
            WIN.blit(pause_label, (WIDTH * 0.01, HEIGHT * 0.95 - pause_label.get_height()))

        if pause:
            pause_font = pygame.font.SysFont("comicsans", int(SIZE * 0.4))
            state_font = pygame.font.SysFont("comicsans", int(SIZE * 0.8))
            pause_label = pause_font.render("Press Q to Quit    Press R to Restart    Press Enter to Resume", 1,
                                            (255, 255, 255))
            state_label = state_font.render("Paused", 1, (255, 255, 255))
            WIN.blit(pause_label, (WIDTH * 0.01, HEIGHT * 0.95 - pause_label.get_height()))
            WIN.blit(state_label, (WIDTH / 2 - state_label.get_width() / 2, HEIGHT * 0.4))
        pygame.display.update()

    def handle_temp_lasers(vel):
        for lsr in temp_lasers:
            lsr.move(vel)
            if lsr.off_screen(HEIGHT):
                temp_lasers.remove(lsr)
            elif lsr.collision(player):
                player.health -= 10
                temp_lasers.remove(lsr)

    while run:
        clock.tick(FPS)
        redraw_window()
        keys = pygame.key.get_pressed()

        # Exit Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Check player death
        if lives <= 0 or player.health <= 0:
            lost = True

        # Pause and Lost menu handling
        if keys[pygame.K_ESCAPE]:  # Pause
            if not lost:
                pause = True
        if keys[pygame.K_RETURN]:  # Resume
            pause = False

        if pause:
            if keys[pygame.K_q]:
                quit()
            if keys[pygame.K_r]:
                main_menu()
                quit()

        if lost:
            if keys[pygame.K_q]:
                quit()
            if keys[pygame.K_r]:
                main_menu()
                quit()

        if pause or lost:
            continue

        # Spawn in Enemies
        if len(enemies) == 0:
            level += 1
            if level <= 3:
                wave_length += 1
                for i in range(0, wave_length):
                    enemies.append(
                        EnemyShip(random.randint(0, WIDTH - BLUE_SPACE_SHIP.get_width()),
                                  random.randint(int(-HEIGHT * (1 + (level * 0.1))), -100),
                                  random.choice(["red", "green"]), 10))
            elif 3 < level < 6:
                wave_length = 10
                for i in range(0, wave_length):
                    enemies.append(
                        EnemyShip(random.randint(0, WIDTH - BLUE_SPACE_SHIP.get_width()),
                                  random.randrange(int(-HEIGHT * 1.5), -100),
                                  random.choice(["red", "green"]), 10))
            elif 6 <= level <= 7:
                wave_length = 7
                for i in range(0, wave_length):
                    enemies.append(
                        EnemyShip(random.randint(0, WIDTH - BLUE_SPACE_SHIP.get_width()),
                                  random.randrange(int(-HEIGHT * 1.5), -100),
                                  random.choice(["red", "green", "blue"]), 10))
            elif level > 7:
                wave_length += 1
                enemy_speed += int(HEIGHT * 0.0002)
                for i in range(0, wave_length):
                    enemies.append(
                        EnemyShip(random.randint(0, WIDTH - BLUE_SPACE_SHIP.get_width()),
                                  random.randrange(int(-HEIGHT * 0.2 * level), -100),
                                  random.choice(["red", "green", "blue"]), 10))
            if level % 8 == 0:
                for i in range(1, 6):
                    enemies.append(
                        EnemyShip(i * WIDTH / 5 - BLUE_SPACE_SHIP.get_width(),
                                  int(-HEIGHT * 0.2 * level) - 300,
                                  random.choice(["red", "green", "blue"]), 10))

        # Spawn in PowerUps
        spawn_chance = random.randint(0, 60 * 20 * 4)
        if spawn_chance == 777:
            if player.health == player.max_health:
                spawn_chance = 778
            else:
                power_ups.append(HealthBoost(HEALTHBOOST, WIN))
        if spawn_chance == 778:
            power_ups.append(RapidFire(RAPIDFIRE, WIN))
        if spawn_chance == 779:
            if lives == 5:
                spawn_chance = 780
            else:
                power_ups.append(ExtraLife(EXTRALIFE, WIN))
        if spawn_chance == 780:
            power_ups.append(TriShot(TRISHOT, WIN))

        # Handle the PowerUps
        if tri_shot_counter > 0:
            tri_shot_counter -= 1
        else:
            player.tri_shot = False
        if rapid_fire_counter > 0:
            rapid_fire_counter -= 1
        else:
            player.rapid_fire = False
        for pu in power_ups:
            pu.move()
            pu.x = clamp(pu.x, 0, WIDTH - pu.img.get_width())
            if pu.x == 0 or pu.x == WIDTH - pu.img.get_width():
                pu.speed_x *= -1
            if collide(pu, player):
                if isinstance(pu, HealthBoost):
                    player.health += 30
                    player.health = clamp(player.health, 0, 100)
                elif isinstance(pu, ExtraLife):
                    lives += 1
                    lives = clamp(lives, 0, 5)
                elif isinstance(pu, TriShot):
                    player.tri_shot = True
                    tri_shot_counter = pu.life_span
                elif isinstance(pu, RapidFire):
                    player.rapid_fire = True
                    rapid_fire_counter = pu.life_span
                power_ups.remove(pu)

        # Player Movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # left
            player.x -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # right
            player.x += speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:  # up
            player.y -= speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # down
            player.y += speed
        if keys[pygame.K_SPACE]:  # Shoot
            player.shoot()

        # Clamp to keep player in screen
        player.x = clamp(player.x, 0, WIDTH - player.width())
        player.y = clamp(player.y, 0, HEIGHT - player.height())

        # Handle PLayer Lasers
        player.move_lasers(laser_speed, enemies)
        handle_temp_lasers(laser_speed)

        # Enemy Handling
        for i in range(len(enemies) - 1, -1, -1):
            # Death
            if enemies[i].health <= 0:
                for laser in enemies[i].lasers:
                    temp_lasers.append(laser)
                enemies.remove(enemies[i])
                continue

            # Movement
            enemies[i].move(enemy_speed)
            enemies[i].x = clamp(enemies[i].x, 0, WIDTH - enemies[i].width())

            # Lasers
            enemies[i].move_lasers(laser_speed, player)
            if random.randrange(0, 3 * 60) == 1:
                enemies[i].shoot()

            # Collide with player
            if collide(enemies[i], player):
                player.health -= 15
                for las in enemies[i].lasers:
                    temp_lasers.append(las)
                enemies.remove(enemies[i])
                continue

            # Enemy went off screen
            if enemies[i].y > HEIGHT:
                lives -= 1
                enemies.remove(enemies[i])


# Contain variable within a min and max value
def clamp(var, min, max):
    # Clamp variable to specified range
    if var > max:
        var = max
    if var < min:
        var = min
    return var


# Check if two objects collide using their mask
def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


# Opening menu if the game, calls the main() function when game starts
def main_menu():
    title_font = pygame.font.SysFont("comicsans", int(WIDTH * 0.1))
    start_font = pygame.font.SysFont("comicsans", int(WIDTH * 0.05))
    quit_font = pygame.font.SysFont("comicsans", int(WIDTH * 0.03))
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("SPACE INVADERS", 1, (255, 255, 255))
        start_label = start_font.render("Press Enter to start...", 1, (255, 255, 255))
        quit_label = quit_font.render("Press Q to Quit", 1, (255, 255, 255))
        WIN.blit(start_label, (WIDTH / 2 - start_label.get_width() / 2, HEIGHT * 0.6))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, HEIGHT * 0.2))
        WIN.blit(quit_label, (WIDTH * 0.01, HEIGHT * 0.95 - quit_label.get_height()))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  # Start game
            main()
        if keys[pygame.K_q]:  # quit
            quit()
    quit()


main_menu()
