import pygame
import pygame_menu


pygame.init()
screen = pygame.display.set_mode((500, 600))
fon = pygame.image.load('fon.jpg')


def start_the_game():
    # Do the job here !
    pass

def about_function():
    #открытие файла txt с описанием правил игры
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