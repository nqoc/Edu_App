from fastapi import FastAPI
import database as db
import server
import uvicorn

app = FastAPI()
print('Successful!') if db.checkAndInit() else print('Failed!')
if db.checkAndInit():
    @app.get('/check')
    async def API_checkAndInit():
        '''**Check** and **Initialize** the database'''
        return {'status':'successful'}
else:
    @app.get('/check')
    async def API_checkAndInit():
        return {'status':'failed'}

@app.get('/')
async def main():
    return 'Greeting from API!'
@app.get('/userIn4/')
async def API_getUserIn4(getIn4By:str,where:str,account_TYPE:str='',wantToGet:str | None = '*'):
    return  db.getUserIn4(getIn4By=getIn4By,where=where,wantToGet=wantToGet,account_TYPE=account_TYPE)
@app.post('/update')
async def API_updateUser(updateIn4By,where,wantToUpdate:str):
    print(list(map(type,[updateIn4By,where,wantToUpdate])),sep=',')
    print(updateIn4By,where,wantToUpdate,sep=';')
    db.updateUser(updateIn4By=updateIn4By,where=where,wantToUpdate=wantToUpdate)
    return
@app.post('/save')
async def API_saveAFile(content:str,postType:str):
    match postType:
        case 'best':
            with open('resources/best.csv','a+') as file:
                file.seek(0)
                rank = list(map(int,file.read().split('\n')[1].split(',')) )
                rank = {j:rank[i] for i,j in enumerate('RIASEC')}
                for i in content:
                    rank[i]+=1
                file.truncate(0)
                print(f"{','.join('RIASEC')}\n{','.join(map(str,rank.values()))}",file=file)
        case 'ratio':
            with open('resources/ratio.csv','a+') as file:
                print(content,file=file)
    print(content)
    return
@app.post('/add')
async def API_addUser(wantToAdd,toAdd:dict):
    if wantToAdd=='meetlink':
        print(wantToAdd,toAdd)
        db.addMeetLINK(toAdd['meet_schoolID'],toAdd['meet_LINK'])
        return
    elif wantToAdd=='user':
        db.addUser(user_ID=toAdd['user_ID'],user_LOGIN=toAdd['user_LOGIN'],user_BIRTHDAY=toAdd['user_BIRTHDAY'],
                   user_CLASS=toAdd['user_CLASS'],user_EMAIL=toAdd['user_EMAIL'],user_LOGINPASS=toAdd['user_LOGINPASS'],
                   user_GENDER=toAdd['user_GENDER'],user_NAME=toAdd['user_NAME'],user_schoolID=toAdd['user_schoolID'],
                   user_schoolNAME=toAdd['user_schoolNAME'],stdent_PHONENUM=toAdd['stdent_PHONENUM'],
                   stdent_SCORE=toAdd['stdent_SCORE'],account_TYPE=toAdd['account_TYPE'],admin_EMAILPASS=toAdd['admin_EMAILPASS'],stdent_ABSENT=toAdd['stdent_ABSENT'])
    return
@app.get('/getAllCol')
async def API_getAllCol(col:str):
    return db.getAllCol(col)
@app.get('/meetlinks')
async def API_getMeetLINKS(meet_schoolID):
    '''Example meet_schoolID: 10604083 or "all"'''
    return db.getMeetLINKS(meet_schoolID)
if __name__ == '__main__':
    server.start(3003)
    uvicorn.run(app=app,host='127.0.0.1',port=8000)