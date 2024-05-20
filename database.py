import sqlite3 as sql
import requests
from random import *
from os.path import isfile
import ast

listRecords=['user_ID','user_LOGIN','user_LOGINPASS',
            'user_NAME','user_EMAIL','user_schoolNAME',
            'user_schoolID','user_CLASS','user_BIRTHDAY','user_GENDER',
            'stdent_SCORE','stdent_PHONENUM',
            'admin_EMAILPASS',
            'account_TYPE','stdent_ABSENT']
def checkAndInit():
    if isfile('database/user.db'):
        global connection,cursor
        connection = sql.connect('database/user.db')
        cursor = connection.cursor()
        return True
    else: 
        return False
def disconnect():
    global connection
    connection.close()
def createTable(tableName:str) -> bool:
    global connection
    creatTable:dict = {'USERS':'''
    CREATE TABLE IF NOT EXISTS "USERS"(
        user_ID MEDIUMINT,
        user_LOGIN TINYTEXT,
        user_LOGINPASS TINYTEXT,
        user_NAME TINYTEXT,
        user_EMAIL TINYTEXT,
        user_schoolNAME TINYTEXT,
        user_schoolID MEDIUMINT,
        user_CLASS TINYTEXT,
        user_BIRTHDAY TINYTEXT,
        user_GENDER TINYTEXT,
        stdent_SCORE TEXT(65535),
        stdent_PHONENUM TINYTEXT,          
        admin_EMAILPASS TINYTEXT,
        account_TYPE TINYTEXT,
        stdent_ABSENT 
        );
    ''',
    'MEETLINKS':'''
    CREATE TABLE IF NOT EXISTS MEETLINKS(
        meet_schoolID MEDIUMINT,
        meet_LINKS TINYTEXT
    );
    '''}
    
    connection.execute(creatTable[tableName])
    return True
