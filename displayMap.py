def displayMap(list2d):
# 2d array - unknown 0, 1 wall, 2 open
# all unknown ░
    size = len(list2d)
    class fourpix:
        def __init__(self,topleft,topright, bottomleft, bottomright):
            self.a[0] = (topleft)
            self.a[1]  = (topright)
            self.a[2]  = (bottomleft)
            self.a[3]  = (bottomright)
        def getChar(self):
            if all(x == 0 for x in a):
                return '░'
            if all(x == 1 for x in a):
                return '█'
            if all(x == 2 for x in a):
                return ' '
            if (a[1] == a[2] == a[3] == 1):
                return '▟'
            if (a[0] == a[2] == a[3] == 1):
                return '▙'
            if (a[0] == a[1] == a[3] == 1):
                return '▜'
            if (a[0] == a[1] == a[2] == 1):
                return '▛'
            if (a[0] == a[1] == 1 and sum(a) == 2):
                return '▀'
            if (a[2] == a[3] == 1 and sum(a) == 2):
                return '▄'
            if (a[1] == a[2] == 1 and sum(a) == 2):
                return '▐'
            if (a[0] == a[3] == 1 and sum(a) == 2):
                return '▌'
            if (a[0] == 1):
                return '▘'
            if (a[1] == 1):
                return '▝'
            if (a[2] == 1):
                return '▖'
            if (a[3] == 1):
                return '▗'
    
    for (y in range(0,size,2)):
        pixString = ''
        for (x in range(0,size,2)):
            pixString = pixString + fourpix(list2d[y][x],list2d[y][x+1],list2d[y+1][x],list2d[y][x+1]).getChar()
        print(pixString)
