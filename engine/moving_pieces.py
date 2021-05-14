import pygame as pg
import os
import numpy as np

pg.init()


class Pieces(pg.sprite.Sprite):
    def __init__(self, image, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.image.set_colorkey((250, 250, 250))

    def update(self, coord):
        if self.rect.collidepoint(coord):
            print("Второй клик")
            pos = pg.mouse.get_pos()
            print(get_coord(pos))
            self.rect.center = get_coord(pos)

# class Pawn_W(Pieces):
#     def __init__(self, image, pos):
#         super(Pawn_W, self).__init__(image, pos)

    # def update(self, coord):
    #     if self.rect.collidepoint(coord):
    #         print("Второй клик")
    #         pos = pg.mouse.get_pos()
    #         print(get_coord(pos))
    #         self.rect.center = get_coord(pos)



# class King_W(Pieces):
#     def __init__(self, image, pos):
#         super(Pawn_W, self).__init__(image, pos)
#
# class Queen_W(Pieces):
#     def __init__(self, image, pos):
#         super(Pawn_W, self).__init__(image, pos)
#
# class Knight_W(Pieces):
#     def __init__(self, image, pos):
#         super(Pawn_W, self).__init__(image, pos)
#
# class Bishop_W(Pieces):
#     def __init__(self, image, pos):
#         super(Pawn_W, self).__init__(image, pos)
#
# class Rook_W(Pieces):
#     def __init__(self, image, pos):
#         super(Pawn_W, self).__init__(image, pos)
# class Pieces(pg.sprite.Sprite):
#     def __init__(self):
#         pg.sprite.Sprite.__init__(self)
#         self.image = pawn_w
#         self.rect = self.image.get_rect()
#         self.rect.bottomleft = ((0, HEIGHT))
#         self.image.set_colorkey((255, 0, 0))
#
#     def update(self):
#         motion = 5
#         self.rect.x += motion
#         self.rect.y -= motion
#         if self.rect.right > WIDTH or self.rect.left < 0:
#             self.rect.x = 400

def get_coord(pos):
    return (pos[0] // 100 * 100 + 50, pos[1] // 100 * 100 + 50)

# def motion():
#     if event.type == pg.MOUSEBUTTONDOWN:
#         where = get_coord(event.pos)


WIDTH = 800
HEIGHT = 800
FPS = 10
struct = np.arange(64)
struct = struct.reshape(8, 8)


game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

board = pg.image.load(os.path.join(img_folder, 'board_1.png'))
board_rect = board.get_rect()
pawn_w = pg.image.load(os.path.join(img_folder, 'wp.png'))
pawn_b = pg.image.load(os.path.join(img_folder, 'bp.png'))
rook_w = pg.image.load(os.path.join(img_folder, 'wr.png'))
rook_b = pg.image.load(os.path.join(img_folder, 'br.png'))
knight_w = pg.image.load(os.path.join(img_folder, 'wk.png'))
knight_b = pg.image.load(os.path.join(img_folder, 'bk.png'))
bishop_w = pg.image.load(os.path.join(img_folder, 'wb.png'))
bishop_b = pg.image.load(os.path.join(img_folder, 'bb.png'))
queen_w = pg.image.load(os.path.join(img_folder, 'wq.png'))
queen_b = pg.image.load(os.path.join(img_folder, 'bq.png'))
king_w = pg.image.load(os.path.join(img_folder, 'w.png'))
king_b = pg.image.load(os.path.join(img_folder, 'b.png'))

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('CHESS')
clock = pg.time.Clock()
all_sprites = pg.sprite.Group()
white_pawns = pg.sprite.Group()
black_pawns = pg.sprite.Group()


for i in range(8):
    pawns_w = Pieces(pawn_w, (50 + 100 * i, 650))
    all_sprites.add(pawns_w)
    white_pawns.add(pawns_w)
for i in range(8):
    pawns_b = Pieces(pawn_b, (50 + 100 * i, 150))
    all_sprites.add(pawns_b)
    black_pawns.add(pawns_b)
for i in range(2):
    bishops_w = Pieces(bishop_w, (400 + ((-1)**i)*150, 750))
    all_sprites.add(bishops_w)
for i in range(2):
    bishops_b = Pieces(bishop_b, (400 + ((-1)**i)*150, 50))
    all_sprites.add(bishops_b)
for i in range(2):
    knights_w = Pieces(knight_w, (400 +((-1)**i)*250, 750))
    all_sprites.add(knights_w)
for i in range(2):
    knights_b = Pieces(knight_b, (400 +((-1)**i)*250, 50))
    all_sprites.add(knights_b)
for i in range(2):
    rooks_w = Pieces(rook_w, (400 +((-1)**i)*350, 750))
    all_sprites.add(rooks_w)
for i in range(2):
    rooks_b = Pieces(rook_b, (400 +((-1)**i)*350, 50))
    all_sprites.add(rooks_b)
queens_w = Pieces(queen_w, (350, 750))
all_sprites.add(queens_w)
queens_b = Pieces(queen_b, (350, 50))
all_sprites.add(queens_b)
kings_w = Pieces(king_w, (450, 750))
all_sprites.add(kings_w)
kings_b = Pieces(king_b, (450, 50))
all_sprites.add(kings_b)

running = True

flag = False

while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if flag == True:
                all_sprites.update(get_coord(coord))
                flag = False
            else:
                print("Первый клик")
                coord = pg.mouse.get_pos()
                flag = True
    screen.fill((255, 255, 255))
    screen.blit(board, board_rect)
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()

