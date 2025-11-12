from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
import pandas as pd
import os
from typing import Optional

# Create FastAPI app
app = FastAPI(
    title="YouTube Analytics API",
    description="REST API for YouTube analytics data pipeline",
    version="1.0.0"
)

# Enable CORS for frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
database_url = "sqlite:///youtube_analytics.db"
engine = create_engine(database_url)


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "YouTube Analytics API is running!",
        "endpoints": {
            "channels": "/channels",
            "videos": "/videos",
            "stats": "/stats",
            "channel_videos": "/channels/{channel_id}/videos"
        }
    }


@app.get("/channels")
async def get_channels(
        limit: int = Query(10, ge=1, le=100),
        sort_by: str = Query("subscriber_count", regex="^(subscriber_count|view_count|video_count)$")
):
    """Get all YouTube channels with pagination and sorting"""
    try:
        query = f"""
        SELECT 
            channel_id, title, subscriber_count, view_count, video_count,
            views_per_video, engagement_ratio, created_at
        FROM youtube_channels 
        ORDER BY {sort_by} DESC
        LIMIT {limit}
        """

        with engine.connect() as conn:
            result = conn.execute(text(query))
            channels = [dict(row) for row in result.mappings()]

        return {
            "count": len(channels),
            "channels": channels
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/channels/{channel_id}")
async def get_channel(channel_id: str):
    """Get specific channel details"""
    try:
        query = "SELECT * FROM youtube_channels WHERE channel_id = :channel_id"

        with engine.connect() as conn:
            result = conn.execute(text(query), {"channel_id": channel_id})
            channel = result.mappings().first()

        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")

        return dict(channel)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/channels/{channel_id}/videos")
async def get_channel_videos(channel_id: str, limit: int = Query(10, ge=1, le=50)):
    """Get videos for a specific channel"""
    try:
        query = """
                SELECT * \
                FROM youtube_videos
                WHERE channel_id = :channel_id
                ORDER BY view_count DESC LIMIT :limit \
                """

        with engine.connect() as conn:
            result = conn.execute(text(query), {"channel_id": channel_id, "limit": limit})
            videos = [dict(row) for row in result.mappings()]

        return {
            "channel_id": channel_id,
            "count": len(videos),
            "videos": videos
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/videos")
async def get_videos(
        limit: int = Query(10, ge=1, le=100),
        min_views: Optional[int] = Query(None, ge=0),
        sort_by: str = Query("view_count", regex="^(view_count|like_count|engagement_rate)$")
):
    """Get videos with filtering and sorting"""
    try:
        where_clause = "WHERE 1=1"
        params = {"limit": limit}

        if min_views is not None:
            where_clause += " AND view_count >= :min_views"
            params["min_views"] = min_views

        query = f"""
        SELECT 
            video_id, channel_id, title, view_count, like_count, 
            comment_count, engagement_rate, published_at
        FROM youtube_videos 
        {where_clause}
        ORDER BY {sort_by} DESC
        LIMIT :limit
        """

        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            videos = [dict(row) for row in result.mappings()]

        return {
            "count": len(videos),
            "videos": videos
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/stats")
async def get_statistics():
    """Get overall statistics about the data"""
    try:
        with engine.connect() as conn:
            # Channel stats
            channel_stats = conn.execute(text("""
                                              SELECT COUNT(*)              as total_channels,
                                                     SUM(subscriber_count) as total_subscribers,
                                                     SUM(view_count)       as total_views,
                                                     AVG(engagement_ratio) as avg_engagement
                                              FROM youtube_channels
                                              """)).mappings().first()

            # Video stats
            video_stats = conn.execute(text("""
                                            SELECT COUNT(*)             as total_videos,
                                                   AVG(view_count)      as avg_views,
                                                   AVG(engagement_rate) as avg_engagement_rate
                                            FROM youtube_videos
                                            """)).mappings().first()

            # Top channel
            top_channel = conn.execute(text("""
                                            SELECT title, subscriber_count
                                            FROM youtube_channels
                                            ORDER BY subscriber_count DESC LIMIT 1
                                            """)).mappings().first()

        return {
            "channel_statistics": dict(channel_stats),
            "video_statistics": dict(video_stats),
            "top_channel": dict(top_channel) if top_channel else None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)