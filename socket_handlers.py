from fastapi import FastAPI
from fastapi_socketio import SocketManager
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

# terminalin arkaplan renkerlini ayarlayan ANSI kodları
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


app = FastAPI()

 
sio = SocketManager(app=app)
yukseltme2Sayi = 0  
yukseltme1Sayi = 0  


@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.sio.on('join')
async def handle_join(sid, *args, **kwargs):
    print("Bağlantı gerçekleşti...")
    await sio.emit('lobby', 'User joined')

@sio.on('2x2determinant')
async def test(sid,*args, **kwargs):
    sayılar = args[0]
    print(sayılar)
    print (np.linalg.det(sayılar).round(2))
    await sio.emit('2x2determinant', np.linalg.det(sayılar).round(2))

@sio.on('3x3determinant')
async def test(sid,*args, **kwargs):
    sayılar = args[0]
    print(sayılar)
    print (np.linalg.det(sayılar).round(2))
    await sio.emit('3x3determinant', np.linalg.det(sayılar).round(2))

@sio.on('4x4determinant')
async def test(sid,*args, **kwargs):
    sayılar = args[0]
    print(sayılar)
    print (np.linalg.det(sayılar).round(2))
    await sio.emit('4x4determinant', np.linalg.det(sayılar).round(2))

@sio.on('random')
async def test(sid,*args, **kwargs):
    print("gelen sayı: ", args[0])
    randomSayi = np.random.randint(1,args[0])
    print(randomSayi)
    await sio.emit('random', randomSayi)
    




if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout)
    
    import uvicorn

    uvicorn.run("socket_handlers:app", host='127.0.0.1', port=8081, reload=True)