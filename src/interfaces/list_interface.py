""" interface principale de l'application """

import pygame

from src.database import Database

from src.components.general import Div

from src.interfaces.control_bar import ControlBar
from src.interfaces.grid import Grid
from src.interfaces.task_editor import TaskEditor


class TaskList(Div):
    """
    La boite qui gère les interactions
    de l'utilisateur avec les éléments du menu.
    """
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos)

        # Fetch data
        self.database = Database()
        self.filter = {
            "fini": False,
            "diff_min": 1,
            "diff_max": 5,
            "long_min": 1,
            "long_max": 5
        }
        self.matching_tasks = self.database.select(self.filter)

        # Bar de contrôles
        self.control_bar = ControlBar(
            (self.surface.get_width(), self.surface.get_height() // 10),
            (0, 0)
        )

        # Grille + Éditeur de tâches
        self.grid = None
        self.editor = None
        self.setup_grid_only()

    def setup_grid_only(self):  # -----------------------------------

        # Grille
        self.grid = Grid(
            (self.surface.get_width(), 9 * self.surface.get_height() // 10),
            (0, self.control_bar.hit_box.bottom),
            (4, 4)
        )
        self.grid.fill_elements(self.matching_tasks)

        # Éditeur de tâches
        self.editor = None

    def setup_grid_editor(self):  # ---------------------------------

        # Grille
        self.grid = Grid(
            (
                3 * self.surface.get_width() // 5,
                9 * self.surface.get_height() // 10
            ),
            (0, self.control_bar.hit_box.bottom),
            (3, 4)
        )
        self.grid.fill_elements(self.matching_tasks)

        # Éditeur de tâches
        self.editor = TaskEditor(
            (
                2 * self.surface.get_width() // 5,
                9 * self.surface.get_height() // 10
            ),
            (self.grid.hit_box.right, self.control_bar.hit_box.bottom),
            {
                "fini": False,
                "nom": "",
                "description": "",
                "difficulté": 1,
                "longueur": 1
            }
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

                    # Barre de contrôle
                    ret = self.control_bar.update(bc_pos)
                    if ret:
                        self.setup_grid_editor()

                # Pos souris sur la grille
                elif self.grid.is_under(m_pos):
                    g_pos = self.grid.get_relative_pos(m_pos)

                    # Grille
                    for task in self.grid.elements:
                        res = task.update(g_pos)

                        if res == "delete":
                            self.database.rm_task(task.spec)
                            self.matching_tasks = self.database.select(
                                self.filter
                            )
                            self.grid.fill_elements(self.matching_tasks)

                        elif res == "editor":
                            self.setup_grid_editor()
                            self.editor.task = task.spec
                            self.editor.set_info()

                        elif res == "end":
                            self.database.insert_task(task.spec)
                            self.matching_tasks = self.database.select(
                                self.filter
                            )
                            self.grid.fill_elements(self.matching_tasks)

                # Pos souris sur l'éditeur de tâches
                elif self.editor is not None:
                    if self.editor.is_under(m_pos):

                        # Éditeur
                        e_pos = self.editor.get_relative_pos(m_pos)
                        res = self.editor.update(e_pos)

                        # Enregistrer
                        if res == "enregistrer":
                            self.editor.set_task()
                            self.database.insert_task(self.editor.task)
                            self.matching_tasks = self.database.select(
                                self.filter
                            )
                            self.grid.fill_elements(self.matching_tasks)
                            self.setup_grid_only()

                        # Quitter
                        elif res == "quitter":
                            self.setup_grid_only()

    def display(self, screen: pygame.Surface):  # -------------------
        self.surface.fill((0, 0, 0))
        self.control_bar.display(self.surface)
        self.grid.display(self.surface)
        if self.editor is not None:
            self.editor.display(self.surface)
        screen.blit(self.surface, self.hit_box)
