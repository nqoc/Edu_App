import os
from threading import Thread

def serving(PORT):
    content = r'''
Write-Output http://127.0.0.1:{port}
Set-Location {path}
.\Scripts\python.exe -m http.server {port}'''
    with open('server.ps1','w') as file:
        print(content.format(port=PORT,path=os.getcwd()),file=file)
    os.system('server.ps1')
start = (lambda PORT :Thread(target=lambda PORT=PORT:serving(PORT)).start())
if __name__ == '__main__':
    start(3003)