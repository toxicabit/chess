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

        self.__player1 = {'pawn': bt.bitarray('0' * 48 + '1' * 8 + '0' * 8),
                          'rook': bt.bitarray('0' * 56 + '1' + '0' * 6 + '1'),
                          'knight': bt.bitarray('0' * 57 + '1' + '0' * 4 + '1' + '0'),
                          'bishop': bt.bitarray('0' * 58 + '1' + '0' * 2 + '1' + '0' * 2),
                          'queen': bt.bitarray('0' * 60 + '1' + '0' * 3),
                          'king': bt.bitarray('0' * 59 + '1' + '0' * 4)}
        self.__player2 = {'pawn': bt.bitarray('0' * 8 + '1' * 8 + '0' * 48),
                          'rook': bt.bitarray('1' + '0' * 6 + '1' + '0' * 56),
                          'knight': bt.bitarray('0' + '1' + '0' * 4 + '1' + '0' * 57),
                          'bishop': bt.bitarray('0' * 2 + '1' + '0' * 2 + '1' + '0' * 58),
                          'queen': bt.bitarray('0' * 4 + '1' + '0' * 59),
                          'king': bt.bitarray('0' * 3 + '1' + '0' * 60)}
        self.__previous = PLAYER2

    # choice
    # ******************************************************************************************************************

    def __choose_bitboard(self, side, figure_type):

        bitboard = NULL.copy()

        if side == PLAYER1:
            bitboard = self.__player1[figure_type].copy()

        elif side == PLAYER2:
            bitboard = self.__player2[figure_type].copy()

        return bitboard

    def __choose_enemy(self, side):

        enemy = NULL.copy()

        if side == PLAYER1:
            enemy = self.__count_player2_occupied_area()

        elif side == PLAYER2:
            enemy = self.__count_player1_occupied_area()

        return enemy

    # converter
    # ******************************************************************************************************************

    @staticmethod
    def __convert_to_bitboard(board_pos):
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

    # msp / lsp
    # ******************************************************************************************************************

    @staticmethod
    def __most_significant_pos(bitboard):
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
    def __less_significant_pos(bitboard):
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

    # occupied area counters
    # ******************************************************************************************************************

    def __count_player1_occupied_area(self):
        """
        This function calculates areas occupied
        by player's figures

        :return: bitboard of occupied area
        """
        occupied = NULL.copy()

        for i in self.__player1.values():
            occupied |= i

        return occupied

    def __count_player2_occupied_area(self):
        """
        This function calculates areas occupied
        by player's figures

        :return: bitboard of occupied area
        """

        occupied = NULL.copy()

        for i in self.__player2.values():
            occupied |= i

        return occupied

    def __count_occupied_area(self):
        """
        This function counts which zones are
        free and which zones are occupied

        :return:
        """

        player = self.__count_player1_occupied_area()
        computer = self.__count_player2_occupied_area()

        return player | computer

    # pawn moves section
    # ******************************************************************************************************************

    @staticmethod
    def __count_pawn_single_defend(side, pawn_bitboard):

        west = NULL.copy()
        east = NULL.copy()

        if side == PLAYER1:
            west = (pawn_bitboard << 7) & ~SECTORS[7]
            east = (pawn_bitboard << 9) & ~SECTORS[0]

        elif side == PLAYER2:
            west = (pawn_bitboard >> 9) & ~SECTORS[7]
            east = (pawn_bitboard >> 7) & ~SECTORS[0]

        return west | east

    def __count_pawn_multi_defend(self, side):

        pawn_bitboard = self.__choose_bitboard(side, PAWN)
        pawn_defends = self.__count_pawn_single_defend(side, pawn_bitboard)

        return pawn_defends

    def __count_pawn_push(self, side, pawn_bitboard):

        occupied = self.__count_occupied_area()
        single = NULL.copy()
        double = NULL.copy()

        if side == PLAYER1:
            single = pawn_bitboard << 8
            double = (pawn_bitboard & RANKS[1]) << 16

        elif side == PLAYER2:
            single = pawn_bitboard >> 8
            double = (pawn_bitboard & RANKS[6]) >> 16

        return (single | double) & ~occupied

    def __count_pawn_single_attack(self, side, pawn_bitboard):

        enemy = self.__choose_enemy(side)
        defend = self.__count_pawn_single_defend(side, pawn_bitboard)

        return defend & enemy

    def __count_pawn_multi_attack(self, side):

        pawn_bitboard = self.__choose_bitboard(side, PAWN)
        pawn_attacks = self.__count_pawn_single_attack(side, pawn_bitboard)

        return pawn_attacks

    # knight moves section
    # ******************************************************************************************************************

    @staticmethod
    def __count_knight_defend(knight_bitboard):

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

        defend = nne | nee | see | sse | nnw | nww | sww | ssw

        return defend

    def __count_knight_push(self, knight_bitboard):

        defend = self.__count_knight_defend(knight_bitboard)
        occupied = self.__count_occupied_area()

        return defend & ~occupied

    def __count_knight_single_attack(self, side, knight_bitboard):

        defend = self.__count_knight_defend(knight_bitboard)
        enemy = self.__choose_enemy(side)

        return defend & enemy

    def __count_knight_multi_attack(self, side):

        knight_bitboard = self.__choose_bitboard(side, KNIGHT)

        knight_attacks = self.__count_knight_single_attack(side, knight_bitboard)

        return knight_attacks

    # sliding figures move sections
    # ******************************************************************************************************************

    def __count_rose(self, figure_type, figure_pos):

        occupied = self.__count_occupied_area()
        less_cut, most_cut = self.__count_sliding_rays(figure_type)
        rose = NULL.copy()

        for l_ray in less_cut:
            ray = l_ray[figure_pos].copy()
            block = ray & occupied

            if block != NULL:
                block_pos = self.__less_significant_pos(block)
                block_ray = l_ray[block_pos].copy()
                ray &= ~block_ray

            rose |= ray

        for m_ray in most_cut:
            ray = m_ray[figure_pos].copy()
            block = ray & occupied

            if block != NULL:
                block_pos = self.__most_significant_pos(block)
                block_ray = m_ray[block_pos].copy()
                ray &= ~block_ray

            rose |= ray

        return rose

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

    def __count_sliding_multi_defend(self, side, figure_type):

        figures = self.__choose_bitboard(side, figure_type)

        first_pos = self.__most_significant_pos(figures)
        second_pos = self.__less_significant_pos(figures)
        first_defend = NULL.copy()
        second_defend = NULL.copy()

        if first_pos <= TOP_RIGHT:
            first_defend = self.__count_rose(figure_type, first_pos)

        if second_pos <= TOP_RIGHT:
            second_defend = self.__count_rose(figure_type, second_pos)

        return first_defend | second_defend

    def __count_sliding_push(self, figure_type, figure_pos):

        rose = self.__count_rose(figure_type, figure_pos)
        occupied = self.__count_occupied_area()

        return rose & ~occupied

    def __count_sliding_single_attack(self, side, figure_type, figure_pos):

        rose = self.__count_rose(figure_type, figure_pos)
        enemy = self.__choose_enemy(side)

        return rose & enemy

    def __count_sliding_multi_attack(self, side, figure_type):

        enemy = self.__choose_enemy(side)
        defend = self.__count_sliding_multi_defend(side, figure_type)

        return defend & enemy

    # king moves section
    # ******************************************************************************************************************

    def __count_taboo_area(self, side):

        taboo = NULL.copy()
        opposite_side = PLAYER2

        if side == PLAYER2:
            opposite_side = PLAYER1

        pawns = self.__count_pawn_multi_defend(opposite_side)
        knight_bitboard = self.__choose_bitboard(opposite_side, KNIGHT)
        knight = self.__count_knight_defend(knight_bitboard)
        rook = self.__count_sliding_multi_defend(opposite_side, ROOK)
        bishop = self.__count_sliding_multi_defend(opposite_side, BISHOP)
        queen = self.__count_sliding_multi_defend(opposite_side, QUEEN)

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

    def __is_king_under_attack(self, side):

        taboo = self.__count_taboo_area(side)
        king = self.__choose_bitboard(side, KING)

        if (king & taboo) != NULL.copy():
            return True

        return False

    def __king_enemy(self, side):

        enemy = self.__choose_enemy(side)
        king_bitboard = self.__choose_bitboard(side, KING)
        king_pos = self.__most_significant_pos(king_bitboard)
        attack_directions = self.__count_rose(QUEEN, king_pos)

        return enemy & attack_directions

    # move general
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

    def __count_possible_multi_move(self, side):

        pawn_bitboard = self.__choose_bitboard(side, PAWN)
        pp = self.__count_pawn_push(side, pawn_bitboard)
        pa = self.__count_pawn_multi_attack(side)
        knight_bitboard = self.__choose_bitboard(side, KNIGHT)
        kp = self.__count_knight_push(knight_bitboard)
        ka = self.__count_knight_multi_attack(side)
        bpa = self.__count_sliding_multi_defend(side, BISHOP)
        rpa = self.__count_sliding_multi_defend(side, ROOK)
        qpa = self.__count_sliding_multi_attack(side, QUEEN)
        kip = self.__count_king_push(side)
        kia = self.__count_king_attack(side)

        pushes = pp | kp | kip
        attacks = pa | ka | bpa | rpa | qpa | kia

        return pushes | attacks

    def __make_move(self, side, figure_type, from_bitboard, to_bitboard):

        move = from_bitboard | to_bitboard

        if side == PLAYER1:
            self.__player1[figure_type] ^= move

        elif side == PLAYER2:
            self.__player2[figure_type] ^= move

        return

    def __make_attack(self, side, figure_type, from_bitboard, to_bitboard):

        self.__make_move(side, figure_type, from_bitboard, to_bitboard)

        if side == PLAYER1:
            for key, value in self.__player2.items():
                if (to_bitboard & value) != NULL:
                    self.__player2[key] ^= to_bitboard
                    break

        elif side == PLAYER2:
            for key, value in self.__player1.items():
                if (to_bitboard & value) != NULL:
                    self.__player1[key] ^= to_bitboard
                    break

        return

    # warning situations
    # ******************************************************************************************************************

    def __is_checkmate(self, side):

        king_attacked = self.__is_king_under_attack(side)
        king_pushes = self.__count_king_push(side)
        king_attacks = self.__count_king_attack(side)
        king_enemy = self.__king_enemy(side)
        others_moves = self.__count_possible_multi_move(side)

        no_moves = (king_pushes & king_attacks) == NULL
        many_enemies = (king_enemy.count(True)) > 1
        nobody_save = (king_enemy & others_moves) == NULL

        conditions = king_attacked and no_moves and (many_enemies or nobody_save)

        if conditions:
            return True

        return False

    def __is_check(self, side):

        king_attacked = self.__is_king_under_attack(side)
        checkmate = self.__is_checkmate(side)

        if king_attacked and not checkmate:
            return True

        return False

    # public methods
    # ******************************************************************************************************************

    def is_empty(self, side, fig_pos):

        fig_bit = self.__convert_to_bitboard(fig_pos)
        figures = self.__count_player1_occupied_area()

        if side == PLAYER2:
            figures = self.__count_player2_occupied_area()

        if (fig_bit & figures) == NULL:
            return True

        return False

    def is_game_over(self):

        checkmate1 = self.__is_checkmate(PLAYER1)
        checkmate2 = self.__is_checkmate(PLAYER2)

        return checkmate1 or checkmate2

    def get_board(self):

        board = self.__count_occupied_area()

        return board

    def player_move(self, side, figure_type, f_pos, t_pos):

        checkmate = self.__is_checkmate(side)

        if checkmate:
            return FAIL

        check = self.__is_check(side)

        if check:
            king_bitboard = self.__choose_bitboard(side, KING)
            king_pos = self.__most_significant_pos(king_bitboard)
            enemy_bitboard = self.__king_enemy(side)
            enemy_pos = self.__most_significant_pos(enemy_bitboard)
            king_rose = self.__count_rose(QUEEN, king_pos)
            enemy_rose = self.__count_rose(QUEEN, enemy_pos)

            required = king_rose & enemy_rose & enemy_bitboard

            from_bit = self.__convert_to_bitboard(f_pos)
            to_bit = self.__convert_to_bitboard(t_pos)

            possible_pushes = self.__count_possible_pushes(side, figure_type, from_bit, f_pos)
            possible_attacks = self.__count_possible_attacks(side, figure_type, from_bit, f_pos)

            if (to_bit & possible_pushes & required) == NULL:
                return FAIL

            elif (to_bit & possible_attacks & required) == NULL:
                return FAIL

            return SUCCESS

        if side == self.__previous:
            return FAIL

        from_bit = self.__convert_to_bitboard(f_pos)
        to_bit = self.__convert_to_bitboard(t_pos)
        figures = self.__choose_bitboard(side, figure_type)

        if (from_bit & figures) == NULL:
            return FAIL

        possible_pushes = self.__count_possible_pushes(side, figure_type, from_bit, f_pos)
        possible_attacks = self.__count_possible_attacks(side, figure_type, from_bit, f_pos)

        if (to_bit & possible_pushes) != NULL:
            self.__make_move(side, figure_type, from_bit, to_bit)

        elif(to_bit & possible_attacks) != NULL:
            self.__make_attack(side, figure_type, from_bit, to_bit)

        else:
            return FAIL

        self.__previous = side

        return SUCCESS
