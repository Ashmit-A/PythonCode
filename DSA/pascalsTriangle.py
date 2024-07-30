def draw(numRows):
    if numRows==1 : return [[1]]
    
    prevRow = draw(numRows-1)
    newRow = [1]* numRows
    for i in range(1,numRows-1):
        newRow[i]=prevRow[-1][i] + prevRow[-1][i-1]
    prevRow.append(newRow)
    return prevRow

print(draw(5))