from abc import abstractmethod
from abc import ABC


"""
************************************************************************
::--------------------------------------------------------------------::
::--------|There is a file with interface of testing module|----------::
::--------------------------------------------------------------------::
************************************************************************
"""


class TestFigureProperty(ABC):
    """
    There is an interface of testing
    module
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def test_figure_property(self):
        """
        Test figure_property() function
        //--------------------------//
        :return:None
        """
        pass

    @abstractmethod
    def test_white(self):
        """
        Test property of white figures
        //--------------------------//
        :return: None
        """
        pass

    @abstractmethod
    def test_black(self):
        """
        Test property of black figures
        //--------------------------//
        :return: None
        """
        pass
