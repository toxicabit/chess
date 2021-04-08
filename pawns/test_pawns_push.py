from pawns_pushes import *
from constants import *


class TestPawnsPush:
    """
    Special class to test pawns pushes functions
    """

    def __init__(self):
        pass

    def __test_pawns_push(self, pawns, empty, color, expect):
        """
        Test pawns_push() function
        //------------------------------------//
        :param pawns: bitarray of pawns
        :param empty: bitarray of empty squares
        :param color: color of pawns
        :param expect: expected result
        :return:None
        """

        result = pawns_push(pawns, empty, color)

        assert result == expect, f'{result} != {expect}'

    def test_black_push(self):
        """
        Test black pushes
        :return: None
        """

        expect = (bpawns >> 8) | (bpawns >> 16)
        expect &= ~occupied
        self.__test_pawns_push(bpawns, ~occupied, BLACK, expect)

        expect = (bknight >> 24) & ~occupied
        self.__test_pawns_push(bknight >> 16, ~occupied, BLACK, expect)

        expect = (bking >> 16) | (bking >> 24)
        expect &= ~occupied
        self.__test_pawns_push(bking >> 8, ~occupied, BLACK, expect)

        expect = (bbishop >> 48) & ~occupied
        self.__test_pawns_push(bbishop >> 40, ~occupied, BLACK, expect)

    def test_white_push(self):
        """
        Test white pushes
        :return: None
        """

        expect = (wpawns << 8) | (wpawns << 16)
        expect &= ~occupied
        self.__test_pawns_push(wpawns, ~occupied, WHITE, expect)

        expect = (wknight << 24) & ~occupied
        self.__test_pawns_push(wknight << 16, ~occupied, WHITE, expect)

        expect = (wking << 16) | (wking << 24)
        expect &= ~occupied
        self.__test_pawns_push(wking << 8, ~occupied, WHITE, expect)

        expect = (wbishop << 48) & ~occupied
        self.__test_pawns_push(wbishop << 40, ~occupied, WHITE, expect)
