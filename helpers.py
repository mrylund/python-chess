def isWhite(val):
    if val > 0:
        return True
    else:
        return False

def isBlack(val):
    if val < 0:
        return True
    else:
        return False

def isEmpty(val):
    if val == 0:
        return True
    else:
        return False


def isKing(val):
    if abs(val) == 6:
        return True
    else:
        return False

def isQueen(val):
    if abs(val) == 5:
        return True
    else:
        return False

def isRook(val):
    if abs(val) == 4:
        return True
    else:
        return False

def isBishop(val):
    if abs(val) == 3:
        return True
    else:
        return False

def isKnight(val):
    if abs(val) == 2:
        return True
    else:
        return False

def isPawn(val):
    if abs(val) == 1:
        return True
    else:
        return False