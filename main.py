import os
import uvicorn


from fastapi import FastAPI, File, HTTPException, UploadFile
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



dir_name='data'
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
        
dir_path=os.path.join(os.getcwd(),dir_name)

@app.get('/')
async def index():
    return {"Greetings":"Welcome to the bus video storage api"} 

@app.get("/get_all_bus_videos_list")
async def get_all_bus_videos_list():
    '''
    Fetch all the bus videos
    Returns a list of all the videos. If no video files exist then it returns a null list.
    '''    
    try:
        dir_list=os.listdir(dir_path)
        return dir_list
    except Exception as ex:
        raise HTTPException(status_code=500, detail=ex)


@app.get("/get_bus_video/bus_video_name/{bus_video_name}") #alternative you don't need an endpoint to be speicified at all!
async def get_bus_video(bus_video_name: str):
    '''
    Fetch bus video file by video file name.
    '''    
    dir_list=os.listdir(dir_path)
    file_path_name=os.path.join(dir_path,bus_video_name)
    if bus_video_name in dir_list:
        return FileResponse(file_path_name)
    else:
        raise HTTPException(status_code=404, detail=f'File with given name {bus_video_name} does not exist.')


@app.post("/add_bus_videos/")
async def add_bus_videos(bus_video_file: UploadFile = File(...)):
    '''
    Add bus video file by video file name.
    '''
    file_path_name=os.path.join(dir_path,bus_video_file.filename)

    if "image/" in bus_video_file.content_type:

        with open(file_path_name,'wb+') as f:
            f.write(bus_video_file.file.read())
            f.close()
        return {"success":f"file {bus_video_file.filename} uploaded"}
    else:
        raise HTTPException(status_code=415, detail='Invalid video file type.')

@app.delete("/delete_bus_videos/bus_video_name/{bus_video_name}") #alternative you don't need an endpoint to be speicified at all!
async def delete_bus_videos(bus_video_name: str):
    '''
    Delete bus videos by video file name.
    '''    
    dir_list=os.listdir(dir_path)
    if bus_video_name in dir_list:
        file_path_name=os.path.join(dir_path,bus_video_name)
        try:
            os.remove(file_path_name)
            return {"success":f"File {bus_video_name} deleted."}
        except Exception as ex:
            raise HTTPException(status_code=500, detail=ex)
    else:
        raise HTTPException(status_code=404, detail=f'File with given name {bus_video_name} does not exist.')
