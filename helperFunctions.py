from yahoo_fin.stock_info import *
import statistics
import requests
import xlrd
import xlwt
import os

######
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from helperFunctions import *
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split


def stockRecomendation(year, levelOfPredictions):
    
    year = int(year)
    
    availableRange = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
    
    if year <= 2011 or year >= 2021:
        print("invalid year")
        return(1)
    
    for level in range(len(levelOfPredictions)):
        
        if levelOfPredictions[level] not in availableRange:
            print("Invalid level selection")
            return(1)
    
    ## Train model for years prior
    #Select correct np files
    startingYear = 2011
    
    dataX = "company_Data_X_" + str(startingYear) + "_" + str(year) + '.npy'
    dataY = "company_Data_Y_" + str(startingYear) + "_" + str(year) + '.npy'
    
    cur_path = os.path.dirname(__file__)
    
    xPath = cur_path + '/data/npArrays/' + dataX
    yPath = cur_path + '/data/npArrays/' + dataY
            
    X = np.load(xPath)
    y = np.load(yPath)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    
    forest = (RandomForestClassifier(n_estimators= 96, criterion="entropy", random_state=2411)).fit(X_train,y_train)    
    
    ## Predict based on 
    
    dataX = "company_Data_X_" + str(year-1) + "_" + str(year) + '.npy'
    cur_path = os.path.dirname(__file__)
    xPath = cur_path + '/data/npArrays/' + dataX    
    
    Xtest = np.load(xPath)
    predictions = forest.predict(Xtest)
    
    pref_indx = []
    
    for i in range(len(predictions)):
        if predictions[i] in levelOfPredictions:
            pref_indx.append(i)
    
    #print(xPath)
    #print(pref_indx)
    ### Get stock ticks
    
    filePath = "Final_" + str(year-1) + "_data_perfYTD_" + str(year) + ".xls"
    cur_path = os.path.dirname(__file__)
    filePath = cur_path + '/data/excel/' + filePath    
    
    wb = xlrd.open_workbook(filePath)
    sheet = wb.sheet_by_index(0)
    
    recomendationTicks = []
    
    #for tick in pref_indx:
    for w in range(len(pref_indx)):
        tickIndx = pref_indx[w]
        element = str((sheet.cell_value(tickIndx, 0)))
        recomendationTicks.append(element)
    
    return recomendationTicks

def stockRecomendationMOD(year, levelOfPredictions):
    
    year = int(year)
    
    if year <= 2011 or year >= 2020:
        print("invalid year")
        return(1)
    
    
    ## Train model for years prior
    #Select correct np files
    startingYear = 2011
    
    dataX = "company_Data_X_" + str(startingYear) + "_" + str(year) + '.npy'
    dataY = "company_Data_Y_" + str(startingYear) + "_" + str(year) + '.npy'
    
    cur_path = os.path.dirname(__file__)
    
    xPath = cur_path + '/data/npArrays/' + dataX
    yPath = cur_path + '/data/npArrays/' + dataY
            
    X = np.load(xPath)
    y = np.load(yPath)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    
    forest = (RandomForestClassifier(n_estimators= 96, criterion="entropy", random_state=2411)).fit(X_train,y_train)    
    
    ## Predict based on 
    
    dataX = "company_Data_X_" + str(year-1) + "_" + str(year) + '.npy'
    cur_path = os.path.dirname(__file__)
    xPath = cur_path + '/data/npArrays/' + dataX    
    
    Xtest = np.load(xPath)
    predictions = forest.predict(Xtest)
    
    pref_indx = []
    bestCh = []
    bestCh.append(int(levelOfPredictions))
    
        
    for i in range(len(predictions)):
        if predictions[i] in bestCh:
            pref_indx.append(i)
    
    #print(xPath)
    #print(pref_indx)
    ### Get stock ticks
    
    filePath = "Final_" + str(year-1) + "_data_perfYTD_" + str(year) + ".xls"
    cur_path = os.path.dirname(__file__)
    filePath = cur_path + '/data/excel/' + filePath    
    
    wb = xlrd.open_workbook(filePath)
    sheet = wb.sheet_by_index(0)
    
    recomendationTicks = []
    
    #for tick in pref_indx:
    for w in range(len(pref_indx)):
        tickIndx = pref_indx[w]
        element = str((sheet.cell_value(tickIndx, 0)))
        recomendationTicks.append(element)
    
    returns = []
    returnSum = 0
    returnCount = 0
    
    filePath2 = "Final_" + str(year) + "_data_perfYTD_" + str(year+1) + ".xls"
    cur_path2 = os.path.dirname(__file__)
    filePath2 = cur_path2 + '/data/excel/' + filePath2    
    
    wb2 = xlrd.open_workbook(filePath2)
    sheet2 = wb2.sheet_by_index(0)
    
    for w in range(len(recomendationTicks)):
        
        tick = recomendationTicks[w]
        
        for i in range((sheet2.nrows)):
            element = str((sheet2.cell_value(i, 0)))
            if tick == element:
                tickReturn = (sheet2.cell_value(i, sheet2.ncols-1))
                returnSum = returnSum + tickReturn
                returnCount = returnCount + 1
    
    if returnCount == 0:
        print("ERROR: No stock in catagoty")
        return 0
    
    returnAVG = returnSum/returnCount
    return returnAVG
    

