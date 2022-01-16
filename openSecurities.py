from helperFunctions import *
import time
from statistics import mean
from sys import exit

class Portfolio:
    def __init__(self, year):
        self.startingYear = year
        self.currYear = self.startingYear
        self.openPositions = []
        self.openPositionsYearAdded = []
        self.openPositionsPriceAdded = []
        self.openPositionsNumShares = []
        self.listOfReturns = []
        self.listOfReturnPercentages = []
        self.priceAtEndOfYear = []
        
        
        self.accumulatedReturnStart = 0
        self.accumulatedReturn = self.accumulatedReturnStart
        self.yearlyReturnList = []
        self.yearlyReturnPercentages = []
        
    
    def clearAndPrepForNewYear(self):
        
        self.incrementYear()
        self.openPositions.clear()
        self.openPositionsYearAdded.clear()
        self.openPositionsPriceAdded.clear()
        self.openPositionsNumShares.clear()
        self.listOfReturns.clear()
        self.listOfReturnPercentages.clear()
        self.priceAtEndOfYear.clear()
        
    def addReturns(self, lastYearReturn, lastYearReturnPercentage):
        self.accumulatedReturn = self.accumulatedReturn + lastYearReturn
        self.yearlyReturnList.append(lastYearReturn)
        self.yearlyReturnPercentages.append(lastYearReturnPercentage)
    
    def printPerformanceOfSim(self):
        yearsPassed = self.currYear - self.startingYear
        
        print()
        print("Annual returns:")
        
        for i in range(yearsPassed+1):
            print("  %-6s: $%-10s %-s%%" % (str(self.startingYear + i), str(self.yearlyReturnList[i]), str(self.yearlyReturnPercentages[i])))
        
        temp = "Summary:"
        
        yReturnSum = 0
        yPercentSum = 0
        
        for j in range(len(self.yearlyReturnList)):
            a = float(self.yearlyReturnList[j])
            b = float(self.yearlyReturnPercentages[j])
                        
            
            yReturnSum = yReturnSum + a
            yPercentSum = yPercentSum + b
        
        yearPercentAvg = yPercentSum/len(self.yearlyReturnList)
        
        print("  %-6s  $%-10s %-s%%" % ( str(temp) ,str(round(yReturnSum,2)), str(round(yearPercentAvg,2))))
        
    def closeYear(self):
        print()
        print("Closing positions.") 
        
        for i in range(len(self.openPositions)):
            
            endYear = "11/01/" + str(self.currYear)
            price = getStockPrice(str(self.openPositions[i]),str(endYear))
            
            if not price:
                endYear = "10/01/" + str(self.currYear)
                price = getStockPrice(str(self.openPositions[i]),str(endYear))  
            
            if not price:
                endYear = "9/01/" + str(self.currYear)
                price = getStockPrice(str(self.openPositions[i]),str(endYear))
                
            self.priceAtEndOfYear.append(price) 
        print()
        print("Positions closed.")
    
    def displayEndOfYearPositions(self):
        
        print()
        print("Ending positions for the year: " + str(self.currYear))
        print()
        print("    Stock     Starting Position in $    Ending Position in $   % Change   $ Delta")
        
        for i in range(len(self.openPositions)):
            
            startingPosition = str(round(float(self.openPositionsPriceAdded[i]) * int(self.openPositionsNumShares[i]),2))
            endingPosition = str(round(float(self.priceAtEndOfYear[i]) * int(self.openPositionsNumShares[i]),2))
            
            delta = float(endingPosition)-float(startingPosition)
            
            percentageChange = round((delta/float(startingPosition))*100,2)
                                   
            dollarChange = str(round(float(endingPosition)-float(startingPosition),2))
            
            self.listOfReturns.append(dollarChange)
            self.listOfReturnPercentages.append(percentageChange)
            
            print('%-4d %-9s %-25s %-22s %-10s %-10s' % (i, self.openPositions[i], startingPosition, endingPosition, percentageChange, dollarChange)) 
        
        totalYearReturn = 0
        avgYearReturn = 0
        
        
        for i in range(len(self.listOfReturns)):
            a = float(self.listOfReturns[i])
            totalYearReturn = totalYearReturn + a
        
        for i in range(len(self.listOfReturnPercentages)):
            a = float(self.listOfReturnPercentages[i])
            avgYearReturn = avgYearReturn + a
        
        avgYearReturn = round(avgYearReturn/len(self.listOfReturnPercentages),2)
        
        print()
        print("Income (loss) for the year " + str(self.currYear) + " is $" + str(round(totalYearReturn,2)))
        print("Return % for the year " + str(self.currYear) + " is " + str(avgYearReturn) + "%")
        
        self.addReturns(round(totalYearReturn,2), avgYearReturn)
    
    def addNewPositions(self, tick, year, numShares):
        
        newYear = "01/01/" + str(year)
        price = getStockPrice(str(tick),str(newYear))
        
        if not price:
            print("ERROR executing " + str(tick) + " trade.")
            return 
        
        self.openPositionsPriceAdded.append(price)        
        self.openPositions.append(tick)
        self.openPositionsYearAdded.append(year)
        self.openPositionsNumShares.append(numShares)
        
        
    def checkPositions(self):
                
        a = len(self.openPositionsPriceAdded) 
        b = len(self.openPositions) 
        c = len(self.openPositionsYearAdded) 
        d = len(self.openPositionsNumShares) 
        
        positions = [a, b, c, d]
        
        for i in range(len(positions)):
            for j in range(len(positions)):
                if positions[i] != positions[j]:
                    print()
                    print("CRITICAL ERROR, QUTTING.")
                    exit
            
        
    
    def incrementYear(self):
        self.currYear = self.currYear + 1
    
    def show(self):
        print(self.openPositions)
        print(self.openPositionsYearAdded)
        print(self.openPositionsPriceAdded)
        print(self.openPositionsNumShares)
        
    def displayOpenPositions(self):
        
        print()
        print("Open positions for the year: " + str(self.currYear))
        print()
        print("    Stock     Strike price    Number of Shares")
        
        for i in range(len(self.openPositions)):
            print('%-4d %-9s %-15s %-10s' % (i, self.openPositions[i], self.openPositionsPriceAdded[i], self.openPositionsNumShares[i]))
        

