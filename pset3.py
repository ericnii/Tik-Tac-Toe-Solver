# (n, m, k) -> n x m board, with k in a row to win
# P1 is O
# P2 is X

def winner(board, k):
    """
    Finds the winner of the current <board> given if there is one
    """
    width = len(board[0])
    height = len(board)
    counter = 0
    count_empty = 0

    # goes through every row
    for i in range(height):
        # goes through every column
        for m in range(width):
            if board[i][m] == "":
                count_empty += 1
            else:

                current = board[i][m]

                # checks horizontally (left to right)
                if m + k <= width:
                    for j in range(k):
                        if board[i][m + j] == current:
                            counter += 1
                        else:
                            break
                    if counter == k:
                        if current == "O":
                            return "P1 wins"
                        else:
                            return "P2 wins"
                    counter = 0

                # checks vertically (top to bottom)
                if i + k <= height:
                    for j in range(k):
                        if board[i + j][m] == current:
                            counter += 1
                        else:
                            break
                    if counter == k:
                        if current == "O":
                            return "P1 wins"
                        else:
                            return "P2 wins"
                    counter = 0

                # checks diagonal (top-left to bottom-right)
                if i + k <= height and m + k <= width:
                    for j in range(k):
                        if board[i + j][m + j] == current:
                            counter += 1
                        else:
                            break
                    if counter == k:
                        if current == "O":
                            return "P1 wins"
                        else:
                            return "P2 wins"
                    counter = 0

                # checks diagonal (bottom-left to top-right)
                if i - k + 1 >= 0 and m + k <= width:
                    for j in range(k):
                        if board[i - j][m + j] == current:
                            counter += 1
                        else:
                            break
                    if counter == k:
                        if current == "O":
                            return "P1 wins"
                        else:
                            return "P2 wins"
                    counter = 0

    if count_empty != 0:
        return "not complete"  # Draw is P2 win, confirmed in office hour
    else:
        return "P2 wins"


# Global variable for boards that are already covered. This will store the
# board position and which player's turn it is.
wins = {}


def solve(board, k):
    """
    Makes all possible moves and figures out which player wins with perfect play
    """
    global wins
    width = len(board[0])
    height = len(board)
    new_board = [row.copy() for row in board]

    x_moves = 0
    o_moves = 0

    # Gets the current turn of the player
    for i in range(height):
        for j in range(width):
            if board[i][j] == 'X':
                x_moves += 1
            elif board[i][j] == 'O':
                o_moves += 1

    player = "P1"
    if o_moves > x_moves:
        player = "P2"

    # For global var wins. It converts the array representation of the board
    # into a tuple since the key of a dict must be immutable.
    current_board = (tuple(tuple(row) for row in board), player)

    piece = "O"
    opponent = "X"
    if player.lower() == "p2":
        piece = "X"
        opponent = "O"

    # Base Case 1: Check if current board is already in global wins dict
    if current_board in wins:
        return wins[current_board]

    # Base case 2, P1 or P2 has already won (has k in a row or P2 wins on draw)
    win = winner(board, k)
    if win in ["P1 wins", "P2 wins"]:
        wins[current_board] = win
        return win

    # The code below will be an exhaustive search
    # Check for immediate win
    for i in range(height):
        for m in range(width):
            if board[i][m] == "":
                new_board[i][m] = piece
                win = winner(new_board, k)
                if win.lower() == f"{player} wins".lower():
                    return solve(new_board, k)
                new_board[i][m] = ""

    other_player = "P2"
    if player.lower() == "p2":
        other_player = "P1"

    # Check for moves that block the opponent if there is no immediate win
    for i in range(height):
        for m in range(width):
            if board[i][m] == "":
                # Find potential move that blocks opponent and check recursively
                new_board[i][m] = opponent
                if winner(new_board, k) == f"{other_player} wins":
                    new_board[i][m] = piece
                    result = solve(new_board, k)
                    wins[current_board] = result
                    return result
                new_board[i][m] = ""

    # Recursively checks all possible moves
    can_win = False
    for i in range(height):
        for m in range(width):
            if board[i][m] == "":
                new_board[i][m] = piece
                result = solve(new_board, k)

                # If current player can force a win, return it
                if result == f"{player} wins":
                    can_win = True
                    new_board[i][m] = ""  # Undo move
                    break

                new_board[i][m] = ""
        if can_win:
            break

    if can_win:
        wins[current_board] = f"{player} wins"
        return f"{player} wins"
    else:
        result = f"{other_player} wins"
        wins[current_board] = result
        return result


def test_solve(n, m, k):
    """
    Solve empty (n, m, k) tic-tac-toe board
    """
    # Clear the global dict for each new game
    global wins
    wins = {}

    board = [["" for _ in range(m)] for _ in range(n)]

    result = solve(board, k)
    return result


# Test cases
if __name__ == "__main__":
    # Test (3,3,3)
    print(f"(3,3,3): {test_solve(3, 3, 3)}")

    # Test (4,4,3)
    print(f"(4,4,3): {test_solve(4, 4, 3)}")

    # Test (3,5,4)
    print(f"(3,5,4): {test_solve(3, 5, 4)}")

    # Test (4,4,4)
    print(f"(4,4,4): {test_solve(4, 4, 4)}")
