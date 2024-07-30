#chatgpt solution
def is_safe(board, row, col, N):
    # Check if there is a queen in the same row
    for i in range(col):
        if board[row][i] == 1:
            return False

    # Check upper diagonal on left side
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    # Check lower diagonal on left side
    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True

def solve_n_queens_util(board, col, N):
    if col >= N:
        return True  # All queens are placed successfully

    for i in range(N):
        if is_safe(board, i, col, N):
            # Place queen
            board[i][col] = 1

            # Recur to place rest of the queens
            if solve_n_queens_util(board, col + 1, N):
                return True

            # If placing queen in the current position doesn't lead to a solution,
            # then backtrack and remove the queen from the current position
            board[i][col] = 0

    return False

def solve_n_queens(N):
    # Create an empty chessboard
    board = [[0 for _ in range(N)] for _ in range(N)]

    # Call the utility function to solve N-Queens problem
    if not solve_n_queens_util(board, 0, N):
        print("Solution does not exist.")
        return

    # Print the solution
    for row in board:
        print(" ".join(map(str, row)))

# Example usage for N = 8
solve_n_queens(8)
