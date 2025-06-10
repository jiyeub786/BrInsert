import os
import pandas as pd
import time

def getSqlDictList(inputFilePath):
    print("Read FileList from " + inputFilePath)
    inputFileList = os.listdir(inputFilePath)  # 읽은 파일 목록
    print("Read FileList completed")
    sqlList = []
    for i, v in enumerate(inputFileList):
        if os.path.isdir(inputFilePath+v) == False :
            print("Read sqlText from " + v)
            f = open(inputFilePath+"/"+v , "r",encoding="utf-8-sig")
            data = f.readlines()
            fileNm = v
            sql = ""
            for v2 in data:
                sql = sql + v2.replace(";","") # sql의 ;를 빼준다
            sqlDict = {"fileNm":fileNm, "sql":sql }
            sqlList.append(sqlDict)
    print("Make SQLList completed")
    return sqlList

def getSqlDictListToExcels(sqlDictList,outputFilePath,dbConnection):
    # sqlList의 dic 구성 [ "sql" ,"fileNm" ]

    print("Create DB Connection _ Connection is " + "EDUORACLE_CONNECTION")
    con = dbConnection
    timeStr = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))
    print(timeStr)
    dfCompletedList = []
    dfFailedList = []
    excelCompletedList = []
    excelFailedList = []
    dfDictList = []

    #sql to dataFrame 시작
    for i,  sqlDict in enumerate(sqlDictList):
       try:
           print(sqlDict)
           dfSql = pd.read_sql(sqlDict["sql"].encode("utf-8"), con)
           fileNm =sqlDict["fileNm"]


           dfDict = {"fileNm": fileNm , "dataFrame":dfSql}
           dfDictList.append( dfDict )
           print("["+ str(i+1) +"/" + str(len(sqlDictList)) +"] " + "append dataFrame from <"+sqlDict["fileNm"] +"> completed")
           dfCompletedList.append(sqlDict["fileNm"])
       except Exception as e:
           print("["+ str(i+1) +"/" + str(len(sqlDictList)) +"] " + "append dataFrame from <"+sqlDict["fileNm"] +">  failed")
           errorDict = {"inputFileNm":sqlDict["fileNm"],"error":str(e)}
           dfFailedList.append(errorDict)

    #sql to dataFrame result
    print("===========================sql to dataFrame result======================================")
    print("completed count = "+str(len(dfCompletedList)) +" failed count = "+ str(len(dfFailedList)))
    for v in dfFailedList:
        print(" failed inputFileNm = " + v["inputFileNm"] +" error >>>> "+ v["error"])
    print("==================================================================================")
    #sql to dataFrame 끝



    #dataFrame to excel 시작
    for i,  dfDict in enumerate(dfDictList):
       try:
           inputFileNm = dfDict["fileNm"]
           outputFileNm = timeStr+"_" +os.path.splitext(dfDict["fileNm"])[0] +  ".xlsx"
           resultFile = outputFilePath + "/"+ outputFileNm

           # 엑셀저장 , 틀고정, 인덱스 제거, 시트명 result
           dfDict["dataFrame"].to_excel(writer, sheet_name="result"  ,encoding='utf-8' , freeze_panes = (1, 0), index=False)
           writer.save()
           print("["+ str(i+1) +"/" + str(len(dfDictList)) +"] " + "write Result from <"+dfDict["fileNm"] +"> to <" + outputFileNm + "> completed")
           excelCompletedList.append(inputFileNm)
       except Exception as e:
           print("["+ str(i+1) +"/" + str(len(dfDictList)) +"] " + "write Result from <"+dfDict["fileNm"] +"> to <" +outputFileNm + "> failed")
           dic = {"inputFileNm":inputFileNm,"error":str(e)}
           excelFailedList.append(dic)

    #write Excel result
    print("============================writeExcel result======================================")
    print("completed count = "+str(len(excelCompletedList)) +" failed count = "+ str(len(excelFailedList)))
    for v in excelFailedList:
        print(" failed inputFileNm = " + v["inputFileNm"] +" error >>>> "+ v["error"])
    print("==================================================================================")
    #dataFrame to excel 끝



    # Close DB Connection
    print("close DB Connection")
    con.close()




