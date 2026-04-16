import numpy as np
from queue import PriorityQueue
import time 
import os 

class Matrix:
    def __init__(self, name):
        self.name :str = name
        self.matrix :np.ndarray = None
    
    def print_matrix(self) -> None:
        print(f"\n{self.name} matrix: ")
        for i in range(self.height):
            for j in range(self.width):
                cell = chr(self.matrix[i][j])
                if cell == '.':
                    print(f"{' ':^3}", end = " ")
                else:
                    print(f"[{cell}]", end = " ")
            print()
        
        print()

    @property
    def width(self):
        return self.matrix.shape[1]
    
    @property
    def height(self):
        return self.matrix.shape[0]

    def __getitem__(self, idx):
        return self.matrix[idx]
    
    def __repr__(self):
        return self.name
    
    def __lt__(self, other):
        return self.name < other.name
    
class InputMatrix(Matrix):
    def __init__(self, name):
        super().__init__(name)
        self.construct_matrix()
    
    def construct_matrix(self) -> None:
        matrix = []
        idx = 1

        while True:
            inp = input(f"Input row {idx} of {self.name}'s matrix: ")
            if inp:
                matrix.append(list(map(ord, inp.split())))
            else:
                break
            idx += 1

        self.matrix = np.array(matrix)

class MatrixConstructor(Matrix):
    def __init__(self, name, width, height, target , obj :str):
        super().__init__(name)
        self.construct_matrix(width, height, target, obj)
    
    def construct_matrix(self, width, height, target, obj :str) -> None:
        matrix = []
        for row in range(height):
            curr = []
            for col in range(width):
                if target[row][col] == ord("."):
                    curr.append(ord("."))
                else:
                    curr.append(target[row][col] if obj == "Copy"\
                             else ord('-'))
            matrix.append(curr)

        self.matrix = np.array(matrix)

class Block(InputMatrix):
    def __init__(self, name):
        super().__init__(name)
    
    @property
    def rotations(self):
        caption = [" Rotated Once", " Rotated Twice", " Rotated Thrice"]
        res = [self]

        rotated = np.rot90(np.copy(self.matrix))
        for i in range(3):
            if np.array_equal(rotated, self.matrix):
                break
            res.append(BuildMatrix(self.name + caption[i], rotated.shape[1], rotated.shape[0], rotated))
            rotated = np.rot90(rotated)
        
        self.name += " Not Flipped"
        return res

class Board(MatrixConstructor):
    def __init__(self, target :Matrix):
        super().__init__("Board", target.width, target.height, target.matrix, "Construct")

class BuildMatrix(MatrixConstructor):
    def __init__(self, name, width, height, target :Matrix):
        super().__init__(name, width, height, target, "Copy")

