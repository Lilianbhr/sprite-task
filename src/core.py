import pygame

from choose_interface import Choose
from list_interface import TaskList


class Core:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        surface_size = (
            2 * self.screen.get_width() // 3,
            2 * self.screen.get_height() // 3
        )
        surface_pos = (
            self.screen.get_width() // 2 - surface_size[0] // 2,
            self.screen.get_height() // 2 - surface_size[1] // 2
        )
        self.current_mode = Choose(surface_size, surface_pos)
        self.active_input = ""

    def modify_input(self, new: str) -> None:
        self.active_input = new

    def run(self):
        self.update()
        self.current_mode.display(self.screen)
        self.modify_input("")

    def update(self):
        ret = self.current_mode.update(self.active_input)
        if ret:
            size = (
                9 * self.screen.get_width() // 10,
                9 * self.screen.get_height() // 10
            )
            pos = (
                self.screen.get_width() // 2 - size[0] // 2,
                self.screen.get_height() // 2 - size[1] // 2
            )
            self.current_mode = TaskList(size, pos)
