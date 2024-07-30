def maxProfitFunction(prices):
    buyIndex = 0
    sellIndex = 1
    maxProfit = 0

    while sellIndex<len(prices):
        profit = prices[sellIndex]-prices[buyIndex]
        
        if(prices[sellIndex]>prices[buyIndex]):
            maxProfit = max(profit,maxProfit)
        else : buyIndex = sellIndex
        sellIndex += 1
    
    return maxProfit

prices = [7,0,5,0,2]
print(maxProfitFunction(prices))