from app.PyClass import BrClass as br, TimeClass, OracleClass
from app.PyClass import XMLClass as XML

#fpath = 'D:\건축물대장 db수급/2025-03/'

fpath = 'c:/br/2025-04/'

fpath_mart_djy01 = f"{fpath}mart_djy_01.txt"
fpath_mart_djy02 = f"{fpath}mart_djy_02.txt"
fpath_mart_djy03 = f"{fpath}mart_djy_03.txt"
fpath_mart_djy04 = f"{fpath}mart_djy_04.txt"

def brMain():
    # /Resource/mapper/br.xml 호출
    xml = XML.XMLclass('brMapper')

    # 파일별로 사용될 ddl문, dml문을 xml에서 변수로 저장
    brMartDjy01 = { 'ddl' : xml.getData("setTableBrMartDjy01") ,'dml' : xml.getData("insertBrMartDjy01") ,'tablename' :  'S_IND.MART_DJY_01' }
    brMartDjy02 = { 'ddl' : xml.getData("setTableBrMartDjy02") ,'dml' : xml.getData("insertBrMartDjy02") ,'tablename' :  'S_IND.MART_DJY_02' }
    brMartDjy03 = { 'ddl' : xml.getData("setTableBrMartDjy03") ,'dml' : xml.getData("insertBrMartDjy03") ,'tablename' :  'S_IND.MART_DJY_03' }
    brMartDjy04 = { 'ddl' : xml.getData("setTableBrMartDjy04") ,'dml' : xml.getData("insertBrMartDjy04") ,'tablename' :  'S_IND.MART_DJY_04' }
    # brMartDjy05 = { 'ddl' : xml.getData("setTableBrMartDjy05") ,'dml' : xml.getData("insertBrMartDjy05") ,'tablename' :  'S_IND.MART_DJY_05' }
    # brMartDjy09 = { 'ddl' : xml.getData("setTableBrMartDjy09") ,'dml' : xml.getData("insertBrMartDjy09") ,'tablename' :  'S_IND.MART_DJY_09' }
    # brMartDjy11 = { 'ddl' : xml.getData("setTableBrMartDjy11") ,'dml' : xml.getData("insertBrMartDjy11") ,'tablename' :  'S_IND.MART_DJY_11' }
    brMartShtreg01 = { 'ddl' : xml.getData("setTableBrMartShtreg01") ,'dml' : xml.getData("insertBrMartShtreg01") ,'tablename' :  'S_IND.MART_SHTREG_01' }
    # brMartKcy07 = { 'ddl' : xml.getData("setTableBrMartKcy07") ,'dml' : xml.getData("insertBrMartKcy07") ,'tablename' :  'S_IND.MART_KCY_07' }
    # brMartKcy08 = { 'ddl' : xml.getData("setTableBrMartKcy08") ,'dml' : xml.getData("insertBrMartKcy08") ,'tablename' :  'S_IND.MART_KCY_08' }

    # 작업 소요시간 확인을 위한 Time클래스 생성
    t = TimeClass.Time()
    # 건축물대장 텍스트파일 경로
    #fpath = 'D:\건축물대장 db수급/2022-10/'


    ## 아래서부터는 DB에 적재할 파일별로 개별로 실행하거나, 전체실행

    # BrClass 생성 파일경로, ddl문, dml문
    mart_djy01 = br.BrFile(path=fpath_mart_djy01,ddl= brMartDjy01['ddl'],dml=brMartDjy01['dml'],tablename=brMartDjy01['tablename']) #기본개요
    mart_djy02 = br.BrFile(path=fpath_mart_djy02,ddl= brMartDjy02['ddl'],dml=brMartDjy02['dml'],tablename=brMartDjy02['tablename']) #총괄표제부
    mart_djy03 = br.BrFile(path=fpath_mart_djy03,ddl= brMartDjy03['ddl'],dml=brMartDjy03['dml'],tablename=brMartDjy03['tablename']) #표제부
    mart_djy04 = br.BrFile(path=fpath_mart_djy04,ddl= brMartDjy04['ddl'],dml=brMartDjy04['dml'],tablename=brMartDjy04['tablename']) #층별개요
    #mart_djy11 = br.BrFile(path=f"{fpath}mart_djy_11.txt",ddl= brMartDjy11['ddl'],dml=brMartDjy11['dml'],tablename=brMartDjy11['tablename']) #층별개요
    #mart_djy05 = br.BrFile(path=f"{fpath}mart_djy_05.txt",ddl= brMartDjy05['ddl'],dml=brMartDjy05['dml'],tablename=brMartDjy05['tablename']) #부속지번
    #mart_djy09 = br.BrFile(path="S:/건축물대장21.02.24/mart_djy_09.txt",ddl= brMartDjy09['ddl'],dml=brMartDjy09['dml'],tablename=brMartDjy09['tablename']) #전유부
    mart_shtreg01 = br.BrFile(path=f"{fpath}mart_shtreg_01.txt",ddl= brMartShtreg01['ddl'],dml=brMartShtreg01['dml'],tablename=brMartShtreg01['tablename']) #폐쇄말소대장
    # mart_kcy07 = br.BrFile(path=f"{fpath}mart_kcy_07.txt",ddl= brMartKcy07['ddl'],dml=brMartKcy07['dml'],tablename=brMartKcy07['tablename']) #허가 철거멸실
    # mart_kcy08 = br.BrFile(path=f"{fpath}mart_kcy_08.txt",ddl= brMartKcy08['ddl'],dml=brMartKcy08['dml'],tablename=brMartKcy08['tablename']) #허가 가설건축물


    #setTable() => drop& create table
    #readAndInsert(파일행수) => read File and insert to Table


    #파일별로 테이블을 drop하고 create 하고 입력


    if 1==1 :
        if mart_djy01.setTable() == 1:
            mart_djy01.readAndInsert(27956180)
    if 1==1 :
        if mart_djy03.setTable() == 1:
            mart_djy03.readAndInsert(8027734)

    if 1==1 :
        if mart_djy04.setTable() == 1:
            mart_djy04.readAndInsert(21044559)
    if 1==1 :
        if mart_djy02.setTable() == 1:
            mart_djy02.readAndInsert(615369)





    if 1==0 :
        if mart_shtreg01.setTable() == 1:
            mart_shtreg01.readAndInsert(3352333)

    #
    # workQueryList = [ xml.getData("setTableMART_DJY_01_MODF") , xml.getData("setTableMART_DJY_02_MODF") ,xml.getData("setTableMART_DJY_03_MODF") ,xml.getData("setTableMART_DJY_04_MODF")]
    #
    #
    # ora = OracleClass.Oracle()
    # for query in workQueryList:
    #     ora.query(query)
    #
    # if 1==0 :
    #     if mart_shtreg01.setTable() == 1 :
    #         mart_shtreg01.readAndInsert(3352333)

    #
    # if 1==1 :
    #     if mart_kcy07.setTable() == 1 :
    #         mart_kcy07.readAndInsert(462775)
    #
    # if 1==0 :
    #     if mart_kcy08.setTable() == 1 :
    #         mart_kcy08.readAndInsert(1940649)


# 실행
brMain()