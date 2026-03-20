import pygame

from src.components.general import Div
from src.components.general import get_screen_text_for
from src.components.general import Button


class ControlBar(Div):
    """
    Barre de contrôles, elle permet de réaliser
    différentes action à l'aide de boutons
    """
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos)
        self.surface.fill((0, 0, 255))
        size_b = (size[0] // 10, 2 * size[1] // 3)

        # Texte - Exploitable par pygame
        self.text = get_screen_text_for("Control Bar", size[1] // 5)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (
            self.surface.get_width() // 2,
            self.surface.get_height() // 2
        )

        # Bouton - 'Ajouter'
        self.ajouter = Button(size_b, (0, 0), "ajouter")
        self.ajouter.hit_box.right = 19 * size[0] // 20
        self.ajouter.hit_box.centery = size[1] // 2

        # Bouton - 'Filtrer'
        self.filtrer = Button(size_b, (0, 0), "filtrer")
        self.filtrer.hit_box.right = self.ajouter.hit_box.left - 10
        self.filtrer.hit_box.centery = size[1] // 2

    def update(self, pos: tuple) -> str:  # -------------------------
        if self.ajouter.is_under(pos):
            return "ajouter"

        elif self.filtrer.is_under(pos):
            return "filtrer"

        return ""

    def display(self, screen: pygame.Surface):  # -------------------
        self.surface.blit(self.text, self.text_rect)
        self.ajouter.display(self.surface)
        self.filtrer.display(self.surface)
        screen.blit(self.surface, self.hit_box)
