import pygame
from text import Text


class InputVisualizer(Text):
    """ Permet la visualisation correct d'un champ de texte (input) """
    def __init__(self, size: tuple, pos: tuple, lines_count: int, left="", right=""):
        super().__init__(size, pos, left + right, size[1] // lines_count)
        self.left = left
        self.right = right

        # Cursor
        self.cursor = pygame.Surface((3, self.font_size))
        self.cursor.fill((255, 255, 255))
        self.cursor_rect = self.cursor.get_rect()

        # Cursor visibility
        self.time = pygame.time.Clock()
        self.interval = 500
        self.reste = 0
        self.visible = True

    def change_text(self, left="", right=""):  # --------------------

        # réinitialisation clignotement curseur
        if left != self.left:
            self.reste = 0
            self.visible = True

        # Modifications des strings
        self.left = left
        self.right = right
        self.raw_text = self.left + self.right
        self.wrap_input()

    def wrap_input(self):  # ----------------------------------------

        # Réinitialisation de la pos du curseur
        self.cursor_rect.topleft = (0, 0)

        # wrap partie gauche curseur
        self.screen_text = self.wrap(
            self.left,
            origin=self.cursor_rect.topleft
        )

        # Nouvelles coordonnées curseur
        if self.screen_text:
            self.cursor_rect.topleft = self.screen_text[-1][1].topright

        # wrap partie droite curseur
        self.screen_text += self.wrap(
            self.right,
            origin=self.cursor_rect.topleft
        )

        # Clignotement de curseur
        self.time.tick()
        self.reste += self.time.get_time()
        if self.reste > self.interval:
            self.reste %= self.interval
            self.visible = not self.visible

        # ajout du curseur dans les éléments du texte
        if self.visible:
            self.screen_text.append((self.cursor, self.cursor_rect))
