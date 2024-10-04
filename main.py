import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

class Item(BaseModel):
    youtubeCode: str

app = FastAPI()

ydl_opts = {}

def download_transcriptions(video_id):
    return YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])


def download(youtubeCode):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        URL = f'https://www.youtube.com/watch?v={youtubeCode}'
        info = ydl.extract_info(URL, download=False)
        info['subtitles'] = download_transcriptions(youtubeCode)

        return ydl.sanitize_info(info)


@app.post("/download")
async def create_item(item: Item):
    print(item)
    return download(item.youtubeCode)

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()