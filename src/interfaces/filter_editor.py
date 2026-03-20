import pygame

from src.components.general import Div, Button, CheckBox
from src.components.scale import Scale, DoubleScale


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

        # Réinitialiser
        self.reinitialize = Button(
            (100, 50),
            (200, 0),
            "reinitialiser"
        )

        # Fini
        self.fini = CheckBox((50, 50), (0, size[1] // 5))

        scales_size = (size[0], size[1] // 10)

        # Difficulté
        self.difficulte = DoubleScale(
            scales_size,
            (0, size[1] // 3),
            5,
            self.conditions["diff_min"],
            self.conditions["diff_max"]
        )

        # Longueur
        self.longueur = DoubleScale(
            scales_size,
            (0, self.difficulte.hit_box.bottom + 30),
            5,
            self.conditions["long_min"],
            self.conditions["long_max"]
        )

        self.set_info()

    def set_info(self):  # ------------------------------------------
        self.fini.state = self.conditions["fini"]
        self.fini.color_state()

        self.difficulte.set_limits(
            self.conditions["diff_min"],
            self.conditions["diff_max"]
        )

        self.longueur.set_limits(
            self.conditions["long_min"],
            self.conditions["long_max"]
        )

    def set_filter(self):  # ----------------------------------------
        self.conditions["fini"] = self.fini.state
        self.conditions["diff_min"] = self.difficulte.min_scale.value
        self.conditions["diff_max"] = self.difficulte.max_scale.value
        self.conditions["long_min"] = self.longueur.min_scale.value
        self.conditions["long_max"] = self.longueur.max_scale.value

    def update(self, pos: tuple) -> str:  # -------------------------
        if self.save.is_under(pos):
            return "enregistrer"

        elif self.quit.is_under(pos):
            return "quitter"

        elif self.reinitialize.is_under(pos):
            return "reinitialiser"

        elif self.fini.is_under(pos):
            self.fini.switch_state()

        elif self.difficulte.is_under(pos):
            d_pos = self.difficulte.get_relative_pos(pos)
            self.difficulte.update(d_pos)

        elif self.longueur.is_under(pos):
            s_pos = self.longueur.get_relative_pos(pos)
            self.longueur.update(s_pos)

        else:
            return ""

    def display(self, screen: pygame.surface):  # -------------------
        self.save.display(self.surface)
        self.quit.display(self.surface)
        self.reinitialize.display(self.surface)

        self.fini.display(self.surface)

        self.difficulte.display(self.surface)
        self.longueur.display(self.surface)

        screen.blit(self.surface, self.hit_box)
