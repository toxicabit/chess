from test_figure_property import TestFigureProperty
from pawns_pushes import *
from constants import *


class TestPawnsPush(TestFigureProperty):
    """
    Special class to test pawns pushes functions
    """

    def __init__(self):
        super().__init__()

    def test_figure_property(self, pawns, empty, color, expect):
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

    def test_black(self):
        """
        Test black pushes
        :return: None
        """

        expect = (bpawns >> 8) | (bpawns >> 16)
        expect &= ~occupied
        self.test_figure_property(bpawns, ~occupied, BLACK, expect)

        expect = (bknight >> 24) & ~occupied
        self.test_figure_property(bknight >> 16, ~occupied, BLACK, expect)

        expect = (bking >> 16) | (bking >> 24)
        expect &= ~occupied
        self.test_figure_property(bking >> 8, ~occupied, BLACK, expect)

        expect = (bbishop >> 48) & ~occupied
        self.test_figure_property(bbishop >> 40, ~occupied, BLACK, expect)

    def test_white(self):
        """
        Test white pushes
        :return: None
        """

        expect = (wpawns << 8) | (wpawns << 16)
        expect &= ~occupied
        self.test_figure_property(wpawns, ~occupied, WHITE, expect)

        expect = (wknight << 24) & ~occupied
        self.test_figure_property(wknight << 16, ~occupied, WHITE, expect)

        expect = (wking << 16) | (wking << 24)
        expect &= ~occupied
        self.test_figure_property(wking << 8, ~occupied, WHITE, expect)

        expect = (wbishop << 48) & ~occupied
        self.test_figure_property(wbishop << 40, ~occupied, WHITE, expect)
