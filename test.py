import pygame
import sys

animation_set = [pygame.image.load(f"animation/{i}.jpg") for i in range(1, 7)]

window = pygame.display.set_mode((550, 550))

clock = pygame.time.Clock()
i = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill((0,0,0))
    window.blit(animation_set[i // 12], (100, 20))
    i += 1
    if i == 60:
        i = 0

    pygame.display.flip()
    clock.tick(30)