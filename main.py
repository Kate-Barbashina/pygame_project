import os
import sys


import pygame
import pygame_menu

pygame.init()
screen = pygame.display.set_mode((500, 600))
fon = pygame.image.load('fon.jpg')


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

    player_image = load_image('creature.png')
    background_image = load_image('backgr.png')

    class Player:
        def __init__(self, x, y):
            player_image = load_image('creature.png')
            self.img = pygame.transform.scale(player_image, (40, 80))
            self.img_rect = self.img.get_rect()
            self.img_rect.x = x
            self.img_rect.y = y
            self.speed_y = 0
            self.f = 0

        def update(self):
            dx = 0
            dy = 0
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx -= 5
            if key[pygame.K_RIGHT]:
                dx += 5
            if key[pygame.K_SPACE] and self.f == 0:
                self.speed_y = -15
                self.f = 1
            if not key[pygame.K_SPACE]:
                self.f = 1
            if self.f == 0:
                self.speed_y += 5
                if self.speed_y > 10:
                    self.speed_y = 10
                dy += self.speed_y
            if self.img_rect.bottom > 800:
                dy = 0
                self.img_rect.bottom = 800
            self.img_rect.x += dx
            self.img_rect.y += dy
            screen.blit(self.img, self.img_rect)

    class Level:
        def __init__(self):
            self.cloud = []
            block_image = load_image('dirt1.png')
            img1 = pygame.transform.scale(block_image, (50, 50))
            dirt_image = load_image('block1.png')
            img = pygame.transform.scale(dirt_image, (50, 50))
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
                    c += 1
                r += 1

        def draw(self):
            for tile in self.cloud:
                screen.blit(tile[0], tile[1])

    player = Player(100, 800 - 130)
    level = Level()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            screen.blit(background_image, (0, 0))
            level.draw()
            player.update()
            pygame.display.flip()
    pygame.quit()


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

while True:

    screen.blit(fon, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()