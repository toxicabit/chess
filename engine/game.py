import numpy as np
from pawns import Pawn
from kings import King
from queens import Queen
from rooks import Rook
from knigts import Knight
from bishops import Bishop
import pygame as pg
from pieces import Piece
from engine import Grandmaster as gm
import os


def print_bitboard(bitboard):
    for i in range(8):
        line = bitboard[i * 8: (i + 1) * 8]
        line.reverse()
        print(line)

    print('\n')


class Game(pg.sprite.Sprite):
    def __init__(self, player):
        super(Game, self).__init__()

        self.gm = gm()

        self.player = player
        self.enemy = 'b' if player == 'w' else 'w'

        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, 'images')

        pg.init()
        self.clock = pg.time.Clock()
        self.__WIDTH = 800
        self.__HEIGHT = 800
        self.__FPS = 10
        self.display = pg.display.set_mode((self.__WIDTH, self.__HEIGHT))
        pg.display.set_caption("CHESS")

        self.board = np.array([Piece(None, (i % 8 * 50, i % 8 * 100 + 50)) for i in range(64)], dtype=object)
        self.board = self.board.reshape(8, 8)
        for i in range(8):
            self.board[i][1] = (Pawn(self.enemy, (i * 100 + 50, 150)))
        for i in range(2):
            self.board[int(3.5 + ((-1) ** i) * 1.5)][0] = (Bishop(self.enemy, (400 + ((-1) ** i) * 150, 50)))
        for i in range(2):
            self.board[int(3.5 + ((-1) ** i) * 2.5)][0] = Knight(self.enemy, (400 + ((-1) ** i) * 250, 50))
        for i in range(2):
            self.board[int(3.5 + ((-1) ** i) * 3.5)][0] = Rook(self.enemy, (400 + ((-1) ** i) * 350, 50))
        self.board[3][0] = Queen(self.enemy, (350, 50))
        self.board[4][0] = King(self.enemy, (450, 50))
        for i in range(8):
            self.board[i][6] = Pawn(self.player, (i * 100 + 50, 650))
        for i in range(2):
            self.board[int(3.5 + ((-1) ** i) * 1.5)][7] = Bishop(self.player, (400 + ((-1) ** i) * 150, 750))
        for i in range(2):
            self.board[int(3.5 + ((-1) ** i) * 2.5)][7] = Knight(self.player, (400 + ((-1) ** i) * 250, 750))
        for i in range(2):
            self.board[int(3.5 + ((-1) ** i) * 3.5)][7] = Rook(self.player, (400 + ((-1) ** i) * 350, 750))
        self.board[3][7] = Queen(self.player, (350, 750))
        self.board[4][7] = King(self.player, (450, 750))
        self.board_image = pg.image.load(os.path.join(self.img_folder, 'board_1.png'))
        self.board_rect = self.board_image.get_rect()

        self.all_sprites = pg.sprite.Group()

        for i in range(8):
            for j in range(2):
                self.all_sprites.add(self.board[i][j])
                self.all_sprites.add(self.board[i][j+6])

        self.play()

    def play(self):
        running = True
        flag = False
        coord1 = (0, 0)

        while running:
            self.clock.tick(self.__FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if flag:
                        self.update(coord1)
                        flag = False
                        running = not self.gm.is_game_over()
                    else:
                        coord1 = self.get_coord(pg.mouse.get_pos())
                        fig_pos = self.get_pos(coord1)
                        if not self.gm.is_empty(1 if self.board[self.pix_to_board(coord1)].color == self.player else -1,
                                                fig_pos):
                            flag = True
                            print(self.get_pos(coord1))

            self.display.fill((255, 255, 255))
            self.display.blit(self.board_image, self.board_rect)
            self.all_sprites.draw(self.display)
            pg.display.flip()
        self.display.blit(pg.image.load(os.path.join(self.img_folder, 'flower.jpg')), self.board_rect)
        pg.quit()

    def update(self, coord1):
        cell1 = self.pix_to_board(coord1)[0]
        cell2 = self.pix_to_board(coord1)[1]
        if self.board[cell1][cell2].rect.collidepoint(coord1):
            print(self.board[cell1][cell2].color, self.board[cell1][cell2].name)
            print((cell1, cell2))
            coord2 = self.get_coord(pg.mouse.get_pos())
            print(self.pix_to_board(coord2))
            if self.gm.player_move(1 if self.board[cell1][cell2].color == self.player else -1,
                                   self.board[cell1][cell2].name, self.get_pos(coord1), self.get_pos(coord2)):
                if self.board[self.pix_to_board(coord2)].rect.collidepoint(coord2):
                    for i in self.all_sprites:
                        if i.rect.center == self.get_coord(coord2):
                            i.kill()
                self.board[cell1][cell2].rect.center = self.get_coord(coord2)
                self.board[cell1][cell2], self.board[self.pix_to_board(coord2)[0]][self.pix_to_board(coord2)[1]] = \
                    self.board[self.pix_to_board(coord2)[0]][self.pix_to_board(coord2)[1]], self.board[cell1][cell2]

        board = self.gm.get_board()
        print_bitboard(board)

    def get_coord(self, coord):
        return coord[0] // 100 * 100 + 50, coord[1] // 100 * 100 + 50

    def pix_to_coord(self, pos):
        return int((self.get_coord(pos)[0] - 50) / 100), int((self.get_coord(pos)[1] - 50) / 100)

    def pix_to_board(self, pos):
        return (pos[0] - 50) // 100, (pos[1] - 50) // 100

    def get_pos(self, pos):
        return (pos[0] - 50) // 100 + ((750 - pos[1]) // 100) * 8


# side = input('Choose side: b or w\n')

game = Game('w')
