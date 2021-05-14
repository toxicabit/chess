import os
import pygame as pg


class Piece(pg.sprite.Sprite):
    def __init__(self, color, pos):
        self.name = ''

        pg.sprite.Sprite.__init__(self)

        self.position = pos
        self.color = color

        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, 'images')
        self.image = pg.image.load(os.path.join(self.img_folder, 'wk.png'))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.image.set_colorkey((250, 250, 250))
        # self.all_sprites = pg.sprite.Group()

    # def update(self, pos):
    #     if self.rect.collidepoint(pos):
    #         print("Второй клик")
    #         pos = pg.mouse.get_pos()
    #         print(self.get_coord(pos))
    #         self.rect.center = self.get_coord(pos)
    #
    # def get_coord(self, coord):
    #     return coord[0] // 100 * 100 + 50, coord[1] // 100 * 100 + 50
    #
    # def pix_to_coord(self, pos):
    #     return (self.get_coord(pos)[0] - 50) / 100, (self.get_coord(pos)[1] - 50) / 100
