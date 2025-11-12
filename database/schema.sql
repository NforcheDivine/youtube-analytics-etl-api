-- Database schema for YouTube Analytics
CREATE TABLE IF NOT EXISTS youtube_channels (
    id SERIAL PRIMARY KEY,
    channel_id VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255),
    subscriber_count INTEGER,
    view_count BIGINT,
    video_count INTEGER,
    views_per_video DECIMAL(10,2),
    engagement_ratio DECIMAL(10,6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS youtube_videos (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(100) UNIQUE NOT NULL,
    channel_id VARCHAR(100),
    title TEXT,
    view_count INTEGER,
    like_count INTEGER,
    comment_count INTEGER,
    engagement_rate DECIMAL(10,6),
    published_at TIMESTAMP,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);