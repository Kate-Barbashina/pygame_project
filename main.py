import os
import sys

import pygame

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


level = Level()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        screen.blit(background_image, (0, 0))
        level.draw()
        pygame.display.flip()
pygame.quit()