def computeStatistics(actual, forest_predictions, knn_predictions, SVC_predictions, displayAll = False):
    forest_counter = 0
    knn_counter = 0
    svc_counter = 0
    combined_counter = 0
    total = 0
    correct = 0
    mispredicted = []
    
    print("here1")

    for i in range(len(actual)):
        predictions = [forest_predictions[i], knn_predictions[i], SVC_predictions[i]]
        best_prediction = statistics.mode(predictions)
        if best_prediction == actual[i]:
            correct = correct +1
        else:
            mispredicted.append(i)
        if forest_predictions[i] == actual[i]:
            forest_counter = forest_counter +1 
        if knn_predictions[i] == actual[i]:
            knn_counter = knn_counter +1 
        if SVC_predictions[i] == actual[i]:
            svc_counter = svc_counter +1 
        total = total + 1
        
        if displayAll:
            print(actual[i],"best:", best_prediction, "forest:",forest_predictions[i], "knn:",knn_predictions[i], "svc:",SVC_predictions[i])
    
    print("here2")
    print(mispredicted)
    
    print("mispredicted:",len(mispredicted),"/", len(actual))
    score = (correct/total) * 100
    overall_forest_score = (forest_counter/total) * 100
    overall_knn_score = (knn_counter/total) * 100
    overall_scv_score_ = (svc_counter/total) * 100
    print("overall:", score)
    print("forest:", overall_forest_score)
    print("knn:", overall_knn_score)
    print("scv:", overall_scv_score_)


def computeStatisticsModified1(actual, forest_predictions, knn_predictions, SVC_predictions, displayAll = False):
    forest_counter = 0
    knn_counter = 0
    svc_counter = 0
    combined_counter = 0
    total = 0
    correct = 0
    mispredicted = []
    
    for i in range(len(actual)):
        predictions = [forest_predictions[i], knn_predictions[i], SVC_predictions[i]]
        best_prediction = statistics.mode(predictions)
        
        predictActual = actual[i]
        predictRange = []
        
        if predictActual == 0:
            predictRange = [0,1]
        elif predictActual == 20:
            predictRange = [19,20]
        else:
            predictRange = [predictActual-1,predictActual,predictActual+1]
        
        if best_prediction in predictRange:
            correct = correct +1
        else:
            mispredicted.append(i)
        
        if forest_predictions[i] in predictRange:
            forest_counter = forest_counter +1 
        if knn_predictions[i] in predictRange:
            knn_counter = knn_counter +1 
        if SVC_predictions[i] in predictRange:
            svc_counter = svc_counter +1 
        total = total + 1
        
        if displayAll:
            print(actual[i],"best:", best_prediction, "forest:",forest_predictions[i], "knn:",knn_predictions[i], "svc:",SVC_predictions[i])
    
    print(mispredicted)
    
    print("mispredicted:",len(mispredicted),"/", len(actual))
    score = (correct/total) * 100
    overall_forest_score = (forest_counter/total) * 100
    overall_knn_score = (knn_counter/total) * 100
    overall_scv_score_ = (svc_counter/total) * 100
    print("overall:", score)
    print("forest:", overall_forest_score)
    print("knn:", overall_knn_score)
    print("scv:", overall_scv_score_)

