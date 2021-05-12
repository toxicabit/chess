"""

There is a GrandMaster chess engine

"""

import bitarray as bt


from constants import *
from rays import NORTH_RAYS
from rays import SOUTH_RAYS
from rays import WEST_RAYS
from rays import EAST_RAYS
from rays import NORTH_WEST_RAYS
from rays import NORTH_EAST_RAYS
from rays import SOUTH_WEST_RAYS
from rays import SOUTH_EAST_RAYS


class Grandmaster:

    def __init__(self):

        self.__player = {'pawns': bt.bitarray('0' * 48 + '1' * 8 + '0' * 8),
                         'rook': bt.bitarray('0' * 56 + '1' + '0' * 6 + '1'),
                         'knight': bt.bitarray('0' * 57 + '1' + '0' * 4 + '1' + '0'),
                         'bishop': bt.bitarray('0' * 58 + '1' + '0' * 2 + '1' + '0' * 2),
                         'queen': bt.bitarray('0' * 59 + '1' + '0' * 4),
                         'king': bt.bitarray('0' * 60 + '1' + '0' * 3)}
        self.__computer = {'pawns': bt.bitarray('0' * 8 + '1' * 8 + '0' * 48),
                           'rook': bt.bitarray('1' + '0' * 6 + '1' + '0' * 56),
                           'knight': bt.bitarray('0' + '1' + '0' * 4 + '1' + '0' * 57),
                           'bishop': bt.bitarray('0' * 2 + '1' + '0' * 2 + '1' + '0' * 58),
                           'queen': bt.bitarray('0' * 3 + '1' + '0' * 60),
                           'king': bt.bitarray('0' * 4 + '1' + '0' * 59)}

    # occupied area counters
    # ******************************************************************************************************************

    def __count_players_occupied_area(self):
        """
        This function calculates areas occupied
        by player's figures

        :return: bitboard of occupied area
        """
        occupied = NULL.copy()

        for i in self.__player.values():
            occupied |= i

        return occupied

    def __count_computer_occupied_area(self):
        """
        This function calculates areas occupied
        by player's figures

        :return: bitboard of occupied area
        """

        occupied = NULL.copy()

        for i in self.__computer.values():
            occupied |= i

        return occupied

    def __count_occupied_area(self):
        """
        This function counts which zones are
        free and which zones are occupied

        :return:
        """

        player = self.__count_players_occupied_area()
        computer = self.__count_computer_occupied_area()

        return player | computer

    # msn / lsn
    # ******************************************************************************************************************

    @staticmethod
    def most_significant_pos(bitboard):
        """
        This function finds number of board pos
        of most significant bit in bitboard

        :param bitboard: bitarray
        :return: number of board pos
        """

        pos = len(bitboard)

        if True in bitboard:
            pos = bitboard.index(True)

        return TOP_RIGHT - pos

    @staticmethod
    def less_significant_pos(bitboard):
        """
        This function finds number of board pos
        of less significant bit in bitboard

        :param bitboard: bitarray
        :return: number of board pos
        """

        pos = len(bitboard)

        board = bitboard.copy()
        board.reverse()

        if True in board:
            ind = board.index(True)
            pos = len(board) - 1 - ind

        return TOP_RIGHT - pos

    # choice
    # ******************************************************************************************************************

    def __choose_bitboard(self, side, figure_type):

        bitboard = NULL.copy()

        if side == PLAYER:
            bitboard = self.__player[figure_type].copy()

        elif side == COMPUTER:
            bitboard = self.__computer[figure_type].copy()

        return bitboard

    def __choose_enemy(self, side):

        enemy = NULL.copy()

        if side == PLAYER:
            enemy = self.__count_computer_occupied_area()

        elif side == COMPUTER:
            enemy = self.__count_players_occupied_area()

        return enemy

    # pawn moves section
    # ******************************************************************************************************************

    def __count_pawn_push(self, side, pawn_bitboard):

        occupied = self.__count_occupied_area()
        single = NULL.copy()
        double = NULL.copy()

        if side == PLAYER:
            single = pawn_bitboard << 8
            double = (pawn_bitboard & RANKS[1]) << 16

        elif side == COMPUTER:
            single = pawn_bitboard >> 8
            double = (pawn_bitboard & RANKS[6]) >> 16

        return (single | double) & ~occupied

    def __count_pawn_single_attack(self, side, pawn_bitboard):

        enemy = NULL.copy()
        west = NULL.copy()
        east = NULL.copy()

        if side == PLAYER:
            enemy = self.__count_computer_occupied_area()
            west = (pawn_bitboard << 7) & ~SECTORS[7]
            east = (pawn_bitboard << 9) & ~SECTORS[0]

        elif side == COMPUTER:
            enemy = self.__count_players_occupied_area()
            west = (pawn_bitboard >> 9) & ~SECTORS[7]
            east = (pawn_bitboard >> 7) & ~SECTORS[0]

        return (west | east) & enemy

    def __count_pawn_multi_attack(self, side):

        pawn_bitboard = self.__choose_bitboard(side, PAWN)

        pawn_attacks = self.__count_pawn_single_attack(side, pawn_bitboard)

        return pawn_attacks

    # knight moves section
    # ******************************************************************************************************************

    @staticmethod
    def __count_knight_rose(knight_bitboard):

        knight = knight_bitboard

        not_a_b = ~SECTORS[0] & ~SECTORS[1]
        not_g_h = ~SECTORS[6] & ~SECTORS[7]

        nne = (knight << 17) & ~SECTORS[0]
        nee = (knight << 10) & not_a_b
        see = (knight >> 6) & not_a_b
        sse = (knight >> 15) & ~SECTORS[0]
        nnw = (knight << 15) & ~SECTORS[7]
        nww = (knight << 6) & not_g_h
        sww = (knight >> 10) & not_g_h
        ssw = (knight >> 17) & ~SECTORS[7]

        rose = nne | nee | see | sse | nnw | nww | sww | ssw

        return rose

    def __count_knight_push(self, knight_bitboard):

        rose = self.__count_knight_rose(knight_bitboard)
        occupied = self.__count_occupied_area()

        return rose & ~occupied

    def __count_knight_single_attack(self, side, knight_bitboard):

        rose = self.__count_knight_rose(knight_bitboard)
        enemy = self.__choose_enemy(side)

        return rose & enemy

    def __count_knight_multi_attack(self, side):

        knight_bitboard = self.__choose_bitboard(side, KNIGHT)

        knight_attacks = self.__count_knight_single_attack(side, knight_bitboard)

        return knight_attacks

    # rose calculator
    # ******************************************************************************************************************

    def __count_rose(self, figure_pos, less_cut, most_cut):

        occupied = self.__count_occupied_area()

        rose = NULL.copy()

        for l_ray in less_cut:
            ray = l_ray[figure_pos].copy()
            block = ray & occupied

            if block != NULL:
                block_pos = self.less_significant_pos(block)
                block_ray = l_ray[block_pos].copy()
                ray &= ~block_ray

            rose |= ray

        for m_ray in most_cut:
            ray = m_ray[figure_pos].copy()
            block = ray & occupied

            if block != NULL:
                block_pos = self.most_significant_pos(block)
                block_ray = m_ray[block_pos].copy()
                ray &= ~block_ray

            rose |= ray

        return rose

    # sliding figures move sections
    # ******************************************************************************************************************

    @staticmethod
    def __count_sliding_rays(figure_type):

        less_cut, most_cut = [], []

        if figure_type == BISHOP:
            less_cut = [NORTH_WEST_RAYS, NORTH_EAST_RAYS]
            most_cut = [SOUTH_WEST_RAYS, SOUTH_EAST_RAYS]

        elif figure_type == ROOK:
            less_cut = [NORTH_RAYS, WEST_RAYS]
            most_cut = [SOUTH_RAYS, EAST_RAYS]

        elif figure_type == QUEEN:
            less_cut = [NORTH_WEST_RAYS, NORTH_EAST_RAYS, NORTH_RAYS, WEST_RAYS]
            most_cut = [SOUTH_WEST_RAYS, SOUTH_EAST_RAYS, SOUTH_RAYS, EAST_RAYS]

        return less_cut, most_cut

    def __count_sliding_push(self, figure_type, figure_pos):

        less_cut, most_cut = self.__count_sliding_rays(figure_type)

        rose = self.__count_rose(figure_pos, less_cut, most_cut)
        occupied = self.__count_occupied_area()

        return rose & ~occupied

    def __count_sliding_single_attack(self, side, figure_type, figure_pos):

        less_cut, most_cut = self.__count_sliding_rays(figure_type)
        rose = self.__count_rose(figure_pos, less_cut, most_cut)
        enemy = self.__choose_enemy(side)

        return rose & enemy

    def __count_sliding_multi_attack(self, side, figure_type):

        figures = self.__choose_bitboard(side, figure_type)

        first_pos = self.most_significant_pos(figures)
        second_pos = self.less_significant_pos(figures)
        first_attack = NULL.copy()
        second_attack = NULL.copy()

        if first_pos <= TOP_RIGHT:
            first_attack = self.__count_sliding_single_attack(PLAYER, figure_type, first_pos)

        if second_pos <= TOP_RIGHT:
            second_attack = self.__count_sliding_single_attack(PLAYER, figure_type, second_pos)

        return first_attack | second_attack

    # king moves section
    # ******************************************************************************************************************

    def __count_taboo_area(self, side):

        taboo = NULL.copy()
        opposite_side = COMPUTER

        if side == COMPUTER:
            opposite_side = PLAYER

        pawns = self.__count_pawn_multi_attack(opposite_side)
        knight = self.__count_knight_multi_attack(opposite_side)
        rook = self.__count_sliding_multi_attack(opposite_side, ROOK)
        bishop = self.__count_sliding_multi_attack(opposite_side, BISHOP)
        queen = self.__count_sliding_multi_attack(opposite_side, QUEEN)

        taboo |= pawns | knight | rook | bishop | queen
            
        return taboo

    def __count_king_rose(self, side):

        taboo = self.__count_taboo_area(side)
        king = self.__choose_bitboard(side, KING)

        n = king << 8
        s = king >> 8
        w = (king >> 1) & ~SECTORS[7]
        e = (king << 1) & ~SECTORS[0]
        nw = (king << 7) & ~SECTORS[7]
        ne = (king << 9) & ~SECTORS[0]
        sw = (king >> 9) & ~SECTORS[7]
        se = (king >> 7) & ~SECTORS[0]

        pushes = n | s | w | e | nw | ne | sw | se

        return pushes & ~taboo

    def __count_king_push(self, side):

        occupied = self.__count_occupied_area()
        rose = self.__count_king_rose(side)

        return rose & ~occupied

    def __count_king_attack(self, side):

        enemy = self.__choose_enemy(side)
        rose = self.__count_king_rose(side)

        return rose & enemy

    # move
    # ******************************************************************************************************************

    def __count_possible_pushes(self, side, figure_type, from_bitboard=NULL.copy(), from_pos=BOTTOM_LEFT):

        pushes = NULL.copy()

        if figure_type == PAWN:
            pushes = self.__count_pawn_push(side, from_bitboard)

        elif figure_type == KNIGHT:
            pushes = self.__count_knight_push(from_bitboard)

        elif figure_type == BISHOP:
            pushes = self.__count_sliding_push(BISHOP, from_pos)

        elif figure_type == ROOK:
            pushes = self.__count_sliding_push(ROOK, from_pos)

        elif figure_type == QUEEN:
            pushes = self.__count_sliding_push(QUEEN, from_pos)

        elif figure_type == KING:
            pushes = self.__count_king_push(side)

        return pushes

    def __count_possible_attacks(self, side, figure_type, from_bitboard=NULL.copy(), from_pos=BOTTOM_LEFT):

        attacks = NULL.copy()

        if figure_type == PAWN:
            attacks = self.__count_pawn_single_attack(side, from_bitboard)

        elif figure_type == KNIGHT:
            attacks = self.__count_knight_single_attack(side, from_bitboard)

        elif figure_type == BISHOP:
            attacks = self.__count_sliding_single_attack(side, BISHOP, from_pos)

        elif figure_type == ROOK:
            attacks = self.__count_sliding_single_attack(side, ROOK, from_pos)

        elif figure_type == QUEEN:
            attacks = self.__count_sliding_single_attack(side, QUEEN, from_pos)

        elif figure_type == KING:
            attacks = self.__count_king_attack(side)

        return attacks

    def __make_move(self, side, figure_type, from_bitboard, to_bitboard):

        move = from_bitboard | to_bitboard

        if side == PLAYER:
            self.__player[figure_type] ^= move

        elif side == COMPUTER:
            self.__computer[figure_type] ^= move

        return

    def __make_attack(self, side, figure_type, from_bitboard, to_bitboard):

        self.__make_move(side, figure_type, from_bitboard, to_bitboard)

        if side == PLAYER:
            for key, value in self.__computer.items():
                if (to_bitboard & value) != NULL:
                    self.__computer[key] ^= to_bitboard
                    break

        elif side == COMPUTER:
            for key, value in self.__player.items():
                if (to_bitboard & value) != NULL:
                    self.__player[key] ^= to_bitboard
                    break

        return

    def player_move(self, figure_type, f_pos, t_pos):

        from_bit = self.convert_to_bitboard(f_pos)
        to_bit = self.convert_to_bitboard(t_pos)

        if (from_bit & self.__player[figure_type]) == NULL:
            return FAIL

        possible_pushes = self.__count_possible_pushes(PLAYER, figure_type, from_bit, f_pos)
        possible_attacks = self.__count_possible_attacks(PLAYER, figure_type, from_bit, f_pos)

        if (to_bit & possible_pushes) != NULL:
            self.__make_move(PLAYER, figure_type, from_bit, to_bit)

        elif(to_bit & possible_attacks) != NULL:
            self.__make_attack(PLAYER, figure_type, from_bit, to_bit)

        else:
            return FAIL

        return [self.__player.copy(), self.__computer.copy()]

    def get_board(self):

        board = self.__count_occupied_area()

        return board

    @staticmethod
    def convert_to_bitboard(board_pos):
        """
        This function converts board position,
        which is represented by number from 0 to 63,
        from number to bitarray

        :param board_pos: number from 0 to 63
        :return: bitarray for given position
        """
        try:
            if board_pos < BOTTOM_LEFT or board_pos > TOP_RIGHT:
                raise ValueError

            bit_pos = bt.bitarray('0' * (TOP_RIGHT - board_pos) + '1' + '0' * board_pos)

            return bit_pos

        except ValueError:
            print('ERROR: ' + str(board_pos) + ' is invalid position')
            print('INCORRECT:' + str(BOTTOM_LEFT) + ' <= ' + str(board_pos) + ' <= ' + str(TOP_RIGHT))

            return NULL.copy()
