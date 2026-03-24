""" menu d'ouverture de l'application. """

import pygame

from src.components.general import Div
from src.components.general import get_screen_text_for
from src.constantes.theme import SCRAP_COLOR, STRIKE_COLOR, WARLORD_COLOR, OMNICYDE_COLOR, BORDERS_COLOR, BG_COLOR


class Choose(Div):
    """
    La boite qui gère les interactions
    de l'utilisateur avec les éléments du menu.
    """
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos, BG_COLOR)
        self.elements = []
        self.gap = size[1] // 20
        self.set_elements()

    def set_elements(self):  # --------------------------------------

        # Tous les éléments ont la même taille
        surface_size = self.surface.get_size()
        tile_h = (surface_size[1] - self.gap * 3) // 4
        tile_w = surface_size[0]

        self.elements.append(
            Humeur(
                "SCRAP HUNTER",
                "Récupération rapide. Élimine les cibles mineures sans pitié.",
                (tile_w, tile_h),
                (0, 0),
                SCRAP_COLOR,
                BORDERS_COLOR
            )
        )
        self.elements.append(
            Humeur(
                "STRIKE COMMANDER",
                "Tactique et efficace. Nettoyage de zone en cours.",
                (tile_w, tile_h),
                (0, tile_h + self.gap),
                STRIKE_COLOR,
                BORDERS_COLOR
            )
        )
        self.elements.append(
            Humeur(
                "WARLORD OVERDRIVE",
                "Écrase les boss de ta liste. Engagement total exigé.",
                (tile_w, tile_h),
                (0, (tile_h + self.gap) * 2),
                WARLORD_COLOR,
                BORDERS_COLOR
            )
        )
        self.elements.append(
            Humeur(
                "OMNICYDE PROTOCOL",
                "Aucune distinction, toutes les cibles sont prioritaires.",
                (tile_w, tile_h),
                (0, (tile_h + self.gap) * 3),
                OMNICYDE_COLOR,
                BORDERS_COLOR
            )
        )

    def update(self, active_input: str) -> str:  # ------------------
        self.surface.fill(self.color)

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
    def __init__(self, nom: str, description: str,
                 size: tuple, pos: tuple, text_color: tuple, color: tuple):
        super().__init__(size, pos, color)
        self.nom = nom
        self.description = description
        self.text_color = text_color

        # Nom - Exploitable par pygame ---------------
        self.text_nom = get_screen_text_for(
            self.nom, size[1] // 5, self.text_color
        )
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
        self.surface.fill(self.color)
        self.surface.blit(self.text_nom, self.nom_rect)
        self.surface.blit(self.text_description, self.description_rect)
        surface.blit(self.surface, self.hit_box)
