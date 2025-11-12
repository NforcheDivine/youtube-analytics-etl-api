import pandas as pd


def transform_data(channels_df, videos_df):
    """Clean and transform the data"""
    print("🔄 Cleaning and transforming data...")

    # Clean channels data
    channels_clean = channels_df.copy()
    channels_clean['subscriber_count'] = pd.to_numeric(channels_clean['subscriber_count'], errors='coerce')
    channels_clean['view_count'] = pd.to_numeric(channels_clean['view_count'], errors='coerce')
    channels_clean['video_count'] = pd.to_numeric(channels_clean['video_count'], errors='coerce')

    # Calculate additional metrics
    channels_clean['views_per_video'] = channels_clean['view_count'] / channels_clean['video_count']
    channels_clean['engagement_ratio'] = channels_clean['subscriber_count'] / channels_clean['view_count']

    # Clean videos data
    videos_clean = videos_df.copy()
    videos_clean['view_count'] = pd.to_numeric(videos_clean['view_count'], errors='coerce')
    videos_clean['like_count'] = pd.to_numeric(videos_clean['like_count'], errors='coerce')
    videos_clean['comment_count'] = pd.to_numeric(videos_clean['comment_count'], errors='coerce')

    # Calculate video engagement
    videos_clean['engagement_rate'] = (videos_clean['like_count'] + videos_clean['comment_count']) / videos_clean[
        'view_count']

    print(f"✅ Transformed {len(channels_clean)} channels and {len(videos_clean)} videos")
    return channels_clean, videos_clean


# Test function
if __name__ == "__main__":
    # This will be used when we test the full pipeline
    pass