from pieces import Piece
import pygame as pg
import os


class Rook(Piece):
    def __init__(self, color, pos):
        self.name = 'rook'
        super(Rook, self).__init__(color, pos)
        self.image = pg.image.load(os.path.join(self.img_folder, f'{self.color}r.png'))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.image.set_colorkey((250, 250, 250))
