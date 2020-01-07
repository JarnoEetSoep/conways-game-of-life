from random import randint

class Grid:
    def __init__(self, rows, cols):
        self.arr = [[0] * rows for i in range(cols)]
        self.rows = rows
        self.cols = cols
        self.generation = 0
    
    def fillRandom(self):
        newGrid = [[0] * self.rows for i in range(self.cols)]
        for i in range(len(self.arr)):
            for j in range(len(self.arr[0])):
                newGrid[i][j] = randint(0, 1)
        
        self.arr = newGrid
    
    def computeNextGen(self):
        newGrid = [[0] * self.rows for i in range(self.cols)]

        for i in range(len(self.arr)):
            for j in range(len(self.arr[0])):
                neighbors = self.sumNeighbors(i, j)
                cell = self.arr[i][j]

                # Rules
                if cell == 1 and neighbors < 2:
                    # A live cell with fewer than 2 live neighbors dies
                    newGrid[i][j] = 0
                elif cell == 1 and neighbors > 3:
                    # A live cell with more than 3 live neighbors dies
                    newGrid[i][j] = 0
                elif cell == 1 and 1 < neighbors < 4:
                    # A live cell with 2 or 3 live neighbors still lives
                    newGrid[i][j] = 1
                elif cell == 0 and neighbors == 3:
                    # A dead cell with 3 live neighbors comes to life
                    newGrid[i][j] = 1
        
        self.arr = newGrid
        self.generation += 1
    
    def sumNeighbors(self, x, y):
        sumn = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (x + i + self.cols) % self.cols
                row = (y + j + self.rows) % self.rows
                sumn += self.arr[col][row]
        
        sumn -= self.arr[x][y]
        return sumn
    
    def change(self, x, y, value):
        self.arr[x][y] = value
    
    def all(self, state, test = lambda c: True):
        newGrid = [[0] * self.rows for i in range(self.cols)]
        for i in range(len(self.arr)):
            for j in range(len(self.arr[0])):
                if test(self.arr[i][j]):
                    newGrid[i][j] = state
        
        self.arr = newGrid

    def __call__(self):
        return self.arr