def main():
    
    welcomePrint()
    instructions()
    
    useChoice()

def useChoice():
    
    print("What do you want to do?")
    print("1.   Stock predictions for a particular year?")
    print("2.   Trading simulation for a single year?")
    print("3.   Trading simulation for multiple years?")
    userIn = input("Choice: ")
    
    avalableChoice = ['1','2','3']
    
    if userIn not in avalableChoice:
        print()
        print("Invalid choice. Try again.")
        useChoice()
    
    if userIn == "1":
        firstChoice()
        closeSession()
        
    elif userIn == "2":
        print()
        userIn = input("What year would you like to start the simulation? ")
        avalableYears = ['2012','2013','2014', '2015', '2016', '2017', '2018', '2019', '2020']
        
        while userIn not in avalableYears:
            print()
            print("Invalid choice. Try again.")
            print()
            userIn = input("What year would you like to start the simulation? ")
            
        
        protfolio = Portfolio(int(userIn))
        a = secondChoice(userIn)
        if a == 1:
            closeSession()
        elif a[0] == 2:
            
            tradeListExecute = a[1][0]
            numShares = a[2]
            
            for i in range(len(tradeListExecute)):
                protfolio.addNewPositions(str(tradeListExecute[i]), str(userIn), numShares[i]) 
            
            protfolio.checkPositions()
            print()
            print("Congratulations, your positions executed!")
            
            userIn2 = optionsChoice2()
            
            if userIn2 == '1':
                protfolio.displayOpenPositions()
                time.sleep(5)
                userIn2 = optionsChoice2()
            
            if userIn2 == '1':
                protfolio.displayOpenPositions()
                time.sleep(5)
                userIn2 = optionsChoice2()
                
            if userIn2 == '2':
                protfolio.closeYear()
                protfolio.displayEndOfYearPositions()
                closeSessionDefinite()
    
    elif userIn == "3":
        print()
        userIn = input("What year would you like to start the simulation? ")
        avalableYears = ['2012','2013','2014', '2015', '2016', '2017', '2018', '2019', '2020']
        
        while userIn not in avalableYears:
            print()
            print("Invalid choice. Try again.")
            print()
            userIn = input("What year would you like to start the simulation? ")
            
        
        protfolio = Portfolio(int(userIn))
        a = thirdChoice(userIn)
        if a == 1:
            closeSession()
        elif a[0] == 2:
            
            tradeListExecute = a[1][0]
            numShares = a[2]
            
            for i in range(len(tradeListExecute)):
                protfolio.addNewPositions(str(tradeListExecute[i]), str(userIn), numShares[i]) 
            
            protfolio.checkPositions()
            print()
            print("Congratulations, your positions executed!")
                        
            while int(protfolio.currYear) < 2020:
                
                userIn2 = optionsChoic3()
                
                if userIn2 == '1':
                    protfolio.displayOpenPositions()
                    time.sleep(5)
                    userIn2 = optionsChoic3()
                
                if userIn2 == '1':
                    protfolio.displayOpenPositions()
                    time.sleep(5)
                    userIn2 = optionsChoic3()
                    
                if userIn2 == '2':
                    protfolio.closeYear()
                    protfolio.displayEndOfYearPositions()
                    protfolio.printPerformanceOfSim()
                    closeSessionDefinite() 
                
                if userIn2 == '3':
                    protfolio.closeYear()
                    protfolio.displayEndOfYearPositions()
                    protfolio.clearAndPrepForNewYear()
                    callForThree(protfolio)
            
            print()
            print("That was the last year of the simulation.")
            print()
            
            userIn2 = optionsChoic2()
                
            if userIn2 == '1':
                protfolio.displayOpenPositions()
                time.sleep(5)
                userIn2 = optionsChoic3()
            
            if userIn2 == '1':
                protfolio.displayOpenPositions()
                time.sleep(5)
                userIn2 = optionsChoic3()
                
            if userIn2 == '2':
                protfolio.closeYear()
                protfolio.displayEndOfYearPositions()
                protfolio.printPerformanceOfSim()
                closeSessionDefinite() 
            
