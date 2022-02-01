import os


class TicTacToe:
    def __init__(self):
        self.grid_content = [["     " for _ in range(3)] for _ in range(3)]
        self.moves = dict()
        self.winner = "Draw"

        count = 1
        for row in range(len(self.grid_content)):
            for col in range(len(self.grid_content[row])):
                self.moves[count] = (row, col)
                count += 1

    def gameContinue(self):
        for row in range(3):
            if list(self.grid_content[row][col] for col in range(3)) == [self.grid_content[row][0] for _ in range(3)] and "     " not in self.grid_content[row]:
                self.winner = self.grid_content[row][0]
                return False

        for col in range(3):
            if list(self.grid_content[row][col] for row in range(3)) == [self.grid_content[0][col] for _ in range(3)] and self.grid_content[0][col] != "     ":
                self.winner = self.grid_content[0][col]
                return False

        if self.grid_content[0][0] == self.grid_content[1][1] == self.grid_content[2][2] and self.grid_content[0][0] != "     ":
            self.winner = self.grid_content[0][0]
            return False

        if self.grid_content[0][2] == self.grid_content[1][1] == self.grid_content[2][0] and self.grid_content[0][2] != "     ":
            self.winner = self.grid_content[0][0]
            return False

        return any("     " in content for content in self.grid_content)

    def getMoves(self):
        print("      Possible Locations\n")

        loc_count = 1
        for row in range(len(self.grid_content)):
            print(end="  ")
            for col in range(len(self.grid_content[row])):
                if self.grid_content[row][col] == "     ":
                    if col == 0:
                        edge = "   "
                    else:
                        edge = "|  "
                    print(f"{edge}[{loc_count}]", end="  ")
                else:
                    if col == 0:
                        print(end="        ")
                    else:
                        print(end="|       ")
                loc_count += 1
            print("\n", end="  ")
            if row < len(self.grid_content) - 1:
                print("-" * 25)

    def playerTurn(self, player, move):
        if player == "X":
            piece = "  X  "
        else:
            piece = "  O  "

        if move in self.moves:
            if self.grid_content[self.moves[move][0]][self.moves[move][1]] == "     ":
                self.grid_content[self.moves[move][0]][self.moves[move][1]] = piece
                return True
        return False

    def printBoard(self):
        print("-" * 30)
        for row in self.grid_content:
            print("         |" * 3, end="\n")
            for column in row:
                print(" ", column, end="  |")
            print("\n         |", end="")
            print("         |" * 2, end="\n")
            print("-" * 30, end="\n")


if __name__ == "__main__":
    try:
        tictactoe = TicTacToe()
        turn = ""

        while turn.lower() != "x" and turn.lower() != "o":
            turn = input("Who plays first?\n[X] or [O]:\t")
            if turn.lower() != "x" and turn.lower() != "o":
                print("Invalid Key! Please enter [X] or [O]\n")

        while tictactoe.gameContinue():
            os.system("cls" if os.name == "nt" else "clear")
            tictactoe.printBoard()
            print("\n\n")

            tictactoe.getMoves()
            playerTurn = False
            while not playerTurn:
                player_move = input(f"\nEnter Location of {turn.upper()}:\t")
                if player_move.isdigit():
                    if 0 < int(player_move) < 10:
                        playerTurn = tictactoe.playerTurn(turn.upper(), int(player_move))
                        if not playerTurn:
                            print("Tile already occupied!\n")
                    else:
                        print("Invalid location!\n")
                else:
                    print("Invalid location!\n")

            if turn.upper() == "X":
                turn = "O"
            else:
                turn = "X"

        os.system("cls" if os.name == "nt" else "clear")
        tictactoe.printBoard()

        if tictactoe.winner != "Draw":
            print(f"\nGame Over! {tictactoe.winner} wins!")
        else:
            print(f"\nGame Over! Draw between X and O!")
    except KeyboardInterrupt:
        print("\nThank you for playing!")