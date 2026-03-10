"""
Ce fichier contient l'ensemble des ressources liées uniquement
à l'affichage du menu d'ouverture de l'application.
"""

import pygame

from src.components.general import Div
from src.components.general import get_screen_text_for


class Choose(Div):
    """
    La boite qui gère les interactions
    de l'utilisateur avec les éléments du menu.
    """
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos)
        self.elements = []
        self.set_elements()

    def set_elements(self):  # --------------------------------------

        # Tous les éléments ont la même taille
        surface_size = self.surface.get_size()
        tile_h = surface_size[1] // 4
        tile_w = surface_size[0]

        self.elements.append(
            Humeur("mood_1", "mood_1", (tile_w, tile_h), (0, 0))
        )
        self.elements.append(
            Humeur("mood_2", "mood_2", (tile_w, tile_h), (0, tile_h))
        )
        self.elements.append(
            Humeur("mood_3", "mood_3", (tile_w, tile_h), (0, tile_h * 2))
        )
        self.elements.append(
            Humeur("ignorer", "ignorer", (tile_w, tile_h), (0, tile_h * 3))
        )

    def update(self, active_input: str) -> str:  # ------------------

        # Position réel de la souris
        if active_input == "mouse_click":
            mouse_pos = pygame.mouse.get_pos()

            # Position relative sur le menu
            if self.is_under(mouse_pos):
                m_pos = self.get_relative_pos(mouse_pos)

                # Un élément du menu à été cliqué ?
                for elt in self.elements:
                    if elt.is_under(m_pos):
                        return elt.get_name()
        return ""

    def display(self, screen: pygame.Surface):  # -------------------
        for elt in self.elements:
            elt.display(self.surface)
        screen.blit(self.surface, self.hit_box)

# ============================================================================


class Humeur(Div):
    """
    Élément particulier du menu
    """
    def __init__(self, nom: str, description: str, size: tuple, pos: tuple):
        super().__init__(size, pos)
        self.nom = nom
        self.description = description
        self.surface.fill((255, 0, 0))

        # Nom - Exploitable par pygame ---------------
        self.text_nom = get_screen_text_for(self.nom, size[1] // 5)
        self.nom_rect = self.text_nom.get_rect()
        self.nom_rect.centery = size[1] // 2
        self.nom_rect.left = size[0] // 20

        # Description - Exploitable par pygame -------
        self.text_description = get_screen_text_for(
            self.description,
            size[1] // 7
        )
        self.description_rect = self.text_description.get_rect()
        self.description_rect.centery = size[1] // 2
        self.description_rect.left = self.nom_rect.right + 25

    def get_name(self):  # ------------------------------------------
        return self.nom

    def display(self, surface: pygame.Surface):  # ------------------
        self.surface.blit(self.text_nom, self.nom_rect)
        self.surface.blit(self.text_description, self.description_rect)
        surface.blit(self.surface, self.hit_box)