def callForThree(protfolio):
    print()
    print("Make your selection for " + str((protfolio.currYear)))
    print()
    
    a = thirdChoice(protfolio.currYear)
    if a == 1:
        closeSession()
    elif a[0] == 2:
        
        tradeListExecute = a[1][0]
        numShares = a[2]
        
        for i in range(len(tradeListExecute)):
            protfolio.addNewPositions(str(tradeListExecute[i]), str(protfolio.currYear), numShares[i]) 
        
        protfolio.checkPositions()
        print()
        print("Congratulations, your positions executed!")
                    
        while int(protfolio.currYear) < 2020:
            
            userIn2 = optionsChoic3()
            
            if userIn2 == '1':
                protfolio.displayOpenPositions()
                time.sleep(5)
                userIn2 = optionsChoic3()
            
            if userIn2 == '1':
                protfolio.displayOpenPositions()
                time.sleep(5)
                userIn2 = optionsChoic3()
                
            if userIn2 == '2':
                protfolio.closeYear()
                protfolio.displayEndOfYearPositions()
                protfolio.printPerformanceOfSim()
                closeSessionDefinite() 
            
            if userIn2 == '3':
                protfolio.closeYear()
                protfolio.displayEndOfYearPositions()
                protfolio.clearAndPrepForNewYear()
                callForThree(protfolio)
        
        print()
        print("That was the last year of the simulation.")
        print()
        
        userIn2 = optionsChoice2()
            
        if userIn2 == '1':
            protfolio.displayOpenPositions()
            time.sleep(5)
            userIn2 = optionsChoic3()
        
        if userIn2 == '1':
            protfolio.displayOpenPositions()
            time.sleep(5)
            userIn2 = optionsChoic3()
            
        if userIn2 == '2':
            protfolio.closeYear()
            protfolio.displayEndOfYearPositions()
            protfolio.printPerformanceOfSim()
            closeSessionDefinite()    
                
