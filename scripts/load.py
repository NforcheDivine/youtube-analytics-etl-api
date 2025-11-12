import pandas as pd
import os
from sqlalchemy import create_engine, text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self):
        # SQLite database file (no installation needed)
        self.database_url = "sqlite:///youtube_analytics.db"
        self.engine = create_engine(self.database_url)

    def initialize_database(self):
        """Create database tables"""
        try:
            with open('database/schema.sql', 'r') as f:
                schema_sql = f.read()

            with self.engine.connect() as conn:
                # SQLite doesn't support some PostgreSQL syntax, so let's adapt
                conn.execute(text("""
                                  CREATE TABLE IF NOT EXISTS youtube_channels
                                  (
                                      id
                                      INTEGER
                                      PRIMARY
                                      KEY
                                      AUTOINCREMENT,
                                      channel_id
                                      VARCHAR
                                  (
                                      100
                                  ) UNIQUE NOT NULL,
                                      title VARCHAR
                                  (
                                      255
                                  ),
                                      subscriber_count INTEGER,
                                      view_count BIGINT,
                                      video_count INTEGER,
                                      views_per_video DECIMAL
                                  (
                                      10,
                                      2
                                  ),
                                      engagement_ratio DECIMAL
                                  (
                                      10,
                                      6
                                  ),
                                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                      )
                                  """))
                conn.execute(text("""
                                  CREATE TABLE IF NOT EXISTS youtube_videos
                                  (
                                      id
                                      INTEGER
                                      PRIMARY
                                      KEY
                                      AUTOINCREMENT,
                                      video_id
                                      VARCHAR
                                  (
                                      100
                                  ) UNIQUE NOT NULL,
                                      channel_id VARCHAR
                                  (
                                      100
                                  ),
                                      title TEXT,
                                      view_count INTEGER,
                                      like_count INTEGER,
                                      comment_count INTEGER,
                                      engagement_rate DECIMAL
                                  (
                                      10,
                                      6
                                  ),
                                      published_at TIMESTAMP,
                                      processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                      )
                                  """))
                conn.commit()

            logger.info("✅ Database tables created successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Database setup error: {e}")
            return False

    def load_to_database(self, channels_df, videos_df):
        """Load data to SQLite database"""
        logger.info("🗄️ Loading data to SQLite database...")

        try:
            # Initialize database first
            self.initialize_database()

            # Load channels
            channels_df.to_sql(
                'youtube_channels',
                self.engine,
                if_exists='replace',
                index=False
            )

            # Load videos
            videos_df.to_sql(
                'youtube_videos',
                self.engine,
                if_exists='replace',
                index=False
            )

            # Verify data loaded
            with self.engine.connect() as conn:
                channel_count = conn.execute(text("SELECT COUNT(*) FROM youtube_channels")).scalar()
                video_count = conn.execute(text("SELECT COUNT(*) FROM youtube_videos")).scalar()

            logger.info(f"✅ Database load successful: {channel_count} channels, {video_count} videos")
            logger.info("💾 Database file: youtube_analytics.db")
            return True

        except Exception as e:
            logger.error(f"❌ Database error: {e}")
            return False

    def load_to_csv(self, channels_df, videos_df):
        """Fallback to CSV files"""
        logger.info("💾 Saving backup CSV files...")
        os.makedirs('data', exist_ok=True)
        channels_df.to_csv('data/channels.csv', index=False)
        videos_df.to_csv('data/videos.csv', index=False)
        logger.info("✅ Data saved to CSV files")
        return True

    def load_data(self, channels_df, videos_df):
        """Main loading function - tries database first, then CSV"""
        logger.info("🔄 Attempting to load to database...")
        db_success = self.load_to_database(channels_df, videos_df)

        # Always create CSV backup
        self.load_to_csv(channels_df, videos_df)

        return db_success


# For backward compatibility
def load_data(channels_df, videos_df):
    loader = DataLoader()
    return loader.load_data(channels_df, videos_df)