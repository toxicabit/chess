from pieces import Piece
import pygame as pg
import os


class Pawn(Piece):
    def __init__(self, color, pos):
        super(Pawn, self).__init__(color, pos)
        self.name = 'pawn'
        self.image = pg.image.load(os.path.join(self.img_folder, f'{self.color}p.png'))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.image.set_colorkey((250, 250, 250))
