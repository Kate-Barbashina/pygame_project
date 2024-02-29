import os
import sys

import pygame
from pygame import mixer
import pygame_menu

mixer.init()
pygame.init()
clock = pygame.time.Clock()
fps = 30
screen = pygame.display.set_mode((500, 600))
fon = pygame.image.load('data/fon.jpg')
number_1 = 0
num_level = 1
number_2 = 0
endgame = 0

#music
start_music = pygame.mixer.Sound('data/song-for-game.mp3')
start_music.set_volume(0.5)
start_music.play()
jump_sound = pygame.mixer.Sound('data/sound.wav')
jump_sound.set_volume(0.4)
jump_sound2 = pygame.mixer.Sound('data/sound2.wav')
jump_sound2.set_volume(0.3)

def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# loading of images
player_1_image = load_image('pl.png')
player_2_image = load_image('player_2.png')
crystal_image = load_image('kristal.png')
water_image = load_image('water.png')
img_c = pygame.transform.scale(crystal_image, (45, 80))
img_w = pygame.transform.scale(water_image, (4, 80))
coin_sprites = pygame.sprite.Group()


# some methods
def lose_game(n):
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    running = True
    if n == 1:
        lose = load_image('tilt_1.jpg')
    else:
        lose = load_image('tilt_2.jpg')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #if event.type == pygame.MOUSEBUTTONDOWN:
               # if area.collidepoint(event.pos):
        lose_tr = pygame.transform.scale(lose, (800, 800))
        clock.tick(fps)
        screen.blit(lose_tr, (0, 0))
        pygame.display.flip()

    print(1)


def win_game():
    print('12334')


class Player_1:
    def __init__(self, x, y):
        self.img = pygame.transform.scale(player_1_image, (45, 80))
        player_image_n = load_image('pln.png')
        self.img_n = pygame.transform.scale(player_image_n, (45, 80))
        self.img_rect = self.img.get_rect()
        self.img_rect.x = x
        self.img_rect.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.speed_y = 0
        self.f = 1  # hero didn't jump
        self.flight = True
        self.flag_n = True
        self.score = 0

    def update(self):
        global number_1
        dx = 0
        dy = 0
        # keypress
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx -= 5
            self.flag_n = False
        if key[pygame.K_RIGHT]:
            self.flag_n = True
            dx += 5
        if key[pygame.K_UP] and self.f == 1 and self.flight == False:
            jump_sound.play()
            self.speed_y = -15
            self.f = 0
        if not key[pygame.K_UP]:
            self.f = 1

        # gravity
        self.speed_y += 1
        if self.speed_y > 10:
            self.speed_y = 10
        dy += self.speed_y

        fl = 0
        # checking
        # collision with water
        for tile in level.water_list:
            if tile[1].collidepoint(self.img_rect.bottomright) or tile[1].collidepoint(self.img_rect.bottomleft):
                lose_game(1)
        # collision with coins
        # collision for jumping
        self.flight = True
        for tile in level.cloud:
            # in x coordinates
            if tile[1].colliderect(self.img_rect.x + dx, self.img_rect.y, self.width, self.height):
                if tile[0] == img_c:
                    fl = 1
                    number_1 = 1
                else:
                    dx = 0
            # in y coordinates
            if tile[1].colliderect(self.img_rect.x, self.img_rect.y + dy, self.width, self.height):
                # jumping
                if self.speed_y < 0:
                    dy = tile[1].bottom - self.img_rect.top
                    self.speed_y = 0  # speed = 0 because we get in a normal state after jump
                # falling
                else:
                    dy = tile[1].top - self.img_rect.bottom
                    self.speed_y = 0
                    self.flight = False # because he falls, so he is on the ground, we can jump after

        self.img_rect.x += dx
        self.img_rect.y += dy
        if self.flag_n:
            screen.blit(self.img, self.img_rect)
        else:
            screen.blit(self.img_n, self.img_rect)

class Player_2:
    def __init__(self, x, y):
        player_image = load_image('player2.png')
        self.img = pygame.transform.scale(player_image, (45, 80))
        player_image_n = load_image('playern.png')
        self.img_n = pygame.transform.scale(player_image_n, (45, 80))
        self.img_rect = self.img.get_rect()
        self.img_rect.x = x
        self.img_rect.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.speed_y = 0
        self.f = 1  # hero didn't jump
        self.flag_n = True
        self.flight = True

    def update(self):
        global number_2
        dx = 0
        dy = 0
        # keypress
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx -= 5
            self.flag_n = False
        if key[pygame.K_d]:
            self.flag_n = True
            dx += 5
        if key[pygame.K_w] and self.f == 1 and self.flight == False:
            jump_sound2.play()
            self.speed_y = -15
            self.f = 0
        if not key[pygame.K_w]:
            self.f = 1

        # gravity
        self.speed_y += 1
        if self.speed_y > 10:
            self.speed_y = 10
        dy += self.speed_y

        fl = 0
        # checking
        # collision with water
        for tile in level.water_list:
            if tile[1].collidepoint(self.img_rect.bottomright) or tile[1].collidepoint(self.img_rect.bottomleft):
                lose_game(2)
        # collision for jumping
        self.flight = True
        for tile in level.cloud:
            # in x coordinates
            if tile[1].colliderect(self.img_rect.x + dx, self.img_rect.y, self.width, self.height):
                if tile[0] == img_c:
                    fl = 1
                    number_2 = 1
                else:
                    dx = 0
            # in y coordinates
            if tile[1].colliderect(self.img_rect.x, self.img_rect.y + dy, self.width, self.height):
                # jumping
                if self.speed_y < 0:
                    dy = tile[1].bottom - self.img_rect.top
                    self.speed_y = 0  # speed = 0 because we get in a normal state after jump
                # falling
                else:
                    dy = tile[1].top - self.img_rect.bottom
                    self.speed_y = 0
                    self.flight = False

        self.img_rect.x += dx
        self.img_rect.y += dy
        if self.flag_n:
            screen.blit(self.img, self.img_rect)
        else:
            screen.blit(self.img_n, self.img_rect)


