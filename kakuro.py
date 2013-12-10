
# Daniel Drucker
# Kakuro Ralley
# 01/28/2013
# github.com/danieldrucker


# If you don't know how to play, type in Kakuro on google!

# This is a game of the Japanese logic puzzle called KAKURO
# that I programmed just for fun. I saw the app on itunes,
# found it challenging so I decided to give it a try. I only
# put one board in, but hopefully someday I will put
# in more! (Or write an algorithm that does it for me.)
# I put in a couple cool features such as solve row/ column and
# show notes, which are featured in the app. Show notes
# was probably the toughest because I had to find out all logically
# possible numbers that could go in a given slot. Some of my more
# complex code can be seen at my github website.
# Check it out: github.com/danieldrucker

BOARD_SIZE = 7

ANSWERS =           [[-1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, 1, 2, -1, 1, 2],
                    [-1, 4, 6, 5, 2, 3, 1],
                    [-1, 1, 5, -1, 9, 8, 5],
                    [-1, -1, 9, 4, 8, 2, -1],
                    [-1, 1, 4, 2, 3, -1, -1],
                    [-1, 3, 2, 1, -1, -1, -1]]

HEADERS = [[(), (), (27, 0), (7, 0), (), (14, 0), (8, 0)],
           [(), (5, 3), (), (), (22, 3), (), ()],
           [(0, 21), (), (), (), (), (), ()],
           [(0, 6), (), (), (7, 22), (), (), ()],
           [(), (4, 23), (), (), (), (), ()],
           [(0, 10), (), (), (), (), (), ()],
           [(0, 6), (), (), (), (), (), ()]]

def cross(a, b):
    ret = []
    for i in a:
        for j in b:
            if isinstance(j, set):
                 if not i in j:
                     t = set([i] + list(j))
                     if not t in ret:
                         ret.append(t)
            elif not i == j and not (j, i) in ret:
                ret.append(set([i, j]))
    return ret

def getOptions(num_digits, total):
    A = range(1, 10)
    combs = A
    for i in range(num_digits - 1):
        combs = cross(A, combs)
    options = []
    for comb in combs:
        if total == sum(comb):
            for i in comb:
                if not i in options:
                    options.append(i)
    return options


class GameBoard():

    def __init__(self, answers, headers):
        self.answers = answers
        self.headers = headers
        self.board = []
        for i in range(BOARD_SIZE):
            row = []
            for j in range(BOARD_SIZE):
                if -1 == self.answers[i][j]:
                    row.append(-1)
                else:
                    row.append(0)
            self.board.append(row)
        
    def isGameWon(self):
        return (self.board == self.answers)

    def enterAnswer(self, row, col, answer):
        if not -1 == self.answers[row][col]:
            self.board[row][col] = answer

    def printBoard(self):
        for i in range(BOARD_SIZE):
            line = ""
            for j in range(BOARD_SIZE):
                if 0 == self.board[i][j] and self.headers[i][j] == ():
                    line += "     x    "
                elif self.headers[i][j]:
                    line += "    " + str(self.headers[i][j][0]) + "\\" + str(self.headers[i][j][1]) + ""
                elif not -1 == self.board[i][j]:
                    line += "     " + str(self.board[i][j])+ "    "
                else:
                    line += "          "
        
            print line
            print "\n"

    def solveRow(self, row):
        self.board[row] = self.answers[row]

    def solveCol(self, col):
        for i in range(BOARD_SIZE):
            self.board[i][col] = self.answers[i][col]

    def solution(self):
        self.board = self.answers
            
               
    def notes(self, row, col):
        c = self.headers[row][col]
        x = 1
        while  c == ():
            x += 1
            c = self.headers[row-x][col]
        col_val = c[0]
      
        r = self.headers[row][col]
        x = 1
        while  r == ():
            x += 1
            r = self.headers[row][col-x]
        row_val = r[1]

        row_digits = 0
        for i in range(BOARD_SIZE):
            if self.board[row][i] == -1 and i >= col:
                break
            elif self.board[row][i] == -1:
                row_digits = 0
            else:
                row_digits += 1

        
        col_digits = 0
        for i in range(BOARD_SIZE):
            if self.board[i][col] == -1 and i >= row:
                break
            elif self.board[i][col] == -1:
                col_digits = 0
            else:
                col_digits += 1
        notes = set.intersection(set(getOptions(row_digits, row_val)), set(getOptions(col_digits, col_val)))
        return list(notes)

class GamePlay:

    def getNumInput(self, prompt, start, end):
        val = input(prompt)
        while not isinstance(val, int) or start > val or end < val:
            print 'Invalid input.'
            val = input(prompt)
        return val

    def __init__(self, board):
        self.board = board

    def play(self):
        prompt = "\nPlease choose one of the following options:\n\t1) Enter selection\n\t2) Show notes\n\t3) Solve row\n\t4) Solve column\n\t5) Exit game\n"
        done = False
        while not done:
            self.board.printBoard()
            opt = self.getNumInput(prompt, 1, 5)
            if 1 == opt:
                row_num = self.getNumInput('Enter row number: ', 1, BOARD_SIZE)
                col_num = self.getNumInput('Enter col number: ', 1, BOARD_SIZE)
                selection = self.getNumInput('Enter selection: ', 1, 9)
                self.board.enterAnswer(row_num, col_num, selection)
            elif 2 == opt:
                row_num = self.getNumInput('Enter row number: ', 1, BOARD_SIZE)                
                col_num = self.getNumInput('Enter col number: ', 1, BOARD_SIZE)
                if self.board.headers[row_num][col_num]:
                    print 'Cell is a header, no notes.'
                else:
                    print 'Notes for cell (' + str(row_num) + ',' + str(col_num) + '): ' + str(self.board.notes(row_num, col_num))

            elif 3 == opt:
                row_num = self.getNumInput('Enter row number: ', 1, BOARD_SIZE)
                self.board.solveRow(row_num)
                print 'row ' + str(row_num) + ' solved.'
            elif 4 == opt:
                col_num = self.getNumInput('Enter col number: ', 1, BOARD_SIZE)
                self.board.solveRow(col_num)
                print 'column ' + str(col_num) + ' solved.'
            elif 5 == opt:
                print 'Goodbye!'
                done = True

            if self.board.isGameWon():
                print '\n\nVICTORY!!!'
                self.board.printBoard()
                done = True


if __name__ == "__main__":
    
    game = GamePlay(GameBoard(ANSWERS, HEADERS))
    game.play()



