import os
import sys

import pygame
import pygame_menu
from pygame import mixer

mixer.init()
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((500, 600))
fon = pygame.image.load('data/fon.jpg')
# variables
fps = 30
sprite_size = 50
number_1 = 0
num_level = 1
number_2 = 0
endgame = 0  # it means that game in process; 1 - you passed level or won game; -1 - game over
died_1 = 0
died_2 = 0


# music
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
crystal_image = load_image('crystal.png')
water_image = load_image('water.png')
img_c = pygame.transform.scale(crystal_image, (35, 90))
img_w = pygame.transform.scale(water_image, (45, 80))

coin_sprites = pygame.sprite.Group()


# some methods
def lose_game(n):
    global endgame
    global died_1
    global died_2
    endgame = -1
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    running = True
    if n == 1:
        lose = load_image('tilt_1.jpg')
        died_1 += 1
    else:
        lose = load_image('tilt_2.jpg')
        died_2 += 1
    rect = pygame.Rect((700, 0, 100, 100))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    endgame = 0
                    start_the_game()
        lose_tr = pygame.transform.scale(lose, (800, 800))
        clock.tick(fps)
        screen.blit(lose_tr, (0, 0))
        pygame.display.flip()
    print(1)


def win_game(s1, s2):
    global endgame
    endgame = -1
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    running = True
    finish = load_image('win.jpg')
    flag = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                flag = True
        if not flag:
            if s1 + s2 == 10:
                intro_text = ['', '', '', '', '', 'Поздравляю, вы собрали все монеты!',
                              'Герои вернутся на свою планету крутыми']
            else:
                intro_text = ['', '', '', '', '', 'Вы не смогли собрать все монеты',
                              'Герои в печчали, теперь они бедные']

            font = pygame.font.SysFont('consolas', 20)
            text_coord = 700
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

            text = ['', '', '', '', '', f'Игрок 1 набрал {s1} монет',
                    f'Игрок 2: набрал {s2} монет']
            font = pygame.font.SysFont('consolas', 20)
            text_coord = 10
            for line in text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        else:
            animation_set = [pygame.image.load(f"animation_2/{i}.jpg") for i in range(1, 13)]
            i = 0
            screen.fill((0, 0, 0))
            screen.blit(pygame.transform.scale(animation_set[i // 12], (750, 750)), (0, 0))
            i += 1
            if i == 60:
                i = 0

        clock.tick(fps)
        pygame.display.flip()


class Player_1:
    def __init__(self, x, y):
        self.img = pygame.transform.scale(player_1_image, (45, 80))
        player_image_n = load_image('pln.png')
        self.img_n = pygame.transform.scale(player_image_n, (45, 80))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.speed_y = 0
        self.f = 1  # hero didn't jump
        self.flight = True
        self.flag_n = True

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

        # checking
        # collision with water
        for tile in level.water_list:
            if tile[1].collidepoint(self.rect.bottomright) or tile[1].collidepoint(self.rect.bottomleft):
                lose_game(1)
        # collision for jumping
        self.flight = True
        for tile in level.cloud:
            # in x coordinates
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                if tile[0] == img_c:
                    number_1 = 1
                dx = 0
            # in y coordinates
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # jumping
                if self.speed_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.speed_y = 0  # speed = 0 because we get in a normal state after jump
                # falling
                else:
                    dy = tile[1].top - self.rect.bottom
                    self.speed_y = 0
                    self.flight = False  # because he falls, so he is on the ground, we can jump after

        self.rect.x += dx
        self.rect.y += dy
        if self.flag_n:
            screen.blit(self.img, self.rect)
        else:
            screen.blit(self.img_n, self.rect)


class Player_2:
    def __init__(self, x, y):
        player_image = load_image('player2.png')
        self.img = pygame.transform.scale(player_image, (45, 80))
        player_image_n = load_image('playern.png')
        self.img_n = pygame.transform.scale(player_image_n, (45, 80))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
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

        # checking
        # collision with water
        for tile in level.water_list:
            if tile[1].collidepoint(self.rect.bottomright) or tile[1].collidepoint(self.rect.bottomleft):
                lose_game(2)
        # collision for jumping
        self.flight = True
        for tile in level.cloud:
            # in x coordinates
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                if tile[0] == img_c:
                    number_2 = 1
                dx = 0
            # in y coordinates
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # jumping
                if self.speed_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.speed_y = 0  # speed = 0 because we get in a normal state after jump
                # falling
                else:
                    dy = tile[1].top - self.rect.bottom
                    self.speed_y = 0
                    self.flight = False

        self.rect.x += dx
        self.rect.y += dy
        if self.flag_n:
            screen.blit(self.img, self.rect)
        else:
            screen.blit(self.img_n, self.rect)


class Level:
    def __init__(self, n):
        self.cloud = []
        self.water_list = []
        if n > 3:
            n = n - 3
        backgr_image = load_image(f'backgr{n}.jpg')
        self.background_image = pygame.transform.scale(backgr_image, (800, 800))
        block_image = load_image(f'dirt{n}.png')
        img1 = pygame.transform.scale(block_image, (sprite_size, sprite_size))
        dirt_image = load_image(f'block{n}.png')
        img = pygame.transform.scale(dirt_image, (sprite_size, sprite_size))
        water_image = load_image('water.png')
        img_w = pygame.transform.scale(water_image, (sprite_size, sprite_size))
        leve = load_level(f'level{n}.txt')
        r = 0
        for y in range(len(leve)):
            c = 0
            for x in range(len(leve[y])):
                if leve[y][x] == '1':
                    img_rect = img.get_rect()
                    img_rect.x = c * sprite_size
                    img_rect.y = r * sprite_size
                    tile = (img, img_rect)
                    self.cloud.append(tile)
                if leve[y][x] == '2':
                    img1_rect = img.get_rect()
                    img1_rect.x = c * sprite_size
                    img1_rect.y = r * sprite_size
                    tile = (img1, img1_rect)
                    self.cloud.append(tile)
                if leve[y][x] == '3':
                    imgc_rect = img.get_rect()
                    imgc_rect.x = c * sprite_size
                    imgc_rect.y = r * sprite_size
                    tile = (img_c, imgc_rect)
                    self.cloud.append(tile)
                if leve[y][x] == '4':
                    coin = Coin([c * sprite_size + sprite_size // 2, r * sprite_size + sprite_size // 2])
                if leve[y][x] == '*':
                    imgw_rect = img.get_rect()
                    imgw_rect.x = c * sprite_size
                    imgw_rect.y = r * sprite_size
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


def coin_screen(s1, s2, corr1, corr2):
    f1 = pygame.font.Font(None, 30)
    text1 = f1.render(f'Игрок 1: {s1} монет', True,
                      'white')
    f1 = pygame.font.Font(None, 30)
    text2 = f1.render(f'Игрок 2: {s2} монет', True,
                      'white')
    screen.blit(text1, (corr1[0], corr1[1]))
    screen.blit(text2, (corr2[0], corr2[1]))


def start_the_game():
    global endgame
    global level
    global num_level
    global number_1
    global number_2
    score_1 = 0
    score_2 = 0
    start_music.stop()
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    background_image = level.background_image

    player_1 = Player_1(100, 800 - 130)
    player_2 = Player_2(130, 800 - 130)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if number_1 == 1 and number_2 == 1:
            # start new level
            if endgame == 0:
                num_level += 1
            endgame = 0
            score_1 = 0
            score_2 = 0
            if num_level == 1 or num_level == 2:
                player_1 = Player_1(100, 800 - 130)
                player_2 = Player_2(130, 800 - 130)
            elif num_level == 3:
                win_game(score_1, score_2)
            else:
                player_1 = Player_1(100, 800 - 130)
                player_2 = Player_2(660, 800 - 130)

            level = Level(num_level)
            number_1 = 0
            number_2 = 0
        clock.tick(fps)
        screen.blit(background_image, (0, 0))
        level.draw()
        if pygame.sprite.spritecollide(player_1, coin_sprites, True):
            score_1 += 1
        if pygame.sprite.spritecollide(player_2, coin_sprites, True):
            score_2 += 1
        coin_screen(score_1, score_2, [50, 50], [585, 50])
        # if endgame != 0:
            # score_1 = 0
            # score_2 = 0
        coin_sprites.draw(screen)
        player_1.update()
        player_2.update()
        pygame.display.flip()


def about_function():
    # открытие файла txt с описанием правил игры
    animation_set = [pygame.image.load(f"animation/{i}.jpg") for i in range(1, 6)]
    window = pygame.display.set_mode((750, 750))
    clock = pygame.time.Clock()
    flag = True
    i = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_the_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                flag = False
        if flag:
            window.fill((0, 0, 0))
            window.blit(pygame.transform.scale(animation_set[i // 12], (750, 750)), (0, 0))
            intro_text = ['Наши герои летели на свои планету',
                        'Но на их корабли возникли неполадки и',
                        'пришлось совершить экстренное приземления на неизвестную планету.',
                        '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                        'К сожалению, при приземлении наши герои вылетели из корабля.',
                        'Нужно помочь им добраться до своего коробля преодолев несколько уровней',
                        'Не забывайте собирать монетки, которые выпали из корабля,',
                        'Иначе герои вернутся домой бедными((']
            font = pygame.font.SysFont('consolas', 19)
            text_coord = 10
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
            i += 1
            if i == 60:
                i = 0
        else:
            rule = load_image('rules.jpg')
            rules = pygame.transform.scale(rule, (750, 750))
            window.blit(rules, (0, 0))

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
