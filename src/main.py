import pygame
from core import Core
pygame.init()

# Window
screen = pygame.display.set_mode()
pygame.display.set_caption("SpriteTask")
background_color = (255, 255, 255)

# Core loop
mode = Core(screen)
clock = pygame.time.Clock()
running = True
while running:

    screen.fill(background_color)
    mode.run()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            mode.modify_input(key)
        elif pygame.mouse.get_pressed() == (1, 0, 0):
            mode.modify_input("mouse_click")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
