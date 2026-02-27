import pygame
import pygame_textinput
import general

type_t = {
    "nom": "",
    "description": "",
    "fini": False,
    "difficulte": 0,
    "longueur": 0
}


class TaskList(general.Div):
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos)
        self.matching_tasks = []
        self.control_bar = ControlBar(
            (self.surface.get_width(), self.surface.get_height() // 10),
            (0, 0)
        )
        self.grid = Grid(
            (self.surface.get_width(), 9 * self.surface.get_height() // 10),
            (0, self.control_bar.hit_box.bottom),
            (4, 4)
        )
        self.editor = None
        self.grid.fill_elements(self.matching_tasks)

    def update(self, active_input: str):
        if active_input == "space":
            if self.editor is None:
                self.grid = Grid(
                    (
                        3 * self.surface.get_width() // 5,
                        9 * self.surface.get_height() // 10
                    ),
                    (0, self.control_bar.hit_box.bottom),
                    (3, 4)
                )
                self.editor = TaskEditor(
                    (
                        2 * self.surface.get_width() // 5,
                        9 * self.surface.get_height() // 10
                    ),
                    (self.grid.hit_box.right, self.control_bar.hit_box.bottom),
                    {"nom": "task"}
                )
                self.grid.fill_elements(self.matching_tasks)
            else:
                self.grid = Grid(
                    (self.surface.get_width(), 9 * self.surface.get_height() // 10),
                    (0, self.control_bar.hit_box.bottom),
                    (4, 4)
                )
                self.editor = None
                self.grid.fill_elements(self.matching_tasks)
        if active_input == "mouse_click":
            mouse_pos = pygame.mouse.get_pos()
            if self.is_under(mouse_pos):
                rel_pos = self.get_relative_pos(mouse_pos)
                if self.control_bar.is_under(rel_pos):
                    pos = self.control_bar.get_relative_pos(rel_pos)
                    ret = self.control_bar.update(pos)
                    if ret:
                        self.matching_tasks.append(type_t)
                        self.grid.fill_elements(self.matching_tasks)

    def display(self, screen: pygame.Surface):
        self.surface.fill((0, 0, 0))
        self.control_bar.display(self.surface)
        self.grid.display(self.surface)
        if self.editor is not None:
            self.editor.display(self.surface)
        screen.blit(self.surface, self.hit_box)


class ControlBar(general.Div):
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos)
        self.surface.fill((0, 0, 255))

        self.text = general.get_screen_text_for("Control Bar", size[1] // 5)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (
            self.surface.get_width() // 2,
            self.surface.get_height() // 2
        )

        size_b = (size[0] // 10, 2 * size[1] // 3)
        self.ajouter = general.Button(size_b, (0, 0), "ajouter")
        self.ajouter.hit_box.right = 19 * size[0] // 20
        self.ajouter.hit_box.centery = size[1] // 2

    def update(self, pos: tuple) -> str:
        if self.ajouter.is_under(pos):
            return "ajouter"
        return ""

    def display(self, screen: pygame.Surface):
        self.surface.blit(self.text, self.text_rect)
        self.ajouter.display(self.surface)
        screen.blit(self.surface, self.hit_box)


class Grid(general.Div):
    def __init__(self, size: tuple, pos: tuple, layout_size: tuple):
        super().__init__(size, pos)
        self.nb_colonne = layout_size[0]
        self.nb_ligne = layout_size[1]
        self.tile_size = (size[0] // self.nb_colonne, size[1] // self.nb_ligne)
        self.elements = []
        self.surface.fill((0, 255, 0))

    def fill_elements(self, new_list: list):
        self.elements = []
        i = 0
        for elt in new_list:
            pos = ((i % self.nb_colonne) * self.tile_size[0], (i // self.nb_colonne) * self.tile_size[1])
            task = Task(self.tile_size, pos, elt)
            self.elements.append(task)
            i += 1

    def display(self, screen: pygame.Surface):
        for elt in self.elements:
            elt.display(self.surface)
        screen.blit(self.surface, self.hit_box)


class Task(general.Div):
    def __init__(self, size: tuple, pos: tuple, spec: dict):
        super().__init__(size, pos)
        self.nom = spec["nom"]
        self.description = spec["description"]
        self.fini = spec["fini"]
        self.difficulte = spec["difficulte"]
        self.longueur = spec["longueur"]

    def display(self, screen: pygame.Surface):
        self.surface.fill((0, 0, 50))
        screen.blit(self.surface, self.hit_box)


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
