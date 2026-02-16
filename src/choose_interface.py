import pygame


class Choose:
    def __init__(self, surface: pygame.Surface, pos):
        self.surface = surface
        self.pos = pos
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

    def update(self, active_input: str) -> str:
        if active_input == "mouse_click":
            mouse_pos = pygame.mouse.get_pos()
            for elt in self.elements:
                if elt.collided(mouse_pos):
                    return elt.get_name()
        return ""

    def display(self, screen: pygame.Surface):
        for elt in self.elements:
            elt.display(self.surface)
        screen.blit(self.surface, self.pos)


class Humeur:
    def __init__(self, nom: str, description: str, size: tuple, pos: tuple):
        self.nom = nom
        self.description = description
        self.surface = pygame.Surface(size)
        self.hit_box = self.surface.get_rect()
        self.hit_box.topleft = pos
        self.surface.fill((255, 0, 0))

    def get_name(self):
        return self.nom

    def collided(self, point: tuple) -> bool:
        if self.hit_box.collidepoint(point):
            return True
        return False

    def display(self, surface: pygame.Surface):
        surface.blit(self.surface, self.hit_box)
