"""
Ce fichier contient l'ensemble des ressources liées uniquement
à l'affichage du menu principal de l'application.
"""

import pygame
import pygame_textinput
import general


class TaskList(general.Div):
    """
    La boite qui gère les interactions
    de l'utilisateur avec les éléments du menu.
    """
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos)
        self.matching_tasks = []

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
            {"nom": "task"}
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
                        if res:
                            self.matching_tasks.remove(task.spec)
                            self.grid.fill_elements(self.matching_tasks)

                # Pos souris sur l'éditeur de tâches
                elif self.editor is not None:
                    if self.editor.is_under(m_pos):

                        # Éditeur
                        e_pos = self.editor.get_relative_pos(m_pos)
                        ree = self.editor.update(e_pos)

                        # Enregistrer
                        if ree == "enregistrer":
                            nom = self.editor.nom_visualizer.raw_text
                            desc = self.editor.description_visualizer.raw_text
                            self.matching_tasks.append(
                                {
                                    "fini": False,
                                    "nom": nom,
                                    "description": desc,
                                    "difficulte": 3,
                                    "longueur": 2
                                }
                            )
                            self.grid.fill_elements(self.matching_tasks)
                            self.setup_grid_only()

                        # Quitter
                        elif ree == "quitter":
                            self.setup_grid_only()

    def display(self, screen: pygame.Surface):  # -------------------
        self.surface.fill((0, 0, 0))
        self.control_bar.display(self.surface)
        self.grid.display(self.surface)
        if self.editor is not None:
            self.editor.display(self.surface)
        screen.blit(self.surface, self.hit_box)

# ============================================================================


class ControlBar(general.Div):
    """
    Barre de contrôles, elle permet de réaliser
    différentes action à l'aide de boutons
    """
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos)
        self.surface.fill((0, 0, 255))

        # Texte - Exploitable par pygame
        self.text = general.get_screen_text_for("Control Bar", size[1] // 5)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (
            self.surface.get_width() // 2,
            self.surface.get_height() // 2
        )

        # Bouton - 'Ajouter'
        size_b = (size[0] // 10, 2 * size[1] // 3)
        self.ajouter = general.Button(size_b, (0, 0), "ajouter")
        self.ajouter.hit_box.right = 19 * size[0] // 20
        self.ajouter.hit_box.centery = size[1] // 2

    def update(self, pos: tuple) -> str:  # -------------------------
        if self.ajouter.is_under(pos):
            return "ajouter"
        return ""

    def display(self, screen: pygame.Surface):  # -------------------
        self.surface.blit(self.text, self.text_rect)
        self.ajouter.display(self.surface)
        screen.blit(self.surface, self.hit_box)

# ============================================================================


class Grid(general.Div):
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


class Task(general.Div):
    def __init__(self, size: tuple, pos: tuple, spec: dict):
        super().__init__(size, pos)
        self.spec = spec
        self.surface.fill((0, 0, 50))

        # Éléments
        self.ended = general.CheckBox(
            (size[1] // 5, size[1] // 5),
            (0, 0),
            spec["fini"]
        )
        self.delete = general.Button(
            (size[0] // 3, size[1] // 5),
            (size[1] // 5 + 5, 0),
            "supprimer"
        )
        self.nom = general.Text(
            (9 * size[0] // 10, 2 * size[1] // 3),
            (size[0] // 20, size[1] // 5 + 5),
            spec["nom"],
            size[1] // 7
        )
        self.effort = general.get_screen_text_for(
            str((spec["difficulte"] + spec["longueur"])/2), size[1] // 5
        )
        self.effort_rect = self.effort.get_rect()
        self.effort_rect.topright = (size[0], 0)

    def update(self, pos: tuple) -> str:  # -------------------------
        t_pos = self.get_relative_pos(pos)

        # Checkbox
        if self.ended.is_under(t_pos):
            self.ended.switch_state()
            self.spec["fini"] = self.ended.get_state()

        # Delete
        elif self.delete.is_under(t_pos):
            return "delete"

        return ""

    def display(self, screen: pygame.Surface):  # -------------------
        self.ended.display(self.surface)
        self.delete.display(self.surface)
        self.nom.display(self.surface)
        self.surface.blit(self.effort, self.effort_rect)
        screen.blit(self.surface, self.hit_box)

# ============================================================================


class TaskEditor(general.Div):
    def __init__(self, size: tuple, pos: tuple, task: dict):
        super().__init__(size, pos)
        self.task = task
        self.surface.fill((255, 0, 0))
        self.selected_area = None

        # Enregistrer
        self.save = general.Button(
            (100, 50),
            (0, 0),
            "enregistrer"
        )

        # Quitter
        self.quit = general.Button(
            (100, 50),
            (100, 0),
            "quitter"
        )

        # Nom
        self.nom_input = pygame_textinput.TextInputManager()
        self.nom_visualizer = general.InputVisualizer(
            (size[0], size[1] // 4),
            (0, 100)
        )

        # Description
        self.description_input = pygame_textinput.TextInputManager()
        self.description_visualizer = general.InputVisualizer(
            (size[0], size[1] // 4),
            (0, 500)
        )

    def update_text(self, events: pygame.event.Event):
        if self.selected_area is not None:
            if self.selected_area == self.nom_input:
                self.nom_input.update(events)
                self.nom_visualizer.change_text(
                    self.nom_input.left,
                    self.nom_input.right
                )
            elif self.selected_area == self.description_input:
                self.description_input.update(events)
                self.description_visualizer.change_text(
                    self.description_input.left,
                    self.description_input.right
                )

    def update(self, pos: tuple) -> str:
        if self.save.is_under(pos):
            return "enregistrer"
        elif self.quit.is_under(pos):
            return "quitter"
        else:

            # Sélection Nom
            if self.nom_visualizer.is_under(pos):
                self.selected_area = self.nom_input
                if (
                    self.description_visualizer.visible
                    and self.description_visualizer.screen_text
                ):
                    self.description_visualizer.screen_text.pop()

            # Sélection Description
            elif self.description_visualizer.is_under(pos):
                self.selected_area = self.description_input
                if (
                    self.nom_visualizer.visible
                    and self.nom_visualizer.screen_text
                ):
                    self.nom_visualizer.screen_text.pop()

            # Déselection
            else:

                # Nom
                if self.selected_area == self.nom_input:
                    if (
                        self.nom_visualizer.visible
                        and self.nom_visualizer.screen_text
                    ):
                        self.nom_visualizer.screen_text.pop()

                # Description
                elif self.selected_area == self.description_input:
                    if (
                        self.description_visualizer.visible
                        and self.description_visualizer.screen_text
                    ):
                        self.description_visualizer.screen_text.pop()

                self.selected_area = None

        return ""

    def display(self, screen: pygame.surface):
        self.save.display(self.surface)
        self.quit.display(self.surface)
        self.nom_visualizer.display(self.surface)
        self.description_visualizer.display(self.surface)
        screen.blit(self.surface, self.hit_box)
