n = 8

def available(x, y, board):
    if (0 <= x < n and 0 <= y < n and board[x][y] == -1):
        return True
    return False

def KnightsTour(n):
    board = [ [-1 for i in range(n)] for i in range(n)]

    x_move = [1,2,-1,-2,-1,-2,1,2]
    y_move = [2,1,2,1,-2,-1,-2,-1]

    pos=board[0][0]=0
    
    if(solveKT(n,board,0,0,x_move,y_move,pos)):
        for i in range(n): 
            for j in range(n): 
                print(board[i][j], end=' ') 
            print()

def solveKT(n,board,x,y,x_move,y_move,pos):
    if(pos==n**2):
        return True
            
    for i in range(0,8):
        x_next =x+ x_move[i]
        y_next =y+ y_move[i]
        if(available(x_next,y_next,board)):
            board[x_next][y_next]=pos
            if(solveKT(n,board,x_next,y_next,x_move,y_move,pos+1)):
                return True

            board[x_next][y_next]=-1
    return False

KnightsTour(n)
