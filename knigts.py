from pieces import Piece
import pygame as pg
import os


class Knight(Piece):
    def __init__(self, color, pos):
        self.name = 'knight'
        super(Knight, self).__init__(color, pos)
        self.image = pg.image.load(os.path.join(self.img_folder, f'{self.color}k.png'))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.image.set_colorkey((250, 250, 250))
