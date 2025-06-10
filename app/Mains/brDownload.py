#사용방법
# 1. 다운로드 폴더를 생성하고 save_path 변수 수정
# 2. 건축물대장 분할다운로드 게시판 확인: https://open.eais.go.kr/board/selectBoardNtcMgmList.do?viewType=C2
# 3. main() 함수의 yyyy, mm에 다운로드 받을 년월 입력. 게시판 1페이지와 2페이지에서 년월 텍스트에 해당하는 기본개요, 표제부, 층별개요 게시물 번호를 식별합니다
# 4. 해당 게시물의 첨부파일 id와 sn을 식별하고, 그 첨부파일을 다운로드 받는다
# 5. 다운로드는 순차적으로 진행되고, 다운로드가 15초이상 멈추면 성공할때까지 재시도함
# 6. 기본개요, 표제부, 층별개요 전부 받는 시간은 1시간 정도.. 진행사항은 실행메시지를 참고하시길..
# 7. 총괄표제부는 게시판에 업로드되지 않고 대용량 받기에서 받으셔야함.


import requests
import time
import re
from bs4 import BeautifulSoup


def getFormattedTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def downloadFile( save_path, file_name,url,headers , progress_txt):
    with open(save_path+ file_name, "wb") as file:  # open in binary mode
        try :
            print(f"[{getFormattedTime()}] {progress_txt} {file_name} start")# get request
            response = requests.post(url,headers = headers, timeout = 15)
            file.write(response.content)  # write to file
            print(f"[{getFormattedTime()}] {progress_txt} {file_name} complete")# get request

        except:
            print(f"[{getFormattedTime()}] {progress_txt} {file_name} failed and re-try")
            downloadFile( save_path, file_name,url,headers ,progress_txt)

def searchDownloadLinks(download_site,headers):
    source = requests.get(download_site ,headers=headers).text
    soup = BeautifulSoup(source, 'html.parser')
    elem_list = soup.select('div.ntc-view a')
    list =[]
    for n,i in enumerate(elem_list):
        list.append(        {'file_nm' : i.getText() , 'file_id': i.get("href").split('\'')[1],'file_sn': i.get("href").split('\'')[3]} )

    return list

def searchPost(download_site,headers,yyyy,mm):
    source = requests.get(download_site ,headers=headers).text
    soup = BeautifulSoup(source, 'html.parser')
    elem_list = soup.select('table.bbs_type3 a')
    list =[]
    for n,i in enumerate(elem_list):
        pattn = re.compile(f'.*(기본개요|표제부|층별개요).*({yyyy}년 {mm}월).*' )
        if pattn.match(i.getText()) != None :
            list.append ( i.get("href").split('\'')[1] )
    print( f"[{getFormattedTime()}] Download Target Post: {', '.join(list)}")
    return list



def main():
    ##  yyyy, mm ,save_path 수정하세요!   ##
    yyyy = '2024'
    mm = '09'
    save_path = f'D:/건축물대장 db수급/2024-09/'

    print(f'다운로드 년월: {yyyy} {mm}')
    print(f'다운로드 경로: {save_path}')
    board_link_pg1 = f'https://open.eais.go.kr/board/selectBoardNtcMgmList.do?viewType=C2&pageIndex=1'
    board_link_pg2 = f'https://open.eais.go.kr/board/selectBoardNtcMgmList.do?viewType=C2&pageIndex=2'
    header1 = {'Referer': 'https://open.eais.go.kr'
        ,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        , 'Origin': 'https://open.eais.go.kr'
        ,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        , 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,vi;q=0.6'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Content-Type': 'application/x-www-form-urlencoded'
        , 'Sec-Ch-Ua-Platform': '"Windows"'
        , 'Host': 'open.eais.go.kr'
        , 'Connection': 'keep-alive'
                }
    post_list = []
    file_list = []
    post_list.extend(searchPost(board_link_pg1,header1,yyyy,mm))
    post_list.extend(searchPost(board_link_pg2,header1,yyyy,mm))
    for ntcSn in post_list:
        post_link =  f'https://open.eais.go.kr/board/selectBoardNtcMgmDetail.do?viewType=C2Dtl&ntcSn={ntcSn}'
        header2 = {'Referer': f'https://open.eais.go.kr/board/selectBoardNtcMgmDetail.do?viewType=C2Dtl&ntcSn={ntcSn}'
                     ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
                     , 'Origin': 'https://open.eais.go.kr'
                     ,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
                     , 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,vi;q=0.6'
                     , 'Accept-Encoding': 'gzip, deflate, br'
                     , 'Content-Type': 'application/x-www-form-urlencoded'
                     , 'Sec-Ch-Ua-Platform': '"Windows"'
                     , 'Host': 'open.eais.go.kr'
                     , 'Connection': 'keep-alive'
                    }
        file_list.extend(searchDownloadLinks(post_link,header1))

    print(f"[{getFormattedTime()}] Download Meta Info:' {str(file_list)}")

    for i, file in enumerate(file_list):
        progress_txt = f'[{str(i + 1)}/{len(file_list)}]'

        file_nm = file['file_nm']
        file_id = file['file_id']
        file_sn = file['file_sn']
        attch_file_link = f'https://open.eais.go.kr/board/downNtc.do?fileSn={file_id}&fileDetlSn={file_sn}'
        downloadFile(save_path ,file_nm ,attch_file_link ,header2 ,progress_txt )


    print(f"[{getFormattedTime()}] 완료")



#실행부
main()

