import os


class TicTacToe:
    def __init__(self):
        self.grid_content = [["     " for _ in range(3)] for _ in range(3)]
        self.winner = "Draw"

    def gameContinue(self):
        if self.grid_content[0][0] != "     ":
            if self.grid_content[0][0] == self.grid_content[0][1] and self.grid_content[0][0] == self.grid_content[0][2]:
                self.winner = self.grid_content[0][0]
                return False
            elif self.grid_content[0][0] == self.grid_content[1][0] and self.grid_content[0][0] == self.grid_content[2][0]:
                self.winner = self.grid_content[0][0]
                return False
            elif self.grid_content[0][0] == self.grid_content[1][1] and self.grid_content[0][0] == self.grid_content[2][2]:
                self.winner = self.grid_content[0][0]
                return False
            elif self.grid_content[0][0] == self.grid_content[1][2] and self.grid_content[0][0] == self.grid_content[2][2]:
                self.winner = self.grid_content[0][0]
                return False
        elif self.grid_content[1][0] != "     ":
            if self.grid_content[1][0] == self.grid_content[1][1] and self.grid_content[1][0] == self.grid_content[1][2]:
                self.winner = self.grid_content[0][0]
                return False
        return True

    def getMoves(self):
        possibleMoves = []
        for row in range(len(self.grid_content)):
            for col in range(len(self.grid_content[row])):
                if self.grid_content[row][col] == "     ":
                    possibleMoves.append((row, col))

        return possibleMoves

    def playerTurn(self, player, move):
        if player == "X":
            piece = "  X  "
        else:
            piece = "  O  "

        if self.grid_content[move[0]][move[1]] == "     ":
            self.grid_content[move[0]][move[1]] = piece
            return True
        return False

    def printBoard(self):
        print("-" * 40)
        for i in range(-1, 3):
            if i >= 0:
                print("   ", i + 1, " ", end="  |")
            else:
                print("         |", end="")
        print()
        print("-" * 40)
        row_ctr = 65
        for row in self.grid_content:
            print("         |" * 4, end="\n")
            print("   ", chr(row_ctr), "   |", end="")
            for column in row:
                print(" ", column, end="  |")
            print("\n         |", end="")
            print("         |" * 3, end="\n")
            print("-" * 40, end="\n")
            row_ctr += 1


tictactoe = TicTacToe()
turn = ""

while turn.lower() != "x" and turn.lower() != "o":
    turn = input("Who plays first?\t[X] or [O]:\t")
    if turn.lower() != "x" and turn.lower() != "o":
        print("Invalid Key! Please enter [X] or [O]\n")

while tictactoe.gameContinue():
    os.system("cls" if os.name == "nt" else "clear")
    tictactoe.printBoard()
    print("\n\n")

    possibleMoves = tictactoe.getMoves()
    possibleMoves.sort()
    print("[#]  LOCATION")
    for curr_piece in range(len(possibleMoves)):
        piece_formatted = chr(possibleMoves[curr_piece][0] + 65) + str(possibleMoves[curr_piece][1] + 1)
        print("[{}]    {:<2} ".format(curr_piece + 1, piece_formatted))
    print()

    playerTurn = False
    while not playerTurn:
        player_move = input(f"Enter Location of {turn.upper()}:\t")
        playerTurn = tictactoe.playerTurn(turn.upper(), possibleMoves[int(player_move) - 1])

    if turn.upper() == "X":
        turn = "O"
    else:
        turn = "X"

tictactoe.printBoard()
print(f"\nGame Over! {tictactoe.winner} wins!")