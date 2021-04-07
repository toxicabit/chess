import bitarray as bt

"""
::--------------------------------------------------------------------::
::-------------------|White figures bitboards|------------------------::
::--------------------------------------------------------------------::
"""

wpawns = bt.bitarray('0' * 48 + '1' * 8 + '0' * 8)
wrook = bt.bitarray('0' * 56 + '1' + '0' * 6 + '1')
wknight = bt.bitarray('0' * 57 + '1' + '0' * 4 + '1' + '0')
wbishop = bt.bitarray('0' * 58 + '1' + '0' * 2 + '1' + '0' * 2)
wqueen = bt.bitarray('0' * 59 + '1' + '0' * 4)
wking = bt.bitarray('0' * 60 + '1' + '0' * 3)


"""
::--------------------------------------------------------------------::
::-------------------|Black figures bitboards|------------------------::
::--------------------------------------------------------------------::
"""

bpawns = bt.bitarray('0' * 8 + '1' * 8 + '0' * 48)
brook = bt.bitarray('1' + '0' * 6 + '1' + '0' * 56)
bknight = bt.bitarray('0' + '1' + '0' * 4 + '1' + '0' * 57)
bbishop = bt.bitarray('0' * 2 + '1' + '0' * 2 + '1' + '0' * 58)
bqueen = bt.bitarray('0' * 3 + '1' + '0' * 60)
bking = bt.bitarray('0' * 4 + '1' + '0' * 59)


"""
::--------------------------------------------------------------------::
::------------------------------|Sectors|-----------------------------::
::--------------------------------------------------------------------::
"""

ASECTOR = bt.bitarray('10000000' * 8)
BSECTOR = bt.bitarray('01000000' * 8)
CSECTOR = bt.bitarray('00100000' * 8)
DSECTOR = bt.bitarray('00010000' * 8)
ESECTOR = bt.bitarray('00001000' * 8)
FSECTOR = bt.bitarray('00000100' * 8)
GSECTOR = bt.bitarray('00000010' * 8)
HSECTOR = bt.bitarray('00000001' * 8)
