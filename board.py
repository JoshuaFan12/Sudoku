from collections import defaultdict

class Board:
    def __init__(self, board):
        self.board = board
        self.possibility = self.generatePoss()
        self.needsUpdate = self.generateNeedsUpdate()

    def getRow(self, row):
        return self.board[row-1].copy()

    def getColumn(self, column):
        return [row[column-1] for row in self.board]

    def updateRow(self, row, rowNum):
        self.board[rowNum-1] = row

    def updateColumn(self, column, columnNum):
        for i in range(len(self.board)):
            self.board[i][columnNum-1] = column[i]

    def getSquare(self, row, col):
        sqri = (row - 1) // 3 * 3
        sqrj = (col - 1) // 3 * 3
        ans = []
        for i in range(0, 3):
            for j in range(0, 3):
                ans += self.board[sqri+i][sqrj+j]
        return ans

    def getSquarePoss(self, row, col):
        sqri = (row - 1) // 3 * 3
        sqrj = (col - 1) // 3 * 3
        ans = []
        for i in range(0, 3):
            for j in range(0, 3):
                ans += self.possibility[sqri+i][sqrj+j].copy()
        return ans

    def updateSquare(self, square, row, col):
        sqri = (row - 1) // 3 * 3
        sqrj = (col - 1) // 3 * 3
        k = 0
        for i in range(3):
            for j in range(3):
                self.board[sqri+i][sqrj+j] = square[k]
                k += 1

    def updateSquarePoss(self, poss, row, col):
        sqri = (row - 1) // 3 * 3
        sqrj = (col - 1) // 3 * 3
        k = 0
        for i in range(3):
            for j in range(3):
                self.possibility[sqri+i][sqrj+j] = poss[k]
                k += 1

    def generatePoss(self):
        pos = []
        for i in range(1, 10):
            pos.append(f'{i}')
        possibilities = []
        for row in range(9):
            possRow = []
            for column in range(9):
                if self.board[row][column] == '.':
                    possRow.append(pos.copy())
                else:
                    temp = ['.']*9
                    # print(self.board[row][column])
                    temp[int(self.board[row][column]) - 1] = self.board[row][column]
                    possRow.append(temp)
            possibilities.append(possRow)
        return possibilities

    def toggleUpdate(self, row, col):
        for i in range(9):
            if self.board[row-1][i] == '.':
                self.needsUpdate[row-1][i] = True
            if self.board[i][col-1] == '.':
                self.needsUpdate[i][col-1] = True
        sqri = (row-1) // 3 * 3
        sqrj = (col-1) // 3 * 3
        for i in range(3):
            for j in range(3):
                if self.board[sqri+i][sqrj+i] == '.':
                    self.needsUpdate[sqri+i][sqrj+j] = True

    def noPoss(self, row, col):
        val = '.'
        count = 0
        if self.board[row-1][col-1] != '.':
            return False
        for char in self.possibility[row-1][col-1]:
            if char != '.':
                count += 1
                val = char
            if count > 1:
                return False
        # print(row,col)
        self.board[row-1][col-1] = val
        self.fixPoss(row, col)
        return True

    def generateNeedsUpdate(self):
        needsUpdate = []
        for row in range(9):
            updRow = []
            for column in range(9):
                if self.board[row][column] == '.':
                    updRow.append(True)
                else:
                    updRow.append(False)
            needsUpdate.append(updRow)
        return needsUpdate

    def basicUpdate(self, rowNum, colNum):
        updated = False
        if not self.needsUpdate[rowNum-1][colNum-1]:
            return False
        for char in row:
            if char != '.':
                self.remPoss(rowNum, colNum, char)
        for char in col:
            if char != '.':
                self.remPoss(rowNum, colNum, char)
        for char in square:
            if char != '.':
                self.remPoss(rowNum, colNum, char)

        if self.noPoss(rowNum, colNum):

            self.toggleUpdate(rowNum, colNum)

    def updateAll(self):
        for i in range(1,10):
            for j in range(1,10):
                if self.board[i-1][j-1] == '.':
                    self.basicUpdate(i, j)
                    self.hasUnique(i, j)
                    self.needsUpdate[i-1][j-1] = False

    def hasNeedsUpdate(self):
        for i in range(9):
            for j in range(9):
                if self.needsUpdate[i][j] and self.board[i][j] == '.': return True

    def hasUnique(self, row, col):
        myItems = set()
        if not self.needsUpdate[row-1][col-1]:
            return False
        for item in self.possibility[row-1][col-1]:
            if item != '.':
                myItems.add(item)
        for i in range(9):
            for item in self.possibility[i][col-1]:
                if i == (row-1) : continue
                if item in myItems:
                    myItems.remove(item)
            for item in self.possibility[row-1][i]:
                if i == (col-1) : continue
                if item in myItems:
                    myItems.remove(item)
        sqri = (row - 1) // 3 * 3
        sqrj = (col - 1) // 3 * 3
        for i in range(3):
            for j in range(3):
                for item in self.possibility[sqri+i][sqrj+j]:
                    if sqri+i == row-1 and sqrj+j == col-1: continue
                    if item in myItems:
                        myItems.remove(item)
        if len(myItems) == 1:
            self.board[row-1][col-1] = myItems.pop()
            self.fixPoss(row, col)
            self.toggleUpdate(row, col)

    def fixPoss(self, row, col):
        if self.board[row-1][col-1] != '.':
           for i in range(9):
               if self.possibility[row-1][col-1][i] != self.board[row-1][col-1]:
                   self.possibility[row - 1][col - 1][i] = '.'

    def checkPair(self, rowNum, colNum):
        defaulposs = ['.']*9
        row = self.getRow(rowNum)
        col = self.getColumn(colNum)
        square = self.getSquare(rowNum, colNum)
        if self.board[rowNum-1][colNum-1] != '.':
            return None
        # logic unique: in any row/column/square. if x,y, so on can only appear in 2 spots, it must appear in those two spots
        # all other possibilities should be set to empty
        pos = []
        for i in range(1, 10):
            if f'{i}' in self.board[rowNum-1][colNum-1]:
                pos.append(f'{i}')
        rdata = defaultdict(list)
        cdata = defaultdict(list)
        sdata = defaultdict(list)
        sposs = self.getSquarePoss(rowNum, colNum)
        for item in pos:
            for ind in range(9):
                if row[ind] == '.':
                    if item in self.possibility[rowNum-1][ind]:
                        rdata[item].append(ind)

                if col[ind] == '.':
                    if item in self.possibility[ind][colNum]:
                        cdata[item].append(ind)

                if square[ind] == '.':
                    if item in sposs:
                        sdata[item].append(ind)

        for key in rdata.keys():
            if len(rdata[key]) == 2:





        # logic perfect: (maybe another function). in any row/column/square if x, y, so on appear in exactly 2 spots,
        # it can only appear in those two spots. x, y, so on in other squares should be set to 0

        