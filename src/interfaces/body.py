import pygame

from src.components.general import Div
from src.database import Database

from src.interfaces.grid import Grid
from src.interfaces.task_editor import TaskEditor
from src.interfaces.filter_editor import FilterEditor


class Body(Div):
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos)

        self.database = Database()
        self.filter = {
            "fini": False,
            "diff_min": 1,
            "diff_max": 5,
            "long_min": 1,
            "long_max": 5
        }
        self.matching_tasks = self.database.select(self.filter)

        self.mode_code = 0  # 1 for task_editor, 2 for filter_editor
        self.grid = None
        self.task_editor = None
        self.filter_editor = None
        self.setup()

    def set_mode(self, mode: int):
        self.mode_code = mode
        self.setup()

    def setup(self):
        if self.mode_code:

            side_size = (2 * self.hit_box.width // 5, self.hit_box.height)
            side_pos = (self.hit_box.width - side_size[0], 0)

            if self.mode_code == 1:
                self.task_editor = TaskEditor(
                    side_size,
                    side_pos,
                    {
                        "fini": False,
                        "nom": "",
                        "description": "",
                        "difficulte": 1,
                        "longueur": 1
                    }
                )

            elif self.mode_code == 2:
                self.filter_editor = FilterEditor(
                    side_size,
                    side_pos,
                    {
                        "fini": False,
                        "diff_min": 1,
                        "diff_max": 5,
                        "long_min": 1,
                        "long_max": 5
                    }
                )

            self.grid = Grid(
                (3 * self.surface.get_width() // 5, self.hit_box.height),
                (0, 0),
                (3, 4)
            )

        else:
            self.grid = Grid(
                (self.hit_box.width, self.hit_box.height),
                (0, 0),
                (4, 4)
            )

    def update(self, b_pos=(-1, -1), modificator="", data=()):
        if self.grid.is_under(b_pos) and b_pos != (-1, -1):
            g_pos = self.grid.get_relative_pos(b_pos)

            for task in self.grid.elements:
                if task.is_under(g_pos):
                    t_pos = task.get_relative_pos(g_pos)

                    res = task.update(t_pos)
                    if res == "delete":
                        self.database.rm_task(task.spec)
                        self.matching_tasks = self.database.select(
                             self.filter
                        )
                        self.grid.fill_elements(self.matching_tasks)

                    elif res == "editor":
                        self.set_mode(1)
                        self.task_editor.task = task.spec
                        self.task_editor.set_info()

                    elif res == "end":
                        self.database.insert_task(task.spec)
                        self.matching_tasks = self.database.select(
                            self.filter
                        )
                        self.grid.fill_elements(self.matching_tasks)

        elif self.mode_code == 1:
            if modificator == "update_text":
                print("here")
                self.task_editor.update_text(data)
            else:
                if self.task_editor.is_under(b_pos):
                    t_pos = self.task_editor.get_relative_pos(b_pos)

                    res = self.task_editor.update(t_pos)
                    if res == "enregistrer":
                        self.database.insert_task(self.task_editor.task)
                        self.matching_tasks = self.database.select(
                            self.filter
                        )
                        self.set_mode(0)
                        self.grid.fill_elements(self.matching_tasks)

                    elif res == "quitter":
                        self.set_mode(0)

    def display(self, screen: pygame.Surface):
        self.grid.display(self.surface)
        if self.mode_code == 1:
            self.task_editor.display(self.surface)
        elif self.mode_code == 2:
            self.filter_editor.display(self.surface)
        screen.blit(self.surface, self.hit_box)