class Game:
    combinations :dict[tuple, int] = {
        (ord("Y"), ord("B")) : ord("G"), 
        (ord("R"), ord("Y")) : ord("O"), 
        (ord("B"), ord("R")) : ord("P")
    }

    half_points :dict[int, set] = {
        ord("B") : {ord("G"), ord("P")},
        ord("Y") : {ord("G"), ord("O")},
        ord("R") : {ord("O"), ord("P")}
    }

    @staticmethod
    def create_target() -> Matrix:
        print("\nConstructing target matrix...")
        print("Abbreviations : ")
        print("Yellow : Y \nBlue : B\nRed : R\nOrange : O\nPurple : P\nGreen : G")
        obj = InputMatrix("Target")
        obj.print_matrix()
        return obj
    
    @staticmethod
    def create_board(target) -> Matrix:
        print("\nAuto constructing board matrix...")
        obj = Board(target)
        obj.print_matrix()
        return obj
    
    @staticmethod
    def create_blocks() -> list[Block]:
        print("\nConstructing blocks...")
        amount = int(input("How many blocks are available? "))
    
        print("\nabbreviations : ")
        print("Yellow : Y \nBlue : B\nRed : R\nOrange : O\nPurple : P\nGreen : G")
        blocks :list[Block] = []
        for i in range(amount):
            blocks.extend(Block(f"Block {i+1}").rotations)

        print("Blocks: ")  
        for block in blocks:
            block.print_matrix()
        
        return blocks
    
    @staticmethod
    def is_feasible(y :int, x :int, block : Block, board : Matrix) -> bool:
        for row in range(y, y + block.height):
            for col in range(x, x + block.width):
                if block[row-y][col-x] == ord("."):
                    continue
                elif row >= board.height or col >= board.width:
                    return False
                elif board[row][col] == ord("."):
                    return False
                elif board[row][col] == ord("-"):
                    continue 
                elif (board[row][col], block[row-y][col-x]) in Game.combinations\
                      or (block[row-y][col-x],board[row][col] ) in Game.combinations:
                    continue
                else:
                    return False      
        return True
    
    @staticmethod
    def put(pos_y :int, pos_x :int, block : Block, board:Matrix) -> None:
        for y in range(pos_y, pos_y + block.height):
            for x in range(pos_x, pos_x + block.width):
                if block[y-pos_y][x-pos_x] == ord("."):
                    continue
                elif board[y][x] == ord("-"):
                    board[y][x] = block[y - pos_y][x - pos_x]
                else:
                    board[y][x] = Game.combine(board[y][x], block[y - pos_y][x - pos_x])

    @staticmethod
    def offset(board : Matrix, target:Matrix):
        
        ans = 0 
        for row in range(target.height):
            for col in range(target.width):
                if board[row][col] == target[row][col]:
                    ans += 2
                elif board[row][col] in Game.half_points.get(target[row][col],[]):
                    ans += 1
        
        return (target.height * target.width * 2) - ans

    @staticmethod
    def combine(color1 :int, color2 :int) -> int:
        return Game.combinations.get((color1, color2), Game.combinations.get((color2, color1)))

class Node:
    def __init__(self, board, used, coord, target):
        self.board :Matrix = board 
        self.used :list[int] = used 
        self.coord :list[str] = coord

        self.offset =  Game.offset(self.board, target)
        self.h_value = len(self.used) + self.offset

    def __lt__(self, other):
        return self.h_value < other.h_value

class GameSolver:
    def __init__(self):
        self.game :Game = Game 
        self.target :Matrix = self.game.create_target()
        self.board :Matrix = self.game.create_board(self.target)
        self.blocks :list[Block] = self.game.create_blocks()
        self.solution()

    def animation(self, blocks, coord):
        while input("Press enter to replay the solution, and exit to quit") != "exit":
            idx = 0
            board_copy = BuildMatrix("Board Copy", self.board.width, self.board.height, self.board)
            while idx < len(blocks):
                
                os.system("cls")
                y, x = map(int, coord[idx].strip("()").split(","))
                print(f"\nStep {idx+1} : Put {self.blocks[blocks[idx]].name} to ({y+1}, {x+1})")
                self.game.put(y, x, self.blocks[blocks[idx]], board_copy)
                board_copy.print_matrix()
                idx += 1
    
                time.sleep(4)

    def solution(self):
        start = time.time()
        status, blocks, coord, trials = self.solve()
        end = time.time()
        if status == "Success":
            print(f"Solution Founded in {trials} tries in {end-start} seconds!")
            os.system("cls")
            self.animation(blocks, coord)
               
        else: 
            print(f"No solution founded, {trials} trials made in {end-start} seconds, please make sure inputs are correct")

    def solve(self) -> list[str]:
        print("Solving...\n")
        start = Node(self.board, list(), list(), self.target)
        queue = PriorityQueue()
        queue.put((start.offset, start))

        trials = 1
        while not queue.empty():
            node :Node = queue.get(0)[1]
            
            if node.offset == 0:
                return "Success", node.used, node.coord, trials

            for idx in range(len(self.blocks)):
                if idx in node.used:
                    continue 

                for y in range(self.target.height):
                    for x in range(self.target.width):
                        if self.game.is_feasible(y, x, self.blocks[idx], node.board ):
                            copy = BuildMatrix("Copy", node.board.width, node.board.height, node.board.matrix)
                            self.game.put(y, x, self.blocks[idx], copy)
                            new_node = Node(copy, node.used + [idx], node.coord + [f"({y},{x})"], self.target)
                            queue.put((new_node.offset, new_node))
            
            trials += 1
        
        return "Failled", None, None, trials

if __name__ == "__main__":
    GameSolver()              

                