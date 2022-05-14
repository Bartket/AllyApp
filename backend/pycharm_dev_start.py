import uvicorn
from envs import Env

if __name__ == '__main__':
    uvicorn.run("src.main:app", host=Env.app.APP_HOST, port=Env.app.APP_PORT,
                reload=Env.app.RELOAD)
