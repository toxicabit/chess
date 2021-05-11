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

    # pawn moves section
    # ******************************************************************************************************************

    def __count_pawn_pushes(self, side, computer_pawn=NULL):

        occupied = self.__count_occupied_area()
        single = NULL.copy()
        double = NULL.copy()

        if side == PLAYER:
            single = self.__player['pawns'] << 8
            double = (self.__player['pawns'] & RANKS[1]) << 16

        elif side == COMPUTER:
            single = computer_pawn >> 8
            double = (computer_pawn & RANKS[6]) >> 16

        return (single | double) & ~occupied

    def __count_pawn_attacks(self, side, computer_pawn=NULL):

        enemy = NULL.copy()
        west = NULL.copy()
        east = NULL.copy()

        if side == PLAYER:
            enemy = self.__count_computer_occupied_area()
            west = (self.__player['pawns'] << 7) & ~SECTORS[7]
            east = (self.__player['pawns'] << 9) & ~SECTORS[0]

        elif side == COMPUTER:
            enemy = self.__count_players_occupied_area()
            west = (computer_pawn >> 9) & ~SECTORS[7]
            east = (computer_pawn >> 7) & ~SECTORS[0]

        return (west | east) & enemy

    # knight moves section
    # ******************************************************************************************************************

    def __count_knight_rose(self, side, computer_knight=NULL):

        knight = NULL.copy()

        not_a_b = ~SECTORS[0] & ~SECTORS[1]
        not_g_h = ~SECTORS[6] & ~SECTORS[7]

        if side == PLAYER:
            knight = self.__player['knight'].copy()

        elif side == COMPUTER:
            knight = computer_knight

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

    def __count_knight_pushes(self, side, computer_knight=NULL):

        rose = self.__count_knight_rose(side, computer_knight)
        occupied = self.__count_occupied_area()

        return rose & ~occupied

    def __count_knight_attacks(self, side, computer_knight=NULL):

        rose = self.__count_knight_rose(side, computer_knight)
        enemy = NULL.copy()

        if side == PLAYER:
            enemy = self.__count_computer_occupied_area()

        elif side == COMPUTER:
            enemy = self.__count_players_occupied_area()

        return rose & enemy

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

    def __count_single_sliding_pushes(self, figure_type, figure_pos):

        less_cut, most_cut = self.__count_sliding_rays(figure_type)

        rose = self.__count_rose(figure_pos, less_cut, most_cut)
        occupied = self.__count_occupied_area()

        return rose & ~occupied

    def __count_sliding_pushes(self, side, figure_type):

        figures = NULL.copy()

        if side == PLAYER:
            figures = self.__player[figure_type].copy()

        elif side == COMPUTER:
            figures = self.__computer[figure_type].copy()

        first_pos = self.most_significant_pos(figures)
        second_pos = self.less_significant_pos(figures)
        first_push = NULL.copy()
        second_push = NULL.copy()

        if first_pos <= TOP_RIGHT:
            first_push = self.__count_single_sliding_pushes(figure_type, first_pos)

        if second_pos <= TOP_RIGHT:
            second_push = self.__count_single_sliding_pushes(figure_type, second_pos)

        return first_push | second_push

    def __count_single_sliding_attacks(self, side, figure_type, figure_pos):

        less_cut, most_cut = self.__count_sliding_rays(figure_type)
        rose = self.__count_rose(figure_pos, less_cut, most_cut)
        enemy = NULL.copy()

        if side == PLAYER:
            enemy = self.__count_computer_occupied_area()

        elif side == COMPUTER:
            enemy = self.__count_players_occupied_area()

        return rose & enemy

    def __count_sliding_attacks(self, side, figure_type):

        figures = NULL.copy()

        if side == PLAYER:
            figures = self.__player[figure_type].copy()

        elif side == COMPUTER:
            figures = self.__computer[figure_type].copy()

        first_pos = self.most_significant_pos(figures)
        second_pos = self.less_significant_pos(figures)
        first_attack = NULL.copy()
        second_attack = NULL.copy()

        if first_pos <= TOP_RIGHT:
            first_attack = self.__count_single_sliding_attacks(PLAYER, figure_type, first_pos)

        if second_pos <= TOP_RIGHT:
            second_attack = self.__count_single_sliding_attacks(PLAYER, figure_type, second_pos)

        return first_attack | second_attack

    # king moves section
    # ******************************************************************************************************************

    def __count_taboo_area(self, side):

        taboo = NULL.copy()

        if side == PLAYER:
            pawns = self.__count_pawn_attacks(COMPUTER, self.__computer['pawns'])
            knight = self.__count_knight_attacks(COMPUTER, self.__computer['knight'])
            rook = self.__count_sliding_attacks(COMPUTER, ROOK)
            bishop = self.__count_sliding_attacks(COMPUTER, BISHOP)
            queen = self.__count_sliding_attacks(COMPUTER, QUEEN)

            taboo |= pawns | knight | rook | bishop | queen

        elif side == COMPUTER:
            pawns = self.__count_pawn_attacks(PLAYER)
            knight = self.__count_knight_attacks(PLAYER)
            rook = self.__count_sliding_attacks(PLAYER, ROOK)
            bishop = self.__count_sliding_attacks(PLAYER, BISHOP)
            queen = self.__count_sliding_attacks(PLAYER, QUEEN)

            taboo |= pawns | knight | rook | bishop | queen
            
        return taboo

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

            return NULL
