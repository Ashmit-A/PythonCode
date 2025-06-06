def boolean_mat(mat):
    rows = len(mat)
    cols = len(mat[0])

    row0 = False
    col0 = False

    for i in range(rows):
        if(mat[i][0] == 1):
            col0 = True
    for j in range(cols):
        if mat[0][j] == 1:
            row0 = True
    
    for i in range(1, rows):
        for j in range(1, cols):
            if mat[i][j] == 1 :
                mat[i][0] = mat[0][j] = 1

    for i in range(1, rows):
        for j in range(1, cols):
            if mat[i][0] == 1 or mat[0][j] == 1:
                mat [i][j] = 1

    if col0:
        for i in range(rows):
            mat[i][0] = 1
    if row0:
        for i in range(cols):
            mat[0][i] = 1
                

if __name__ == "__main__":
    mat=[
        [1,0,0,0,0,1],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [1,0,0,0,0,1],
        ]
    
    print(mat)

    boolean_mat(mat)
    
    print(mat)