def optionsChoice2():
    print()
    print("Options: ")
    print("  1. Display open positons")
    print("  2. Close positions and quit simulation")
    userIn2 = input("Choice: ")
    return userIn2

def optionsChoic3():
    print()
    print("Options: ")
    print("  1. Display open positons")
    print("  2. Close positions and quit simulation")
    print("  3. Close positions and continue simulation")
    userIn2 = input("Choice: ")
    return userIn2

#
#def startInvestmentYear(year):
   
#def closeInvestmentYear(year):

def closeSessionDefinite():

    print()
    print("Thank you for using openSecurities!")
    exit
    
def closeSession():
    print()
    userIn = input("Close openSecurities (y/n)? ")
    
    if userIn == "y" or userIn == "Y":
        print()
        print("Thank you for using openSecurities!")
        exit
    elif userIn == "n" or userIn == "N":
        useChoice()
    else:
        print()
        print("Invalid choice. Try again.")
        closeSession()

def thirdChoice(userIn):
    
    print()
    print("What level of predictions do you want to choose?")
    print("Options:")
    print("  1. Pre-defined predicted optimum")
    print("  2. Your choice of 0-21, each split by comma.")
    print("     example: 12,16,17")
    userIn2 = input("Choice: ")
    print() 
    
    avalableChoice = ['1','2']
    
    while userIn2 not in avalableChoice:
        print("Invalid choice. Try again.")
        print()
        print("What level of predictions do you want to choose?")
        print("Options:")
        print("  1. Pre-defined predicted optimum")
        print("  2. Your choice of 0-21, each split by comma.")
        print("     example: 12,16,17")
        userIn2 = input("Choice: ")
        print()        
    
    bestCH = [18,19]
    
    if userIn2 == "1":
        ret = stockRecomendation(int(userIn),bestCH)
        
    elif userIn2 == "2":
        userIn3 = input("Enter your selection: ")
        
        while specialCatChoice(userIn3):
            print("Invalid choice. Try again.")
            print()
            userIn3 = input("Enter your selection: ")        
        
        userSelection = []
        
        selection = userIn3.split(",")
        
        for i in range(len(selection)):
            newSel = selection[i].strip()
            userSelection.append(int(newSel))
        
        ret = stockRecomendation(int(userIn),userSelection)
    
    for stock in range(len(ret)):
        print(str(stock) + ". " + str(ret[stock]))
    
    print()
    
    userIn4 = input("Ready to execute a trade? (y/n) ")
    
    availableChoice = ['y', 'Y', 'n', 'N']
    
    while userIn4 not in availableChoice:
        print()
        print("Invalid choice. Try again.")
        print()
        userIn4 = input("Ready to execute a trade? (y/n) ")
        print()
    print()
    tradeList = []
    
    if userIn4 == "n" or userIn4 == "N":
        return(1)
    
    elif userIn4 == "y" or userIn4 == "Y":
        
        print("Which securities do you want to trade?")
        print("  1. All of the securities displayed above.")
        print("  2. Input your own selection, according to numbers above.")
        print("     example: 1, 7, 16")
        print()
        userIn5 = input("Choice: ")
        
        avalableChoice = ['1','2']
        
        while userIn5 not in avalableChoice:
            print("Invalid choice. Try again.")
            print()
            print("Which securities do you want to trade?")
            print("  1. All of the securities displayed above.")
            print("  2. Input your own selection, according to numbers above.")
            print("     example: 1, 7, 16")
            print()
            userIn5 = input("Choice: ")
            print()         
        
        if userIn5 == "1":
            
            numSharesList = []
            numShares = input("How many shares of each stock do you want to purchase? ")
            tradeList.append(ret)
            
            for i in range(len(tradeList[0])):
                numSharesList.append(numShares)
                        
            return [2, tradeList, numSharesList]
        
        elif userIn5 == "2":
            
            userIn6 = input("Enter your selection: ")
            
            userSelection = []
            
            selection = userIn6.split(",")
            
            for i in range(len(selection)):
                newSel = selection[i].strip()
                
                if int(newSel) < 0 or int(newSel) > len(ret)-1:
                    print("invalid selection of " + str(newSel) + " removed.")
                else:
                    userSelection.append(int(newSel))    
            
            
            # Ask how many shares of each
            numSharesOfEachSelected = []
            stocksToPopIndx = []
            for i in range(len(userSelection)):
                ind = userSelection[i]
                print()
                userIn7 = input("How many shares of " + ret[ind] + " do you want to buy? ")
                
                if not float(userIn7).is_integer() or int(userIn7) < 0:
                    print()
                    print("invalid selection for " + ret[ind])
                    print(ret[ind] + " removed from selection")
                    stocksToPopIndx.append(i)
                
                else:
                    numSharesOfEachSelected.append(userIn7)
            
            numElementsPoped = 0
            for i in range(len(stocksToPopIndx)):
                indx = stocksToPopIndx[i] - numElementsPoped
                userSelection.pop(indx)
                numElementsPoped = numElementsPoped + 1
                
            finalSelection = []
            temList = []
            
            for i in range(len(userSelection)):
                ind = userSelection[i]
                temList.append(ret[ind])
                
            finalSelection.append(temList)
            
            return [2, finalSelection, numSharesOfEachSelected]

