import os
import sys

import pygame
import pygame_menu

pygame.init()
clock = pygame.time.Clock()
fps = 30
screen = pygame.display.set_mode((500, 600))
fon = pygame.image.load('data/fon.jpg')


def start_the_game():
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)

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

    player_image = load_image('player_1.png')
    background_image = load_image('backgr.png')

    class Player:
        def __init__(self, x, y):
            player_image = load_image('player_1.png')
            self.img = pygame.transform.scale(player_image, (40, 80))
            player_image_n = load_image('player_1_n.png')
            self.img_n = pygame.transform.scale(player_image_n, (40, 80))
            self.img_rect = self.img.get_rect()
            self.img_rect.x = x
            self.img_rect.y = y
            self.width = self.img.get_width()
            self.height = self.img.get_height()
            self.speed_y = 0
            self.f = 1  # hero didn't jump
            self.flag_n = True

        def update(self):
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
            if key[pygame.K_SPACE] and self.f == 1:
                self.speed_y = -15
                self.f = 0
            if not key[pygame.K_SPACE]:
                self.f = 1

            # gravity
            self.speed_y += 1
            if self.speed_y > 10:
                self.speed_y = 10
            dy += self.speed_y

            # checking
            for tile in level.cloud:
                # in x coordinates
                if tile[1].colliderect(self.img_rect.x + dx, self.img_rect.y, self.width, self.height):
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

            self.img_rect.x += dx
            self.img_rect.y += dy
            if self.flag_n:
                screen.blit(self.img, self.img_rect)
            else:
                screen.blit(self.img_n, self.img_rect)

    class Level:
        def __init__(self):
            self.cloud = []
            block_image = load_image('dirt2.png')
            img1 = pygame.transform.scale(block_image, (50, 50))
            dirt_image = load_image('block2.png')
            img = pygame.transform.scale(dirt_image, (50, 50))
            water_image = load_image('water.png')
            img_w = pygame.transform.scale(water_image, (50, 50))
            #water_dop_image = load_image('water_dop.png')
            # img_w1 = pygame.transform.scale(water_dop_image, (50, 50))
            leve = load_level('level1.txt')
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
                    if leve[y][x] == '*':
                        imgw_rect = img.get_rect()
                        imgw_rect.x = c * 50
                        imgw_rect.y = r * 50
                        tile = (img_w, imgw_rect)
                        self.cloud.append(tile)
                    #if leve[y][x] == '#':
                        #imgw1_rect = img.get_rect()
                        #imgw1_rect.x = c * 50
                       # imgw1_rect.y = r * 50
                       # tile = (img_w1, imgw1_rect)
                        #self.cloud.append(tile)
                    c += 1
                r += 1

        def draw(self):
            for tile in self.cloud:
                screen.blit(tile[0], tile[1])
                # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

    player = Player(100, 800 - 130)
    level = Level()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
        clock.tick(fps)
        screen.blit(background_image, (0, 0))
        level.draw()
        player.update()
        pygame.display.flip()


def about_function():
    # открытие файла txt с описанием правил игры
    pass


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
