from fastapi import FastAPI, HTTPException
from fastapi_socketio import SocketManager
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from typing import List, Union, Dict
import logging
from dataclasses import dataclass

# Configuration
@dataclass
class Config:
    HOST: str = '127.0.0.1'
    PORT: int = 8081
    LOG_LEVEL: str = 'INFO'
    ROUND_DIGITS: int = 2

# Terminal colors
class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Matrix operations handler
class MatrixOperations:
    @staticmethod
    def validate_matrix(matrix: List[List[float]], expected_size: int) -> bool:
        try:
            arr = np.array(matrix, dtype=np.float64)
            return arr.shape == (expected_size, expected_size)
        except:
            return False

    @staticmethod
    def calculate_determinant(matrix: List[List[float]], size: int) -> float:
        """Calculate matrix determinant with validation"""
        if not MatrixOperations.validate_matrix(matrix, size):
            raise ValueError(f"Invalid {size}x{size} matrix")
        
        try:
            # Convert to float64 for better precision
            arr = np.array(matrix, dtype=np.float64)
            result = np.linalg.det(arr).round(Config.ROUND_DIGITS)
            return float(result)
        except np.linalg.LinAlgError:
            raise ValueError("Matrix is singular")

# Initialize FastAPI app
app = FastAPI()
logger = logging.getLogger(__name__)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket manager
sio = SocketManager(app=app)
matrix_ops = MatrixOperations()

# Route handlers
@app.get("/")
async def main() -> Dict[str, str]:
    return {"message": "Matrix Calculator API"}

# WebSocket handlers
@sio.on('connect')
async def handle_connect(sid: str, environ: dict, *args, **kwargs) -> None:
    logger.info(f"New connection: {sid}")
    await sio.emit('lobby', 'User joined', room=sid)

@sio.on('2x2determinant')
async def handle_2x2determinant(sid: str, *args, **kwargs) -> None:
    try:
        result = matrix_ops.calculate_determinant(args[0], 2)
        logger.debug(f"2x2 det result: {result}")
        await sio.emit('2x2determinant', result, room=sid)
    except Exception as e:
        logger.error(f"Error in 2x2 det: {e}")
        await sio.emit('error', str(e), room=sid)

@sio.on('3x3determinant')
async def handle_3x3determinant(sid: str, *args, **kwargs) -> None:
    try:
        result = matrix_ops.calculate_determinant(args[0], 3)
        logger.debug(f"3x3 det result: {result}")
        await sio.emit('3x3determinant', result, room=sid)
    except Exception as e:
        logger.error(f"Error in 3x3 det: {e}")
        await sio.emit('error', str(e), room=sid)

@sio.on('4x4determinant')
async def handle_4x4determinant(sid: str, *args, **kwargs) -> None:
    try:
        result = matrix_ops.calculate_determinant(args[0], 4)
        logger.debug(f"4x4 det result: {result}")
        await sio.emit('4x4determinant', result, room=sid)
    except Exception as e:
        logger.error(f"Error in 4x4 det: {e}")
        await sio.emit('error', str(e), room=sid)

@sio.on('random')
async def handle_random(sid: str, *args, **kwargs) -> None:
    try:
        max_val = int(args[0])
        if max_val < 2:
            raise ValueError("Maximum value must be greater than 1")
        
        # Use numpy's faster random number generator
        random_num = np.random.default_rng().integers(1, max_val)
        logger.debug(f"Random number generated: {random_num}")
        await sio.emit('random', int(random_num), room=sid)
    except Exception as e:
        logger.error(f"Error generating random number: {e}")
        await sio.emit('error', str(e), room=sid)

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    import uvicorn
    uvicorn.run(
        "main:app", 
        host=Config.HOST, 
        port=Config.PORT, 
        reload=True,
        log_level=Config.LOG_LEVEL.lower()
    )