import pygame
from src.components.general import Div


class Scale(Div):
    """ Permet la séléction d'une valeur dans [1;max_value] """
    def __init__(self, size: tuple, pos: tuple, max_value: int,
                 value=1, direction=1):
        super().__init__(size, pos)
        self.max_value = max_value
        self.value = value
        self.direction = direction
        self.gap = size[0] // 50

        self.elements = []
        self.set_elements()

    def set_elements(self):  # --------------------------------------
        self.elements = []

        # Largeur des éléments
        grad_width = ((self.hit_box.width - self.gap * (self.max_value - 1))
                      // self.max_value)

        # Création des graduation dynamiquement
        x = 0
        for value in range(1, self.max_value + 1):

            # Rendu visuel en fonction de la valeur actuelle
            boolean = False
            if value * self.direction <= self.value * self.direction:
                boolean = True

            # Ajout des éléments à la liste
            self.elements.append(
                Graduation(
                    (grad_width, self.hit_box.height),
                    (x, 0),
                    boolean,
                    value
                )
            )

            # Pos
            x += grad_width + self.gap

    def update(self, rel_pos: tuple):  # ----------------------------
        for elt in self.elements:
            if elt.is_under(rel_pos):
                self.value = elt.value
        self.set_elements()

    def display(self, screen: pygame.Surface):  # -------------------
        for elt in self.elements:
            elt.display(self.surface)
        screen.blit(self.surface, self.hit_box)

# ============================================================================


class Graduation(Div):
    """ Élément qui constitue Scale """
    def __init__(self, size: tuple, pos: tuple, active: bool, value: int):
        super().__init__(size, pos)
        self.active = active
        self.value = value
        self.set_color()

    def set_color(self):  # -----------------------------------------
        if self.active:
            self.surface.fill((100, 0, 200))
        else:
            self.surface.fill((100, 100, 100))

    def display(self, screen: pygame.Surface):  # -------------------
        screen.blit(self.surface, self.hit_box)
