import pygame

from src.components.general import Div, Button, CheckBox
from src.components.scale import Scale


class FilterEditor(Div):
    """ interface permettant de controller le filtre actif """
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

        # Fini
        self.fini = CheckBox((50, 50), (0, size[1] // 5))

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

        self.set_info()

    def set_info(self):  # ------------------------------------------
        self.fini.state = self.conditions["fini"]
        self.fini.color_state()

        self.diff_min.value = self.conditions["diff_min"]
        self.diff_min.set_elements()

        self.diff_max.value = self.conditions["diff_max"]
        self.diff_max.set_elements()

        self.long_min.value = self.conditions["long_min"]
        self.long_min.set_elements()

        self.long_max.value = self.conditions["long_max"]
        self.long_max.set_elements()

    def set_filter(self):  # ----------------------------------------
        self.conditions["fini"] = self.fini.state
        self.conditions["diff_min"] = self.diff_min.value
        self.conditions["diff_max"] = self.diff_max.value
        self.conditions["long_min"] = self.long_min.value
        self.conditions["long_max"] = self.long_max.value

    def update(self, pos: tuple) -> str:  # -------------------------
        if self.save.is_under(pos):
            return "enregistrer"

        elif self.quit.is_under(pos):
            return "quitter"

        elif self.fini.is_under(pos):
            self.fini.switch_state()

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

    def display(self, screen: pygame.surface):  # -------------------
        self.save.display(self.surface)
        self.quit.display(self.surface)

        self.fini.display(self.surface)

        self.diff_min.display(self.surface)
        self.diff_max.display(self.surface)
        self.long_min.display(self.surface)
        self.long_max.display(self.surface)

        screen.blit(self.surface, self.hit_box)