def secondChoice(userIn):
    
    print()
    print("What level of predictions do you want to choose?")
    print("Options:")
    print("  1. Pre-defined predicted optimum")
    print("  2. Your choice of 0-21, each split by comma.")
    print("     example: 12,16,17")
    userIn2 = input("Choice: ")
    print() 
    
    avalableChoice = ['1','2']
    
    while userIn2 not in avalableChoice:
        print("Invalid choice. Try again.")
        print()
        print("What level of predictions do you want to choose?")
        print("Options:")
        print("  1. Pre-defined predicted optimum")
        print("  2. Your choice of 0-21, each split by comma.")
        print("     example: 12,16,17")
        userIn2 = input("Choice: ")
        print()        
    
    bestCH = [18,19]
    
    if userIn2 == "1":
        ret = stockRecomendation(int(userIn),bestCH)
        
    elif userIn2 == "2":
        userIn3 = input("Enter your selection: ")
        
        while specialCatChoice(userIn3):
            print("Invalid choice. Try again.")
            print()
            userIn3 = input("Enter your selection: ")        
        
        userSelection = []
        
        selection = userIn3.split(",")
        
        for i in range(len(selection)):
            newSel = selection[i].strip()
            userSelection.append(int(newSel))
        
        ret = stockRecomendation(int(userIn),userSelection)
    
    for stock in range(len(ret)):
        print(str(stock) + ". " + str(ret[stock]))
    
    print()
    
    userIn4 = input("Ready to execute a trade? (y/n) ")
    
    availableChoice = ['y', 'Y', 'n', 'N']
    
    while userIn4 not in availableChoice:
        print()
        print("Invalid choice. Try again.")
        print()
        userIn4 = input("Ready to execute a trade? (y/n) ")
        print()
    print()
    tradeList = []
    
    if userIn4 == "n" or userIn4 == "N":
        return(1)
    
    elif userIn4 == "y" or userIn4 == "Y":
        
        print("Which securities do you want to trade?")
        print("  1. All of the securities displayed above.")
        print("  2. Input your own selection, according to numbers above.")
        print("     example: 1, 7, 16")
        print()
        userIn5 = input("Choice: ")
        
        avalableChoice = ['1','2']
        
        while userIn5 not in avalableChoice:
            print("Invalid choice. Try again.")
            print()
            print("Which securities do you want to trade?")
            print("  1. All of the securities displayed above.")
            print("  2. Input your own selection, according to numbers above.")
            print("     example: 1, 7, 16")
            print()
            userIn5 = input("Choice: ")
            print()         
        
        if userIn5 == "1":
            
            numSharesList = []
            numShares = input("How many shares of each stock do you want to purchase? ")
            tradeList.append(ret)
            
            for i in range(len(tradeList[0])):
                numSharesList.append(numShares)
                        
            return [2, tradeList, numSharesList]
        
        elif userIn5 == "2":
            
            userIn6 = input("Enter your selection: ")
            
            userSelection = []
            
            selection = userIn6.split(",")
            
            for i in range(len(selection)):
                newSel = selection[i].strip()
                
                if int(newSel) < 0 or int(newSel) > len(ret)-1:
                    print("invalid selection of " + str(newSel) + " removed.")
                else:
                    userSelection.append(int(newSel))    
            
            
            # Ask how many shares of each
            numSharesOfEachSelected = []
            stocksToPopIndx = []
            for i in range(len(userSelection)):
                ind = userSelection[i]
                print()
                userIn7 = input("How many shares of " + ret[ind] + " do you want to buy? ")
                
                if not float(userIn7).is_integer() or int(userIn7) < 0:
                    print()
                    print("invalid selection for " + ret[ind])
                    print(ret[ind] + " removed from selection")
                    stocksToPopIndx.append(i)
                
                else:
                    numSharesOfEachSelected.append(userIn7)
            
            numElementsPoped = 0
            for i in range(len(stocksToPopIndx)):
                indx = stocksToPopIndx[i] - numElementsPoped
                userSelection.pop(indx)
                numElementsPoped = numElementsPoped + 1
                
            finalSelection = []
            temList = []
            
            for i in range(len(userSelection)):
                ind = userSelection[i]
                temList.append(ret[ind])
                
            finalSelection.append(temList)
            
            return [2, finalSelection, numSharesOfEachSelected]
            