def computeStatisticsModified2(actual, forest_predictions, knn_predictions, SVC_predictions, displayAll = False):
    forest_counter = 0
    knn_counter = 0
    svc_counter = 0
    combined_counter = 0
    total = 0
    correct = 0
    mispredicted = []
    

    for i in range(len(actual)):
        predictions = [forest_predictions[i], knn_predictions[i], SVC_predictions[i]]
        best_prediction = statistics.mode(predictions)
        
        predictActual = actual[i]
        predictRange = []
        
        if predictActual == 0:
            predictRange = [0,1]
        elif predictActual == 20:
            predictRange = [19,20]
        else:
            predictRange = [predictActual-2,predictActual-1,predictActual,predictActual+1,predictActual+2]
        
        if best_prediction in predictRange:
            correct = correct +1
        else:
            mispredicted.append(i)
        
        if forest_predictions[i] in predictRange:
            forest_counter = forest_counter +1 
        if knn_predictions[i] in predictRange:
            knn_counter = knn_counter +1 
        if SVC_predictions[i] in predictRange:
            svc_counter = svc_counter +1 
        total = total + 1
        
        if displayAll:
            print(actual[i],"best:", best_prediction, "forest:",forest_predictions[i], "knn:",knn_predictions[i], "svc:",SVC_predictions[i])
    
    print(mispredicted)
    
    print("mispredicted:",len(mispredicted),"/", len(actual))
    score = (correct/total) * 100
    overall_forest_score = (forest_counter/total) * 100
    overall_knn_score = (knn_counter/total) * 100
    overall_scv_score_ = (svc_counter/total) * 100
    print("overall:", score)
    print("forest:", overall_forest_score)
    print("knn:", overall_knn_score)
    print("scv:", overall_scv_score_)

def getStockPrice(tick, Date):
    try:
        dateEdit = Date.split('/')
        if dateEdit[0] == 12:
            dateEdit[0] = 1
        else:
            tempDate = int(dateEdit[0]) + 1
            dateEdit[0] = str(tempDate)
        
        endDate = str(dateEdit[0]) + '/' + str(dateEdit[1]) + '/' + str(dateEdit[2])
        
        price = get_data(tick, start_date = Date, end_date = endDate,index_as_date = True, interval = '1mo')["close"]
        
        #print()
        #print(round(price[0],3))
        #print(round(price,3))
        price = round(float(price[0]),3)
        
        return price
    
    except AssertionError:
        #print("stock call error")
        return False
    
    except KeyError:
        #print("Stock call error")
        return False

def performanceOverTime0or1(tick, startDate, endDate, growth):
    try:
        dateEdit = startDate.split('/')
        
        if dateEdit[0] == 12:
            dateEdit[0] = 1
        else:
            tempDate = int(dateEdit[0]) + 1
            dateEdit[0] = str(tempDate)

        endDateEdit = str(dateEdit[0]) + '/' + str(dateEdit[1]) + '/' + str(dateEdit[2])

        start=get_data(tick, start_date=startDate, end_date=endDateEdit, index_as_date=True, interval='1mo')["close"]

        dateEdit=endDate.split('/')

        if dateEdit[0] == 12:
            dateEdit[0]=1
        else:
            tempDate=int(dateEdit[0]) + 1
            dateEdit[0]=str(tempDate)

        endDateEdit=str(dateEdit[0]) + '/' + str(dateEdit[1]) + '/' + str(dateEdit[2])

        end=get_data(tick, start_date=endDate, end_date=endDateEdit, index_as_date=True, interval='1mo')["close"]
        
        end=round(float(end), 3)
        start=round(float(start), 3)

        progress=0

        if end > (start*growth):
            progress=1
            print(tick, start, end)
        return progress

    except AssertionError:
        print("Stock call error 1")
        return None
    
    except KeyError:
        print("Stock call error 2")
        return None
    
    except TypeError:
        print("Stock call error 3")
        return None            

def performanceOverTimePersentage(tick, startDate, endDate):
    try:
        dateEdit = startDate.split('/')
        
        if dateEdit[0] == 12:
            dateEdit[0] = 1
        else:
            tempDate = int(dateEdit[0]) + 1
            dateEdit[0] = str(tempDate)

        endDateEdit = str(dateEdit[0]) + '/' + str(dateEdit[1]) + '/' + str(dateEdit[2])

        start=get_data(tick, start_date=startDate, end_date=endDateEdit, index_as_date=True, interval='1mo')["close"]

        dateEdit=endDate.split('/')

        if dateEdit[0] == 12:
            dateEdit[0]=1
        else:
            tempDate=int(dateEdit[0]) + 1
            dateEdit[0]=str(tempDate)

        endDateEdit=str(dateEdit[0]) + '/' + str(dateEdit[1]) + '/' + str(dateEdit[2])

        end=get_data(tick, start_date=endDate, end_date=endDateEdit, index_as_date=True, interval='1mo')["close"]
        
        end=round(float(end), 3)
        start=round(float(start), 3)
        
        progress = end/start
        
        return progress

    except AssertionError:
        print("Stock call error 1")
        return None
    
    except KeyError:
        print("Stock call error 2")
        return None
    
    except TypeError:
        print("Stock call error 3")
        return None