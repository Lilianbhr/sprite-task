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

        # Activation/désactivation de l'éditeur de tâches
        if active_input == "space":
            if self.editor is None:
                self.setup_grid_editor()
            else:
                self.setup_grid_only()

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
                        self.matching_tasks.append(
                            {
                                "fini": False,
                                "nom": "J'arrive, je mets mes chaussures..."
                            }
                        )
                        self.grid.fill_elements(self.matching_tasks)

                # Pos souris sur la grille
                if self.grid.is_under(m_pos):
                    g_pos = self.grid.get_relative_pos(m_pos)

                    # Grille
                    for task in self.grid.elements:
                        res = task.update(g_pos)
                        if res:
                            self.matching_tasks.remove(task.spec)
                            self.grid.fill_elements(self.matching_tasks)

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

    def update(self, pos: tuple) -> str:  # -------------------------
        t_pos = self.get_relative_pos(pos)
        if self.ended.is_under(t_pos):
            self.ended.switch_state()
            self.spec["fini"] = self.ended.get_state()
        elif self.delete.is_under(t_pos):
            return "delete"
        return ""

    def display(self, screen: pygame.Surface):  # -------------------
        self.ended.display(self.surface)
        self.delete.display(self.surface)
        self.nom.display(self.surface)
        screen.blit(self.surface, self.hit_box)

# ============================================================================


class TaskEditor(general.Div):
    def __init__(self, size: tuple, pos: tuple, task: dict):
        super().__init__(size, pos)
        self.surface.fill((255, 0, 0))
        self.task = task
        self.selected_area = None
        self.nom = pygame_textinput.TextInputVisualizer()
        self.description = pygame_textinput.TextInputVisualizer()

    def display(self, screen: pygame.surface):
        screen.blit(self.surface, self.hit_box)