def getSqlDictListToExcel(sqlDictList,outputFilePath,dbConnection):
    #sqlList의 dic 구성 [ "sql" ,"fileNm" ]

    print("Create DB Connection _ Connection is " + "EDUORACLE_CONNECTION")
    con = dbConnection
    dfCompletedList = []
    dfFailedList = []
    dfDictList = []

    #sql to dataFrame 시작
    for i,  sqlDict in enumerate(sqlDictList):
       try:
           dfSql = pd.read_sql(sqlDict["sql"].encode("utf-8"), con)
           fileNm =sqlDict["fileNm"]
           dfTitle = pd.DataFrame({'title':fileNm} ,index=[i])

           dfDict = {"title": dfTitle , "dataFrame":dfSql}
           dfDictList.append( dfDict )
           print("["+ str(i+1) +"/" + str(len(sqlDictList)) +"] " + "append dataFrame from <"+sqlDict["fileNm"] +"> completed")
           dfCompletedList.append(sqlDict["fileNm"])
       except Exception as e:
           print("["+ str(i+1) +"/" + str(len(sqlDictList)) +"] " + "append dataFrame from <"+sqlDict["fileNm"] +">  failed")
           errorDict = {"inputFileNm":sqlDict["fileNm"],"error":str(e)}
           dfFailedList.append(errorDict)

    #sql to dataFrame result
    print("===========================sql to dataFrame result======================================")
    print("completed count = "+str(len(dfCompletedList)) +" failed count = "+ str(len(dfFailedList)))
    for v in dfFailedList:
        print(" failed inputFileNm = " + v["inputFileNm"] +" error >>>> "+ v["error"])
    print("==================================================================================")
    # sql to dataFrame 종료



    #dataFrame to excel 시작
    timeStr = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))
    outputFileNm = timeStr+"_multipulResult"  + ".xlsx"
    resultFile = outputFilePath + "/" + outputFileNm
    writer = pd.ExcelWriter(resultFile, engine="xlsxwriter")
    row=0
    print("write multipulResultFile start")

    result = ""
    try:
        for i, dfDict in enumerate(dfDictList):
            dfDict["title"].to_excel(writer, sheet_name="result", startrow=row, startcol=0, index=False)
            row = row + len(dfDict["title"].index)  + 2
            dfDict["dataFrame"].fillna(0).to_excel(writer, sheet_name="result", startrow=row, startcol=0 )
            row = row + len(dfDict["dataFrame"].index)  + 2
            print("[" +str(i+1)+"/"+str(len(dfDictList))+"]"+" write dataFrame to excel completed" )
        writer.save()
        result = "write multipulResultFile completed >> result file = "+ resultFile
    except Exception as e:
        result = "write multipulResultFile failed >>" + str(e)

    print("===========================dataFrame to excel result======================================")
    print(result )
    print("==================================================================================")


    #dataFrame to excel 끝

    # Close DB Connection
    print("close DB Connection")

    con.close()




def statexcel(sqlDictList,outputFilePath,dbConnection):
    #sqlList의 dic 구성 [ "sql" ,"fileNm" ]

    print("Create DB Connection _ Connection is " + "EDUORACLE_CONNECTION")
    con = dbConnection
    dfCompletedList = []
    dfFailedList = []
    dfDictList = []

    #sql to dataFrame 시작
    for i,  sqlDict in enumerate(sqlDictList):
       try:
           dfSql = pd.read_sql(sqlDict["sql"].encode("utf-8"), con)
           fileNm =sqlDict["fileNm"]
           theme  = sqlDict["theme"]
           dfTitle = pd.DataFrame({'title':fileNm} ,index=[i])

           dfDict = {"title": dfTitle , "dataFrame":dfSql,"theme" : theme}
           dfDictList.append( dfDict )
           print("["+ str(i+1) +"/" + str(len(sqlDictList)) +"] " + "append dataFrame from <"+sqlDict["fileNm"] +"> completed")
           dfCompletedList.append(sqlDict["fileNm"])
       except Exception as e:
           print("["+ str(i+1) +"/" + str(len(sqlDictList)) +"] " + "append dataFrame from <"+sqlDict["fileNm"] +">  failed")
           errorDict = {"inputFileNm":sqlDict["fileNm"],"error":str(e)}
           dfFailedList.append(errorDict)

    #sql to dataFrame result
    print("===========================sql to dataFrame result======================================")
    print("completed count = "+str(len(dfCompletedList)) +" failed count = "+ str(len(dfFailedList)))
    for v in dfFailedList:
        print(" failed inputFileNm = " + v["inputFileNm"] +" error >>>> "+ v["error"])
    print("==================================================================================")
    # sql to dataFrame 종료



    #dataFrame to excel 시작
    timeStr = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))
    outputFileNm = timeStr+"_multipulResult"  + ".xlsx"
    resultFile = outputFilePath + "/" + outputFileNm
    writer = pd.ExcelWriter(resultFile, engine="xlsxwriter")
    row = 0
    row1=0
    row2=0
    row3=0
    row4=0
    row5=0
    print("write multipulResultFile start")


    result = ""
    try:
        for i, dfDict in enumerate(dfDictList):

            if dfDict["theme"] == 'ST':
                row = row1
            if dfDict["theme"] =='PM':
                row = row2
            if dfDict["theme"] =='SM':
                row = row3
            if dfDict["theme"] =='DOC':
                row = row4
            if dfDict["theme"] =='SMRY':
                row = row5

            dfDict["title"].to_excel(writer, sheet_name= dfDict["theme"], startrow=row, startcol=0, index=False)
            row = row + len(dfDict["title"].index)  + 2


            dfDict["dataFrame"].fillna(0).to_excel(writer, sheet_name= dfDict["theme"], startrow=row, startcol=0 )
            row = row + len(dfDict["dataFrame"].index)  + 2


            if dfDict["theme"] == 'ST':
                row1 = row
            if dfDict["theme"] =='PM':
                row2 = row
            if dfDict["theme"] =='SM':
                row3 = row
            if dfDict["theme"] =='DOC':
                row4 = row
            if dfDict["theme"] == 'SMRY':
                row5 = row

            print("[" +str(i+1)+"/"+str(len(dfDictList))+"]"+" write dataFrame to excel completed" )
        writer.save()
        result = "write multipulResultFile completed >> result file = "+ resultFile
    except Exception as e:
        result = "write multipulResultFile failed >>" + str(e)

    print("===========================dataFrame to excel result======================================")
    print(result )
    print("==================================================================================")


    #dataFrame to excel 끝

    # Close DB Connection
    print("close DB Connection")

    con.close()

