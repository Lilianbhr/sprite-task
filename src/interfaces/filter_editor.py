import pygame

from src.components.general import Div, Button


class FilterEditor(Div):
    def __init__(self, size: tuple, pos: tuple, conditions: dict):
        super().__init__(size, pos)
        self.conditions = conditions
        self.surface.fill((255, 255, 0))

        # Enregistrer
        self.save = Button(
            (100, 50),
            (0, 0),
            "enregistrer"
        )

        # Quitter
        self.quit = Button(
            (100, 50),
            (100, 0),
            "quitter"
        )

    def update(self, pos: tuple) -> str:
        if self.save.is_under(pos):
            return "enregistrer"

        elif self.quit.is_under(pos):
            return "quitter"

        else:
            return ""

    def display(self, screen: pygame.surface):
        self.save.display(self.surface)
        self.quit.display(self.surface)
        screen.blit(self.surface, self.hit_box)
