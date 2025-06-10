from app.PyClass import OracleClass, FileClass, TimeClass, LoggerClass

t = TimeClass.Time()
startTime = t.getNow()
class BrFile:
    def __init__(self, path,ddl,dml,tablename):
        self.brPath = path
        self.brDDL =  ddl
        self.brDML = dml
        self.brTableName = tablename
        self.endLine = 0

    def getDDL(self):
        return self.brDDL

    def getDML(self):
        return self.brDML

    def getFilePath(self):
        return self.brPath

    def setTable(self):
        try:
            ora = OracleClass.Oracle()
            ora.query("DROP TABLE "+self.brTableName + " PURGE")
            ora.query(self.brDDL)
            print("CREATE TABLE " +self.brTableName)
            return 1

        except Exception as e:
            LoggerClass.logger.info(e)
            return 0




    def setTableTruncate(self):
        ora = OracleClass.Oracle()
        ora.query("TRUNCATE TABLE "+self.brTableName)
        print("TRUNCATE TABLE")

    def setTableDROP(self):
        ora = OracleClass.Oracle()
        ora.query("DROP TABLE "+self.brTableName + " PURGE")
        print("DROP TABLE")

    def getEndLine(self):
        File01 = FileClass.File(self.brPath)
        f = File01.readFile()
        buffer = 1024 * 1024 * 10
        endLine = 0
        # get file end line
        while True:
            lines = f.readlines(buffer)
            endLine = endLine + str(lines).count("\\n")

            if not lines:
                f.close()
                break;
            print("\r seek endLine : " + str(endLine) + " Elapsed time:" + str(t.getTimeSub(startTime, t.getNow())) + "s", end="")
        print("")

        return endLine

    def readAndInsert(self,endLine):
        startTime = t.getNow()
        ora = OracleClass.Oracle()
        counter = 0
        buffersize = 10000
        insertbuffer = []

        File01 = FileClass.File(self.brPath)
        f = File01.readFile()

        listLength = len(f.readline().split('|'))

        while True:
            counter = counter + 1
            data = f.readline()
            try:
                if not data:
                    print("\rinserting rows :" + str(counter) + "/" + str(endLine) + "  [" + str( round( (counter-1) / endLine* 100, 4)) + "%] Elapsed time: " + str(t.getTimeSub(startTime, t.getNow())) + "s",                      end="")
                    ora.insertmany(self.brDML , insertbuffer)
                    ora.commit()
                    f.close()
                    break
                else:
                    dataSplited = data.split('|')
                    dataModf = []
                    if listLength == len(dataSplited):  #1행에서 확인한 열 개수와 읽는중 열 개수가 같은경우만 처리함
                        for i, v in enumerate(dataSplited):
                            if i < (len(dataSplited) ):
                                dataModf.append(v.replace("''", "None").replace("\\n", "None").strip()) #읽은 데이터를 리스트로작성

                        #print(tuple(dataModf))
                        insertbuffer.append(tuple(dataModf)) #읽은 데이터를 튜플로 저장

                    #print(dataModf)

                    if len(insertbuffer) == buffersize:
                        print("\rinserting rows :" + str(counter) + "/" + str(endLine) + "  [" + str( round( (counter-1) / endLine * 100, 4)) + "%] Elapsed time: " + str(                        t.getTimeSub(startTime, t.getNow())) + "s",                          end="")
                        ora.insertmany(self.brDML, insertbuffer)
                        ora.commit()

                        insertbuffer = []

            except Exception as e:
                insertbuffer = []
                LoggerClass.logger.info(e)
                break
        print('');