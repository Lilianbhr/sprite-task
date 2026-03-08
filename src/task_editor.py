import general
import pygame
import pygame_textinput


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
            (size[0], size[1] // 8),
            (0, 100),
            3
        )

        # Description
        self.description_input = pygame_textinput.TextInputManager()
        self.description_visualizer = general.InputVisualizer(
            (size[0], size[1] // 4),
            (0, self.nom_visualizer.hit_box.bottom + 10),
            7
        )

        # Difficulté
        self.difficulty = general.Scale(
            (size[0], size[1] // 10),
            (0, self.description_visualizer.hit_box.bottom + 30),
            5
        )

        # Longueur
        self.longueur = general.Scale(
            (size[0], size[1] // 10),
            (0, self.difficulty.hit_box.bottom + 20),
            5
        )

        # Checkbox
        self.checkbox = general.CheckBox(
            (size[1] // 10, size[1] // 10),
            (0, self.longueur.hit_box.bottom + 30),
        )

    def set_task(self):
        self.task["nom"] = self.nom_visualizer.raw_text
        self.task["description"] = self.description_visualizer.raw_text
        self.task["difficulté"] = self.difficulty.value
        self.task["longueur"] = self.longueur.value
        self.task["fini"] = self.checkbox.state

    def set_info(self):

        # Nom
        self.nom_input.left = self.task["nom"]
        self.nom_visualizer.change_text(self.nom_input.left, "")
        self.nom_visualizer.screen_text.pop()

        # Description
        self.description_input.left = self.task["description"]
        self.description_visualizer.change_text(
            self.description_input.left, ""
        )
        self.description_visualizer.screen_text.pop()

        # Difficulté
        self.difficulty.value = self.task["difficulté"]
        self.difficulty.set_elements()

        # Longueur
        self.longueur.value = self.task["longueur"]
        self.longueur.set_elements()

        # Checkbox
        self.checkbox.state = self.task["fini"]
        self.checkbox.color_state()

    def update_text(self, events: pygame.event.Event):
        if self.selected_area is not None:
            if self.selected_area == "nom":
                self.nom_input.update(events)
                self.nom_visualizer.change_text(
                    self.nom_input.left,
                    self.nom_input.right
                )
            elif self.selected_area == "description":
                self.description_input.update(events)
                self.description_visualizer.change_text(
                    self.description_input.left,
                    self.description_input.right
                )

    def unselect_nom(self):
        if (
            self.nom_visualizer.visible
            and self.nom_visualizer.screen_text
        ):
            self.nom_visualizer.screen_text.pop()
        self.nom_visualizer.screen_text = self.nom_visualizer.wrap(
            self.nom_visualizer.raw_text
        )

    def unselect_description(self):
        if (
            self.description_visualizer.visible
            and self.description_visualizer.screen_text
        ):
            self.description_visualizer.screen_text.pop()
        self.description_visualizer.screen_text = self.description_visualizer.wrap(
            self.description_visualizer.raw_text
        )

    def update(self, pos: tuple) -> str:
        if self.save.is_under(pos):
            return "enregistrer"
        elif self.quit.is_under(pos):
            return "quitter"
        elif self.difficulty.is_under(pos):
            rel_pos = self.difficulty.get_relative_pos(pos)
            self.difficulty.update(rel_pos)
        elif self.longueur.is_under(pos):
            rel_pos = self.longueur.get_relative_pos(pos)
            self.longueur.update(rel_pos)
        elif self.checkbox.is_under(pos):
            self.checkbox.switch_state()
        else:

            # Sélection Nom
            if self.nom_visualizer.is_under(pos):
                self.selected_area = "nom"
                self.nom_input.left = self.nom_visualizer.raw_text
                self.nom_input.right = ""
                self.unselect_description()

            # Sélection Description
            elif self.description_visualizer.is_under(pos):
                self.selected_area = "description"
                self.description_input.left = self.description_visualizer.raw_text
                self.description_input.right = ""
                self.unselect_nom()

            # Déselection
            else:

                # Nom
                if self.selected_area == "nom":
                    self.unselect_nom()

                # Description
                elif self.selected_area == "description":
                    self.unselect_description()

                self.selected_area = None

        return ""

    def display(self, screen: pygame.surface):
        self.save.display(self.surface)
        self.quit.display(self.surface)
        self.nom_visualizer.display(self.surface)
        self.description_visualizer.display(self.surface)
        self.difficulty.display(self.surface)
        self.longueur.display(self.surface)
        self.checkbox.display(self.surface)
        screen.blit(self.surface, self.hit_box)
