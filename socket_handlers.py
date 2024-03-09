from fastapi import FastAPI
from fastapi_socketio import SocketManager
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

# terminalin arkaplan renklerini ayarlayan ANSI kodları
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

# CORS politikalarını belirleme
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm kaynaklardan gelen isteklere izin ver
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metodlarına izin ver
    allow_headers=["*"],  # Tüm HTTP başlıklarına izin ver
)

# SocketManager oluşturma
sio = SocketManager(app=app)

# Ana sayfa
@app.get("/")
async def main():
    return {"message": "Hello World"}

# WebSocket bağlantı işlemleri
@sio.on('connect')
async def handle_connect(sid, environ, *args, **kwargs):
    print("Bağlantı gerçekleşti...")
    await sio.emit('lobby', 'User joined', room=sid)

# 2x2 determinant hesaplama işlemi
@sio.on('2x2determinant')
async def handle_2x2determinant(sid, *args, **kwargs):
    sayilar = args[0]
    print(sayilar)
    result = np.linalg.det(sayilar).round(2)
    print(result)
    await sio.emit('2x2determinant', result, room=sid)

# 3x3 determinant hesaplama işlemi
@sio.on('3x3determinant')
async def handle_3x3determinant(sid, *args, **kwargs):
    sayilar = args[0]
    print(sayilar)
    result = np.linalg.det(sayilar).round(2)
    print(result)
    await sio.emit('3x3determinant', result, room=sid)

# 4x4 determinant hesaplama işlemi
@sio.on('4x4determinant')
async def handle_4x4determinant(sid, *args, **kwargs):
    sayilar = args[0]
    print(sayilar)
    result = np.linalg.det(sayilar).round(2)
    print(result)
    await sio.emit('4x4determinant', result, room=sid)

# Rastgele sayı üretme işlemi
@sio.on('random')
async def handle_random(sid, *args, **kwargs):
    print("Gelen sayı:", args[0])
    random_sayi = np.random.randint(1, args[0])
    print(random_sayi)
    await sio.emit('random', random_sayi, room=sid)

if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout)
    
    import uvicorn

    uvicorn.run("socket_handlers:app", host='127.0.0.1', port=8081, reload=True)
