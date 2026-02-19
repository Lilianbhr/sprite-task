import pygame

import general


class TaskList(general.Div):
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos)
        pass

    def update(self, active_input: str):
        pass

    def display(self, screen: pygame.Surface):
        screen.blit(self.surface, self.hit_box)
