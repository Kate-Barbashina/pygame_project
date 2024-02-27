import pygame
import sys

animation_set = [pygame.image.load(f"animation/{i}.jpg") for i in range(1, 7)]

window = pygame.display.set_mode((550, 550))
intro_text = ["Наши герои летели домой", "",
                "Но на космическом корабле случились неполадки",
                "Корабль упал где-то на другой планете",
                "Нужно помочь нашим героям как можно быстрее добраться до корабля"
                "Иначе они не выживут на чужой планете"]

    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        window.blit(string_rendered, intro_rect)
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