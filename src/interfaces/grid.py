import pygame

from src.components.general import Div
from src.components.general import CheckBox
from src.components.general import Button
from src.components.general import get_screen_text_for

from src.components.text import Text


class Grid(Div):
    """
    Grille d'affichage des tâches, elle permet d'afficher et de manager
    les tâches auquelles elle est associée en leur donnant une taille identique
    et une position dynamique.
    """
    def __init__(self, size: tuple, pos: tuple, layout_size: tuple):
        super().__init__(size, pos)
        self.elements = []
        self.gap = size[0] // 100

        # Dimensions de la grille
        self.nb_colonne = layout_size[0]
        self.nb_ligne = layout_size[1]
        self.tile_size = (
            (size[0] - self.gap) // self.nb_colonne - self.gap,
            (size[1] - self.gap) // self.nb_ligne - self.gap
        )

    def fill_elements(self, new_list: list):  # ---------------------
        """ Construction dynamique des tâches """
        self.elements = []
        i = 0
        for elt in new_list:
            pos = (
                self.gap + (i % self.nb_colonne) * (self.tile_size[0] + self.gap),
                self.gap + (i // self.nb_colonne) * (self.tile_size[1] + self.gap)
            )
            task = Task(self.tile_size, pos, elt)
            self.elements.append(task)
            i += 1

    def display(self, screen: pygame.Surface):  # -------------------
        self.surface.fill((0, 255, 0))
        for elt in self.elements:
            elt.display(self.surface)
        screen.blit(self.surface, self.hit_box)

# ============================================================================


class Task(Div):
    """ Élément qui constitue la grille """
    def __init__(self, size: tuple, pos: tuple, spec: dict):
        super().__init__(size, pos)
        self.spec = spec
        self.surface.fill((0, 0, 50))

        # Éléments
        self.ended = CheckBox(
            (size[1] // 5, size[1] // 5),
            (0, 0),
            spec["fini"]
        )
        self.delete = Button(
            (size[0] // 3, size[1] // 5),
            (size[1] // 5 + 5, 0),
            "supprimer"
        )
        self.nom = Text(
            (9 * size[0] // 10, 2 * size[1] // 3),
            (size[0] // 20, size[1] // 5 + 5),
            spec["nom"],
            size[1] // 7
        )
        self.effort = get_screen_text_for(
            str((spec["difficulte"] + spec["longueur"])/2), size[1] // 5
        )
        self.effort_rect = self.effort.get_rect()
        self.effort_rect.topright = (size[0], 0)

    def update(self, pos: tuple) -> str:  # -------------------------

        # Checkbox
        if self.ended.is_under(pos):
            self.ended.switch_state()
            self.spec["fini"] = self.ended.get_state()
            return "end"

        # Delete
        elif self.delete.is_under(pos):
            return "delete"

        elif self.nom.is_under(pos):
            return "editor"

        return ""

    def display(self, screen: pygame.Surface):  # -------------------
        self.ended.display(self.surface)
        self.delete.display(self.surface)
        self.nom.display(self.surface)
        self.surface.blit(self.effort, self.effort_rect)
        screen.blit(self.surface, self.hit_box)
