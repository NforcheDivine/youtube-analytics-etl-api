import requests
import pandas as pd
import time
from datetime import datetime
import os


class YouTubeDataExtractor:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        self.base_url = "https://www.googleapis.com/youtube/v3"

    def get_channel_stats(self, channel_id):
        """Extract real channel statistics from YouTube API"""
        url = f"{self.base_url}/channels"
        params = {
            'part': 'snippet,statistics',
            'id': channel_id,
            'key': self.api_key
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if 'items' in data and len(data['items']) > 0:
                channel_data = data['items'][0]
                return {
                    'channel_id': channel_id,
                    'title': channel_data['snippet']['title'],
                    'description': channel_data['snippet']['description'],
                    'subscriber_count': int(channel_data['statistics'].get('subscriberCount', 0)),
                    'view_count': int(channel_data['statistics'].get('viewCount', 0)),
                    'video_count': int(channel_data['statistics'].get('videoCount', 0)),
                    'country': channel_data['snippet'].get('country', 'Unknown'),
                    'published_at': channel_data['snippet']['publishedAt'],
                    'extracted_at': datetime.now()
                }
            else:
                print(f"❌ No data found for channel: {channel_id}")
                return None

        except Exception as e:
            print(f"❌ Error extracting channel {channel_id}: {e}")
            return None

    def get_channel_videos(self, channel_id, max_results=10):
        """Extract recent videos from a channel"""
        url = f"{self.base_url}/search"
        params = {
            'part': 'snippet',
            'channelId': channel_id,
            'maxResults': max_results,
            'order': 'date',
            'type': 'video',
            'key': self.api_key
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            videos = []
            if 'items' in data:
                for item in data['items']:
                    video_data = {
                        'video_id': item['id']['videoId'],
                        'channel_id': channel_id,
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'published_at': item['snippet']['publishedAt'],
                        'thumbnail_url': item['snippet']['thumbnails']['default']['url']
                    }
                    videos.append(video_data)

            return videos

        except Exception as e:
            print(f"❌ Error extracting videos for {channel_id}: {e}")
            return []


def extract_data(api_key):
    """Main extraction function with real YouTube API"""
    extractor = YouTubeDataExtractor(api_key)

    # Popular tech channels for demo
    channel_ids = [
        'UC_x5XG1OV2P6uZZ5FSM9Ttw',  # Google Developers
        'UCBJycsmduvYEL83R_U4JriQ',  # Marques Brownlee
        'UCsBjURrPoezykLs9EqgamOA',  # Fireship
        'UC8butISFwT-Wl7EV0hUK0BQ'  # freeCodeCamp
    ]

    all_channels = []
    all_videos = []

    print("📥 Extracting real YouTube data...")

    for channel_id in channel_ids:
        print(f"🔄 Processing channel: {channel_id}")

        # Extract channel data
        channel_data = extractor.get_channel_stats(channel_id)
        if channel_data:
            all_channels.append(channel_data)
            print(f"   ✅ Channel: {channel_data['title']}")

        # Extract video data
        video_data = extractor.get_channel_videos(channel_id, max_results=5)
        all_videos.extend(video_data)
        print(f"   ✅ Videos: {len(video_data)}")

        # Rate limiting - be nice to YouTube API
        time.sleep(1)

    channels_df = pd.DataFrame(all_channels)
    videos_df = pd.DataFrame(all_videos)

    print(f"🎯 Extraction complete: {len(channels_df)} channels, {len(videos_df)} videos")
    return channels_df, videos_df


# For testing without API key
def extract_sample_data():
    """Fallback to sample data if no API key"""
    print("🔧 Using sample data (no API key provided)")

    # Your existing sample data function
    from datetime import datetime

    channels_data = [
        {
            'channel_id': 'UC_x5XG1OV2P6uZZ5FSM9Ttw',
            'title': 'Google Developers',
            'subscriber_count': 2800000,
            'view_count': 950000000,
            'video_count': 4500,
            'extracted_at': datetime.now()
        },
        {
            'channel_id': 'UCBJycsmduvYEL83R_U4JriQ',
            'title': 'Marques Brownlee',
            'subscriber_count': 18000000,
            'view_count': 3500000000,
            'video_count': 1500,
            'extracted_at': datetime.now()
        }
    ]

    videos_data = []
    for i in range(1, 6):
        videos_data.append({
            'video_id': f'video_{i}',
            'channel_id': 'UC_x5XG1OV2P6uZZ5FSM9Ttw',
            'title': f'Sample Video {i}',
            'view_count': 10000 * i,
            'like_count': 500 * i,
            'comment_count': 100 * i,
            'published_at': datetime.now()
        })

    return pd.DataFrame(channels_data), pd.DataFrame(videos_data)