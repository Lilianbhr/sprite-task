import pygame

from src.components.general import Div, Button
from src.components.scale import Scale


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

        scales_size = (size[0], size[1] // 20)

        # Diff_min
        self.diff_min = Scale(
            scales_size,
            (0, size[1] // 3),
            5
        )

        # Diff_max
        self.diff_max = Scale(
            scales_size,
            (0, self.diff_min.hit_box.bottom + 10),
            5,
            value=5,
            direction=-1
        )

        # Long_min
        self.long_min = Scale(
            scales_size,
            (0, self.diff_max.hit_box.bottom + 30),
            5
        )

        # Long_max
        self.long_max = Scale(
            scales_size,
            (0, self.long_min.hit_box.bottom + 10),
            5,
            value=5,
            direction=-1
        )

    def update(self, pos: tuple) -> str:
        if self.save.is_under(pos):
            return "enregistrer"

        elif self.quit.is_under(pos):
            return "quitter"

        elif self.diff_min.is_under(pos):
            s_pos = self.diff_min.get_relative_pos(pos)
            self.diff_min.update(s_pos)

        elif self.diff_max.is_under(pos):
            s_pos = self.diff_max.get_relative_pos(pos)
            self.diff_max.update(s_pos)

        elif self.long_min.is_under(pos):
            s_pos = self.long_min.get_relative_pos(pos)
            self.long_min.update(s_pos)

        elif self.long_max.is_under(pos):
            s_pos = self.long_max.get_relative_pos(pos)
            self.long_max.update(s_pos)

        else:
            return ""

    def display(self, screen: pygame.surface):
        self.save.display(self.surface)
        self.quit.display(self.surface)

        self.diff_min.display(self.surface)
        self.diff_max.display(self.surface)
        self.long_min.display(self.surface)
        self.long_max.display(self.surface)

        screen.blit(self.surface, self.hit_box)
