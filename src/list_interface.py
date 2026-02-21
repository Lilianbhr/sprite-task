import pygame
import general


class TaskList(general.Div):
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos)
        self.matching_tasks = []
        self.grid = Grid(self.surface.get_size(), (0, 0))

    def update(self, active_input: str):
        pass

    def display(self, screen: pygame.Surface):
        self.grid.display(self.surface)
        screen.blit(self.surface, self.hit_box)


class Grid(general.Div):
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos)
        self.nb_colonne = 4
        self.nb_ligne = 4
        self.tile_size = (size[0] // self.nb_colonne, size[1] // self.nb_ligne)
        self.elements = []

    def fill_elements(self, new_list: list):
        self.elements = []
        i = 0
        for elt in new_list:
            pos = ((i % 5) * self.tile_size[0], (i // 5) * self.tile_size[1])
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
        self.surface.fill((0, 255, 0))
        screen.blit(self.surface, self.hit_box)
