""" interface principale de l'application """

import pygame

from src.components.general import Div

from src.interfaces.control_bar import ControlBar
from src.interfaces.body import Body


class TaskList(Div):
    """
    La boite qui gère les interactions
    de l'utilisateur avec les éléments du menu.
    """
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos)
        # Bar de contrôles
        self.control_bar = ControlBar(
            (self.hit_box.width, self.hit_box.height // 10),
            (0, 0)
        )

        # Body
        self.body = Body(
            (self.hit_box.width, 9 * self.hit_box.height // 10),
            (0, self.control_bar.hit_box.bottom)
        )

    def update(self, active_input: str):  # -------------------------

        # Pos réel souris
        if active_input == "mouse_click":
            mouse_pos = pygame.mouse.get_pos()

            # Pos souris sur le menu
            if self.is_under(mouse_pos):
                m_pos = self.get_relative_pos(mouse_pos)

                # Pos souris sur la barre de contrôles
                if self.control_bar.is_under(m_pos):
                    bc_pos = self.control_bar.get_relative_pos(m_pos)

                    ret = self.control_bar.update(bc_pos)
                    if ret:
                        self.body.set_mode(1)

                # Pos souris sur le corps
                if self.body.is_under(m_pos):
                    b_pos = self.body.get_relative_pos(m_pos)
                    self.body.update(b_pos=b_pos)

    def display(self, screen: pygame.Surface):  # -------------------
        self.surface.fill((0, 0, 0))
        self.control_bar.display(self.surface)
        self.body.display(self.surface)
        screen.blit(self.surface, self.hit_box)
