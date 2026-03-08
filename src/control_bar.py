import pygame
import general


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