class Level:
    def __init__(self, n):
        self.cloud = []
        self.water_list = []
        backgr_image = load_image(f'backgr{n}.jpg')
        background_image = pygame.transform.scale(backgr_image, (800, 800))
        block_image = load_image(f'dirt{n}.png')
        img1 = pygame.transform.scale(block_image, (50, 50))
        dirt_image = load_image(f'block{n}.png')
        img = pygame.transform.scale(dirt_image, (50, 50))
        water_image = load_image('water.png')
        img_w = pygame.transform.scale(water_image, (50, 50))
        # water_dop_image = load_image('water_dop.png')
        # img_w1 = pygame.transform.scale(water_dop_image, (50, 50))
        leve = load_level(f'level{n}.txt')
        r = 0
        for y in range(len(leve)):
            c = 0
            for x in range(len(leve[y])):
                if leve[y][x] == '1':
                    img_rect = img.get_rect()
                    img_rect.x = c * 50
                    img_rect.y = r * 50
                    tile = (img, img_rect)
                    self.cloud.append(tile)
                if leve[y][x] == '2':
                    img1_rect = img.get_rect()
                    img1_rect.x = c * 50
                    img1_rect.y = r * 50
                    tile = (img1, img1_rect)
                    self.cloud.append(tile)
                if leve[y][x] == '3':
                    imgc_rect = img.get_rect()
                    imgc_rect.x = c * 50
                    imgc_rect.y = r * 50
                    tile = (img_c, imgc_rect)
                    self.cloud.append(tile)
                if leve[y][x] == '4':
                    coin = Coin([c * 50 + 25, r * 50 + 25])
                if leve[y][x] == '*':
                    imgw_rect = img.get_rect()
                    imgw_rect.x = c * 50
                    imgw_rect.y = r * 50
                    tile = (img_w, imgw_rect)
                    self.water_list.append(tile)
                    self.cloud.append(tile)
                # if leve[y][x] == '#':
                # imgw1_rect = img.get_rect()
                # imgw1_rect.x = c * 50
                # imgw1_rect.y = r * 50
                # tile = (img_w1, imgw1_rect)
                # self.cloud.append(tile)
                c += 1
            r += 1

    def draw(self):
        for tile in self.cloud:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Coin(pygame.sprite.Sprite):
    def __init__(self, coordinates):
        super().__init__(coin_sprites)
        x = coordinates[0]
        y = coordinates[1]
        coin_img = load_image('coin.png')
        self.image = pygame.transform.scale(coin_img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


level = Level(num_level)

def start_the_game():
    start_music.stop()
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    global level
    global num_level
    global number_1
    global number_2
    backgr_image = load_image(f'backgr{num_level}.jpg')
    background_image = pygame.transform.scale(backgr_image, (800, 800))

    player_1 = Player_1(100, 800 - 130)
    player_2 = Player_2(130, 800 - 130)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
        if number_1 == 1 and number_2 == 1:
            num_level += 1
            if num_level == 2:
                player_1 = Player_1(100, 800 - 130)
                player_2 = Player_2(660, 800 - 130)
                level = Level(num_level)
            else:
                player_1 = Player_1(100, 800 - 130)
                player_2 = Player_2(130, 800 - 130)
                level = Level(num_level)
            number_1 = 0
            number_2 = 0

        clock.tick(fps)
        screen.blit(background_image, (0, 0))
        level.draw()
        coin_sprites.draw(screen)
        player_1.update()
        player_2.update()
        pygame.display.flip()


def about_function():
    # открытие файла txt с описанием правил игры
    animation_set = [pygame.image.load(f"animation/{i}.jpg") for i in range(1, 6)]
    window = pygame.display.set_mode((550, 550))
    clock = pygame.time.Clock()
    i = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_the_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                rule = load_image('rules.jpg')
                rules = pygame.transform.scale(rule, (800, 800))
                window.blit(rules, (100, 0))

        window.fill((0, 0, 0))
        window.blit(animation_set[i // 12], (100, 20))
        i += 1
        if i == 60:
            print('1')

        pygame.display.flip()
        clock.tick(30)


main_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
main_theme.set_background_color_opacity(0.0)
menu = pygame_menu.Menu('Добро пожаловать', 400, 300,
                        theme=main_theme)

menu.add.text_input('Имя: ', default='User')
menu.add.button(' Об игре', about_function)
menu.add.button('Начать игру', start_the_game)
running = True
while running:

    screen.blit(fon, (0, 0))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if running and menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()

pygame.quit()
