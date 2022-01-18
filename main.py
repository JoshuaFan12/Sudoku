from board import Board

board = Board([[".",".","9","7","4","8",".",".","."],["7",".",".",".",".",".",".",".","."],[".","2",".","1",".","9",".",".","."],[".",".","7",".",".",".","2","4","."],[".","6","4",".","1",".","5","9","."],[".","9","8",".",".",".","3",".","."],[".",".",".","8",".","3",".","2","."],[".",".",".",".",".",".",".",".","6"],[".",".",".","2","7","5","9",".","."]])
for item in board.board:
    print(item)
print()
while board.hasNeedsUpdate():
    board.updateAll()
for i in range(9):
    for j in range(9):
        print(f'[{i+1}, {j+1}] = ', board.possibility[i][j])
print()
# for item in board.needsUpdate:
#     print(item)
# print()




for item in board.board:
    print(item)