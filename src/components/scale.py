import pygame
from src.components.general import Div


class Scale(Div):
    """ Permet la séléction d'une valeur dans [1;max_value] """
    def __init__(self, size: tuple, pos: tuple, max_value: int,
                 value=1, direction=1, limit=6):
        super().__init__(size, pos)

        # Values
        self.max_value = max_value
        self.value = value
        self.direction = direction
        self.limit = limit

        # Visuel
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
            active = 0
            if value * self.direction <= self.value * self.direction:
                active = 1
            elif value * self.direction > self.limit * self.direction:
                active = -1

            # Ajout des éléments à la liste
            self.elements.append(
                Graduation(
                    (grad_width, self.hit_box.height),
                    (x, 0),
                    active,
                    value
                )
            )

            # Pos
            x += grad_width + self.gap

    def update(self, rel_pos: tuple):  # ----------------------------
        for elt in self.elements:
            if elt.is_under(rel_pos):
                self.value = elt.value
                if self.value * self.direction >= self.limit * self.direction:
                    self.value = self.limit
        self.set_elements()

    def display(self, screen: pygame.Surface):  # -------------------
        for elt in self.elements:
            elt.display(self.surface)
        screen.blit(self.surface, self.hit_box)

# ============================================================================


class DoubleScale(Div):
    def __init__(self, size: tuple, pos: tuple, range_size: int, mini: int, maxi: int):
        super().__init__(size, pos)
        self.range_size = range_size
        self.gap = size[1] // 10

        self.min_scale = Scale(
            (size[0], size[1] // 2),
            (0, 0),
            range_size,
            value=mini,
            limit=maxi
        )
        self.max_scale = Scale(
            (size[0], size[1] // 2),
            (0, self.min_scale.hit_box.bottom + self.gap),
            range_size,
            value=maxi,
            direction=-1,
            limit=mini
        )

    def set_limits(self, mini, maxi):
        self.min_scale.limit = maxi
        self.max_scale.limit = mini

        self.min_scale.set_elements()
        self.max_scale.set_elements()

    def update(self, pos):
        if self.min_scale.is_under(pos):
            m_pos = self.min_scale.get_relative_pos(pos)
            self.min_scale.update(m_pos)

        elif self.max_scale.is_under(pos):
            m_pos = self.max_scale.get_relative_pos(pos)
            self.max_scale.update(m_pos)

        self.set_limits(self.min_scale.value, self.max_scale.value)

    def display(self, screen: pygame.Surface):
        self.min_scale.display(self.surface)
        self.max_scale.display(self.surface)
        screen.blit(self.surface, self.hit_box)
# ============================================================================


class Graduation(Div):
    """ Élément qui constitue Scale """
    def __init__(self, size: tuple, pos: tuple, active: int, value: int):
        super().__init__(size, pos)
        self.active = active
        self.value = value
        self.set_color()

    def set_color(self):  # -----------------------------------------
        if self.active < 0:
            self.surface.fill((50, 50, 50))
        elif self.active:
            self.surface.fill((100, 0, 200))
        else:
            self.surface.fill((100, 100, 100))

    def display(self, screen: pygame.Surface):  # -------------------
        screen.blit(self.surface, self.hit_box)