def firstChoice():
    print()
    userIn = input("What year would you like a prediction for? ")
    
    print()
    print("What level of predictions do you want to choose?")
    print("Options:")
    print("  1. Pre-defined predicted optimum")
    print("  2. Your choice of 0-21, each split by comma.")
    print("     example: 12,16,17")
    print()
    userIn2 = input("Choice: ")
    print()
    
    avalableChoice = ['1','2']
    
    while userIn2 not in avalableChoice:
        print("Invalid choice. Try again.")
        print()
        print("What level of predictions do you want to choose?")
        print("Options:")
        print("  1. Pre-defined predicted optimum")
        print("  2. Your choice of 0-21, each split by comma.")
        print("     example: 12,16,17")
        userIn2 = input("Choice: ")
        print()    
    
    bestCH = [18,19]
    
    if userIn2 == "1":
        ret = stockRecomendation(int(userIn),bestCH)
        
    elif userIn2 == "2":
        userIn3 = input("Enter your selection: ")
        
        while specialCatChoice(userIn3):
            print("Invalid choice. Try again.")
            print()
            userIn3 = input("Enter your selection: ")
            
        
        userSelection = []
        
        selection = userIn3.split(",")
        
        for i in range(len(selection)):
            newSel = selection[i].strip()
            userSelection.append(int(newSel))
        
        ret = stockRecomendation(int(userIn),userSelection)
    
    for stock in range(len(ret)):
        print(str(stock) + ". " + str(ret[stock]))

def specialCatChoice(choice):
    
    userSelection = []
    
    selection = choice.split(",")
    
    for i in range(len(selection)):
        newSel = selection[i].strip()
        userSelection.append(int(newSel))
    
    for j in range(len(userSelection)):
        if int(userSelection[j]) < 0 or int(userSelection[j]) > 21:
            return True
    
    return False

def welcomePrint():
    print()
    print("############################")
    print("##                        ##")
    print("##     openSecurities     ##")
    print("##                        ##")
    print("############################")
    print()    
    
def instructions():
    
    print("Instructions? (y/n)")
    userIn = input("Choice: ") 
    print()
    
    if userIn == "y" or userIn == "Y":
        print("Use this link to read instructions.")
        return
    
    elif userIn == "n" or userIn == "N":
        return
    
    else:
        print("invalid response") 
        instructions()
        print()

main()
