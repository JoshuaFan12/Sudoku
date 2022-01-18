class Solution:
    def __init__(self):
        self.board = 0
        self.possibility = 0
        self.needsUpdate = 0
    def solveSudoku(self, board: List[List[str]]) -> None:
        self.board = board
        self.possibility = self.generatePoss()
        self.needsUpdate = self.generateNeedsUpdate()

        while self.unsolved():
            while self.hasNeedsUpdate():
                self.updateAll()





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

    def updateSquare(self, square, row, col):
        row = row - 1
        col = col - 1
        k = 0
        for i in range(row, row+3):
            for j in range(col, col+3):
                self.board[row][col] = square[k]
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
        self.needsUpdate[row-1][col-1] = False

    def remPoss(self, row, col, poss):
        self.possibility[row-1][col-1][int(poss)-1] = '.'

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
        row = self.getRow(rowNum)
        col = self.getColumn(colNum)
        square = self.getSquare(rowNum, colNum)
        # print(row)
        updated = False
        if not self.needsUpdate[rowNum-1][colNum-1]:
            return False
        for char in row:
            if char != '.':
                self.remPoss(rowNum, colNum, char)
                updated = True
        for char in col:
            if char != '.':
                self.remPoss(rowNum, colNum, char)
                updated = True
        for char in square:
            if char != '.':
                self.remPoss(rowNum, colNum, char)
                updated = True

        if self.noPoss(rowNum, colNum):

            self.toggleUpdate(rowNum, colNum)
        if updated:
            self.needsUpdate[rowNum - 1][colNum - 1] = False

    def updateAll(self):
        for i in range(1,10):
            for j in range(1,10):
                self.basicUpdate(i,j)
                self.hasUnique(i,j)

    def hasNeedsUpdate(self):
        for row in self.needsUpdate:
            for col in row:
                if col: return True

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
                    if ((sqri+i, sqrj+j) == (row-1, col-1)): continue
                    if item in myItems:
                        myItems.remove(item)
        if len(myItems) == 1:
            self.board[row-1][col-1] = myItems.pop()
            self.toggleUpdate(row, col)

    def unsolved(self):
        for item in self.bourd:
            for char in item:
                if char == '.': return True
