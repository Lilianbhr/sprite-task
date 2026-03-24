import pygame
from core import Core
from src.constantes.theme import BG_COLOR
from src.interfaces.list_interface import TaskList

pygame.init()

# Window
screen = pygame.display.set_mode()
pygame.display.set_caption("SpriteTask")

# Core loop
mode = Core(screen)
clock = pygame.time.Clock()
running = True
pygame.key.set_repeat(400, 60)

while running:

    screen.fill(BG_COLOR)
    mode.run()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            mode.modify_input(key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mode.modify_input("mouse_click")

    mode.update_text(events)

    pygame.display.flip()
    clock.tick(60)

if type(mode.current_mode) is TaskList:
    mode.current_mode.body.database.close()
pygame.quit()
