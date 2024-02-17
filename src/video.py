import os
from src.channel import Channel
from dotenv import load_dotenv
from config import File_name

load_dotenv(File_name)
key = os.getenv("YOUTUBE_API")


class Video:
    api_key: str = key
    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видио. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        try:
            self.video_info = Channel.get_service().videos().list(part='snippet,statistics', id=self.video_id).execute()
            self.title = self.video_info["items"][0]["snippet"]["title"]
            self.url = f"https://www.youtube.com/watch/{self.video_id}"
            self.view_count = self.video_info["items"][0]["statistics"]["viewCount"]
            self.like_count = self.video_info["items"][0]["statistics"]["likeCount"]
        except IndexError:
            self.video_info = None
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
