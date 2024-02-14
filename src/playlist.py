import datetime
import os
import isodate
from src.channel import Channel
from dotenv import load_dotenv
from config import File_name

load_dotenv(File_name)
key = os.getenv("YOUTUBE_API")


class PlayList:
    api_key: str = key

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.playlists = Channel.get_service().playlists().list(id=playlist_id,
                                                                part='contentDetails,snippet',
                                                                maxResults=50,
                                                                ).execute()
        self.playlist_videos = Channel.get_service().playlistItems().list(playlistId=playlist_id,
                                                                          part='contentDetails',
                                                                          maxResults=50,
                                                                          ).execute()
        self.title = self.playlists["items"][0]["snippet"]["title"]
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = Channel.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                  id=self.video_ids).execute()

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration

    def show_best_video(self):
        max_like = 0
        max_video = None
        for video in self.video_response['items']:
            like_count = video["statistics"]["likeCount"]
            if int(like_count) > int(max_like):
                max_like = like_count
                max_video = video["id"]
        return f"https://youtu.be/{max_video}"