def addUser(user_ID:int,user_LOGIN:int,user_LOGINPASS:str,
            user_NAME:str,user_EMAIL:str,user_schoolNAME:str,
            user_schoolID:int,user_CLASS:str,user_BIRTHDAY:str,user_GENDER:str,
            stdent_SCORE:str,stdent_PHONENUM:str,
            admin_EMAILPASS:str,
            account_TYPE:str,
            stdent_ABSENT:str):
    '''Insert values to the database:
    With 'USERS' table:
    - user_ID: MEDIUMINT
    - user_LOGIN: TINYTEXT
    - user_LOGINPASS: TINYTEXT
    - user_NAME: TINYTEXT
    - user_IMAGE: LONGTEXT
    - user_EMAIL: TINYTEXT
    - user_schoolNAME: TINYTEXT
    - user_schoolID: MEDIUMINT
    - user_CLASS: TINYTEXT
    - user_BIRTHDAY: TINYTEXT
    - user_GENDER: TINYTEXT
    - stdent_SCORE: TEXT(65535)
    - stdent_PHONENUM: TINYTEXT
    - admin_EMAILPASS
    - account_TYPE: TINYTEXT
    - stdent_ABSENT: MEDIUMINT
    '''

    global connection,cursor
    sql_insert = '''INSERT INTO USERS VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    params = (user_ID,user_LOGIN,user_LOGINPASS,user_NAME,user_EMAIL,
              user_schoolNAME,user_schoolID,user_CLASS,user_BIRTHDAY,user_GENDER,
              stdent_SCORE,stdent_PHONENUM,
              admin_EMAILPASS,
              account_TYPE,stdent_ABSENT)
    cursor.execute(sql_insert,params)
    connection.commit()
def addMeetLINK(meet_school_ID:int,meet_LINK:str):
    '''Insert values to the database:
    With 'MEETLINKS' table:
    - meet_school_ID: MEDIUMINT
    - meet_LINKS: TINYTEXT'''

    global connection,cursor
    sql_addMeetLINK = '''
    INSERT INTO MEETLINKS VALUES (?,?);
    '''
    params = (meet_school_ID,meet_LINK)
    cursor.execute(sql_addMeetLINK,params)
    connection.commit()
def getMeetLINKS(meet_schoolID):
    '''Get a LINK from table 'MEETLINKS' with its meet_schoolID'''
    global connection,cursor
    if meet_schoolID!='all':
        sql_select = f'SELECT meet_LINKS FROM MEETLINKS WHERE meet_schoolID = ?'
        results = cursor.execute(sql_select,(meet_schoolID,)).fetchall()
        return [result[0] for result in results]
    elif meet_schoolID == 'all':
        sql_select = f'SELECT meet_schoolID,meet_LINKS FROM MEETLINKS'
        results = cursor.execute(sql_select).fetchall()
        return [{'meet_schoolID':result[0],'meet_LINKS':result[1]} for result in results]
def getUserIn4(getIn4By:str,where:str,wantToGet:str|None ='*',account_TYPE=''):
    '''# Get user info by anythings. This's the most important method
    ~~~~
    ### Non-required argument `student`: `True`, `False` or `all`
    * `True` : account_TYPE = 'STDENT'
    * `False` : account_TYPE = 'ADMIN'
    * `all` : ignore 'account_TYPE'
    ~~~~
    ## Trường hợp 1:
    ##### - Trường hợp client yêu cầu GET, nhưng info không có trên database, hoặc yêu cầu lỗi
    #### -> Trả về một chuỗi, với nội dung 'Not Found!'
    * `Example: getUserIn4(getIn4By='user_ID',where='Something not available',wantToGet='*')`
    >OutputStructure: str
    ~~~~
    ## Trường hợp 2:
    ##### - Trường hợp client yêu cầu GET * giá trị, và chỉ có 1 giá trị tìm được
    ##### - Client phải tuân thủ quy tắc, GET thông tin của user từ database thì phải getInfoBy=='user_ID' vì user_ID là duy nhất đối với mỗi account!
    #### -> Trả về một json với keys là allKeys, values là info
    * `Example: getUserIn4(getIn4By='user_ID',where='29346715',wantToGet='*')`
    >Output: {"user_ID":'29346715',"user_LOGIN":"domenic.gutkowski","user_LOGINPASS":"YLJR7QxFrI","user_NAME":"Domenic Gutkowski", ...}
    >OutputStructure: dict(str,str)
    ~~~~
    ## Trường hợp 3:
    ##### - Trường hợp client yêu cầu GET * giá trị, và có >1 giá trị tìm được
    #### -> Trả về một list json với `n` phần tử là các giá trị tìm được, n là json với keys là allKeys, values là info
    * `Example: getUserIn4(getIn4By='user_CLASS',where='11A5',wantToGet='*')`
    >Output: [{"user_ID":'29346715',"user_LOGIN":"domenic.gutkowski","user_LOGINPASS":"YLJR7QxFrI","user_NAME":"Domenic Gutkowski", ...}]
    >OutputStructure: list(dict(str,str))
    ~~~~
    ## Trường hợp 4:
    ##### - Trường hợp client yêu cầu GET 1 giá trị, và chỉ có 1 giá trị tìm được
    #### -> Trả về một chuỗi, là wantToGet với giá trị info
    * `Example: getUserIn4(getIn4By='user_NAME',where='NGUYỄN NHƯ NGỌC',wantToGet='user_ID')`
    >Output: '82654793'
    >OutputStructure: str
    ~~~~
    ## Trường hợp 5:
    ##### - Trường hợp client yêu cầu GET 1 giá trị, và có >1 giá trị tìm được
    #### -> Trả về một list là info
    * `Example: getUserIn4(getIn4By='user_CLASS',where='11A5',wantToGet='user_ID')`
    >Output: [29346715,30941175,30213610,39825816,48844550,46505156,14616986,54590457,...]
    >OutputStructure: list(str)
    ~~~~
    ## Trường hợp 6:
    ##### - Trường hợp client yêu cầu GET >1 giá trị, hoặc không dùng *, và chỉ có 1 giá trị tìm được
    #### - Trả về một json với key là wantToGet, values là info với thứ tự là thứ tự của wantToGet
    * `Example: getUserIn4(getIn4By='user_ID',where='82654793',wantToGet='user_CLASS,user_LOGIN')`
    >Output: {'user_CLASS':'11A5','user_LOGIN':'student82654793'}
    >OutputStructure: dict(str,str)
    ~~~~
    ## Trường hợp 7:
    ##### - Trường hợp client yêu cầu GET >1 giá trị, hoặc không dùng *, và có >1 giá trị tìm được
    #### - Trả về một list json với `n` phần tử là các giá trị tìm được, mỗi giá trị `n` là một json, với key là wantToGet, values là info
    * `Example: getUserIn4(getIn4By='user_CLASS',where='11A5',wantToGet='user_ID,user_LOGIN')`
    >Output: [{'user_ID':'82654793','user_LOGIN':'student82654793'},...]
    >OutputStructure: list(dict(str,str))
    '''
    global connection,cursor,listRecords
    if account_TYPE=='':
        sql_select = f"""SELECT {wantToGet} FROM USERS WHERE {getIn4By} = ?"""
    elif account_TYPE!='':
        sql_select = f"""SELECT {wantToGet} FROM USERS WHERE {getIn4By} = ? AND account_TYPE = '{account_TYPE}' """
        
    result = cursor.execute(sql_select,(where,)).fetchall()
    wantToGetSplited = wantToGet.split(',')

    # Trường hợp 1
    if result==None or result==[]:
        return 'NotFound!'
    
    # Trường hợp 2
    if wantToGet == '*' and getIn4By=='user_ID' and len(result)==1:
        json_result = {key:result[0][idx] for idx,key in enumerate(listRecords)}
        return json_result
    
    # Trường hợp 3
    if wantToGet == '*' and len(result)>1:
        list_result = [{key:result[i][idx] for idx,key in enumerate(listRecords)} for i in range((len(result)))]
        return list_result
    
    # Trường hợp 4
    if len(wantToGetSplited) == 1 and len(result)==1:
        return result[0][0]
    
    # Trường hợp 5
    if len(wantToGetSplited) == 1 and len(result)>1:
        list_result = [i[0] for i in result]
        return list_result
    
    # Trường hợp 6
    if len(wantToGetSplited) > 1 and len(result)==1:
        json_result = {j:result[0][i] for i,j in enumerate(wantToGetSplited)}
        return json_result
    
    # Trường hợp 7
    if len(wantToGetSplited)>1 and len(result)>1:
        list_result = [{key:result[i][idx] for idx,key in enumerate(wantToGetSplited)} for i in range(len(result))]
        return list_result
def getAllCol(col:str):
    '''Get all data from a column, from 'USERS' table'''
    global connection,cursor
    sql_getCol = f'SELECT {col} FROM USERS'
    results = cursor.execute(sql_getCol).fetchall()
    return [result[0] for result in results]
def updateUser(updateIn4By:str,where:str,wantToUpdate:str):
    print('UPDATED!')
    '''Update user info by anythings
    Example:updateUser(updateIn4By='user_ID',where='82654793',user_CLASS='10A3')'''
    global connection,cursor

    wantToUpdate:dict = ast.literal_eval(wantToUpdate)

    updateSTR = [f"{key}='{wantToUpdate[key]}'" for key in wantToUpdate.keys()]
    updateSTR = ','.join(updateSTR)
    sql_update = f'UPDATE USERS SET {updateSTR} WHERE {updateIn4By} = ?'
    cursor.execute(sql_update,(where,))
    connection.commit()
def deleteUser(deleteUserBy:str,where:str):
    global connection,cursor
    sql_delete = f"DELETE FROM USERS WHERE {deleteUserBy}='{where}'"
    cursor.execute(sql_delete)
    connection.commit()
def addSTDENT()->str:
    def testGENDER(name):
        url = 'https://api.genderize.io'
        r = requests.get(url,params={'name':name})
        return r.json()['gender']
    def userIMG():
        r = requests.get('https://randomuser.me/api')
        results = r.json()['results'][0]
        url = results['picture']['large']
        imglink = requests.get(url)
        return sql.Binary(imglink.content)

    url = 'https://random-data-api.com/api/v2/users'
    r = requests.get(url=url,params={'response_type':'json','size':'5'})
    n=0
    for user in r.json():
        n+=1
        print(f'Added {n} users!',end='\r')
        addUser(user_ID=randint(10000000,99999999),
            user_LOGINPASS=user['password'],
            user_NAME=user['first_name']+' '+user['last_name'],
            user_BIRTHDAY=f'{str(randint(1,28))}-{str(randint(1,12))}-2007',
            user_CLASS='11A5',
            user_EMAIL=user['email'],
            user_GENDER=testGENDER(user['first_name']),
            user_IMAGE=userIMG(),
            user_LOGIN=user['username'],
            user_schoolID=10604083,
            user_schoolNAME='HOA VANG HIGH SCHOOL',
            stdent_PHONENUM=user['phone_number'],
            stdent_SCORE=f'''Math<1:{randint(1,10)+random()},{randint(1,10)+random()};2:{randint(1,10)+random()},{randint(1,10)+random()};3:{randint(1,10)+random()},{randint(1,10)+random()}>
            English<1:{randint(1,10)+random()},{randint(1,10)+random()};2:{randint(1,10)+random()},{randint(1,10)+random()};3:{randint(1,10)+random()},{randint(1,10)+random()}>
            Physics<1:{randint(1,10)+random()},{randint(1,10)+random()};2:{randint(1,10)+random()},{randint(1,10)+random()};3:{randint(1,10)+random()},{randint(1,10)+random()}>
            Chemistry<1:{randint(1,10)+random()},{randint(1,10)+random()};2:{randint(1,10)+random()},{randint(1,10)+random()};3:{randint(1,10)+random()},{randint(1,10)+random()}>
            Literature<1:{randint(1,10)+random()},{randint(1,10)+random()};2:{randint(1,10)+random()},{randint(1,10)+random()};3:{randint(1,10)+random()},{randint(1,10)+random()}>
            History<1:{randint(1,10)+random()},{randint(1,10)+random()};2:{randint(1,10)+random()},{randint(1,10)+random()};3:{randint(1,10)+random()},{randint(1,10)+random()}>
            Geography<1:{randint(1,10)+random()},{randint(1,10)+random()};2:{randint(1,10)+random()},{randint(1,10)+random()};3:{randint(1,10)+random()},{randint(1,10)+random()}>
            Biology<1:{randint(1,10)+random()},{randint(1,10)+random()};2:{randint(1,10)+random()},{randint(1,10)+random()};3:{randint(1,10)+random()},{randint(1,10)+random()}>
            CE<1:{randint(1,10)+random()},{randint(1,10)+random()};2:{randint(1,10)+random()},{randint(1,10)+random()};3:{randint(1,10)+random()},{randint(1,10)+random()}>
            Technology<1:{randint(1,10)+random()},{randint(1,10)+random()};2:{randint(1,10)+random()},{randint(1,10)+random()};3:{randint(1,10)+random()},{randint(1,10)+random()}>
            DE<1:{randint(1,10)+random()},{randint(1,10)+random()};2:{randint(1,10)+random()},{randint(1,10)+random()};3:{randint(1,10)+random()},{randint(1,10)+random()}>
            PE<1:{randint(1,10)+random()},{randint(1,10)+random()};2:{randint(1,10)+random()},{randint(1,10)+random()};3:{randint(1,10)+random()},{randint(1,10)+random()}>
            IT<1:{randint(1,10)+random()},{randint(1,10)+random()};2:{randint(1,10)+random()},{randint(1,10)+random()};3:{randint(1,10)+random()},{randint(1,10)+random()}>''',
            account_TYPE='STDENT',
            admin_EMAILPASS='')