import pygame
import general


class Choose:
    def __init__(self, surface: pygame.Surface, pos):
        self.surface = surface
        self.pos = pos
        self.elements = []
        self.set_elements()
        self.interface_rect = self.surface.get_rect()
        self.interface_rect.topleft = pos

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

    def update(self, active_input: str) -> str:
        if active_input == "mouse_click":
            mouse_pos = pygame.mouse.get_pos()
            for elt in self.elements:
                if self.interface_rect.collidepoint(mouse_pos):
                    m_pos = (
                        mouse_pos[0] - self.pos[0],
                        mouse_pos[1] - self.pos[1]
                    )
                    if elt.collided(m_pos):
                        return elt.get_name()
        return ""

    def display(self, screen: pygame.Surface):
        for elt in self.elements:
            elt.display(self.surface)
        screen.blit(self.surface, self.interface_rect)


class Humeur:
    def __init__(self, nom: str, description: str, size: tuple, pos: tuple):
        self.nom = nom
        self.description = description

        self.screen_text_nom = general.get_screen_text_for(self.nom, size[1] // 5)
        self.screen_nom_rect = self.screen_text_nom.get_rect()
        self.screen_nom_rect.centery = size[1] // 2
        self.screen_nom_rect.centerx = size[0] // 10

        self.screen_description = general.get_screen_text_for(
            self.description,
            size[1] // 7
        )
        self.description_rect = self.screen_description.get_rect()
        self.description_rect.centery = size[1] // 2
        self.description_rect.left = self.screen_nom_rect.right + 25

        self.surface = pygame.Surface(size)
        self.hit_box = self.surface.get_rect()
        self.hit_box.topleft = pos
        print(self.hit_box)
        self.surface.fill((255, 0, 0))

    def get_name(self):
        return self.nom

    def collided(self, point: tuple) -> bool:
        if self.hit_box.collidepoint(point):
            return True
        return False

    def display(self, surface: pygame.Surface):
        self.surface.blit(self.screen_text_nom, self.screen_nom_rect)
        self.surface.blit(self.screen_description, self.description_rect)
        surface.blit(self.surface, self.hit_box)

    def __str__(self):
        res = f"name : {self.nom}"
        return res
