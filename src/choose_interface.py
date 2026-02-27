import pygame
import general


class Choose(general.Div):
    def __init__(self, size: tuple, pos: tuple):
        super().__init__(size, pos)
        self.elements = []
        self.set_elements()

    def set_elements(self):
        surface_size = self.surface.get_size()
        tile_h = surface_size[1] // 4
        tile_w = surface_size[0]

        self.elements.append(
            Humeur("mood_1", "mood_1", (tile_w, tile_h), (0, 0))
        )
        self.elements.append(
            Humeur("mood_2", "mood_2", (tile_w, tile_h), (0, tile_h))
        )
        self.elements.append(
            Humeur("mood_3", "mood_3", (tile_w, tile_h), (0, tile_h * 2))
        )
        self.elements.append(
            Humeur("ignorer", "ignorer", (tile_w, tile_h), (0, tile_h * 3))
        )

    def update(self, active_input: str) -> str:
        if active_input == "mouse_click":
            mouse_pos = pygame.mouse.get_pos()
            for elt in self.elements:
                if self.is_under(mouse_pos):
                    m_pos = self.get_relative_pos(mouse_pos)
                    if elt.is_under(m_pos):
                        return elt.get_name()
        return ""

    def display(self, screen: pygame.Surface):
        for elt in self.elements:
            elt.display(self.surface)
        screen.blit(self.surface, self.hit_box)


class Humeur(general.Div):
    def __init__(self, nom: str, description: str, size: tuple, pos: tuple):
        super().__init__(size, pos)
        self.nom = nom
        self.description = description

        self.text_nom = general.get_screen_text_for(self.nom, size[1] // 5)
        self.nom_rect = self.text_nom.get_rect()
        self.nom_rect.centery = size[1] // 2
        self.nom_rect.left = size[0] // 20

        self.text_description = general.get_screen_text_for(
            self.description,
            size[1] // 7
        )
        self.description_rect = self.text_description.get_rect()
        self.description_rect.centery = size[1] // 2
        self.description_rect.left = self.nom_rect.right + 25

        self.surface.fill((255, 0, 0))

    def get_name(self):
        return self.nom

    def display(self, surface: pygame.Surface):
        self.surface.blit(self.text_nom, self.nom_rect)
        self.surface.blit(self.text_description, self.description_rect)
        surface.blit(self.surface, self.hit_box)
