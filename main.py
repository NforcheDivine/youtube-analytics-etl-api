#!/usr/bin/env python3
"""
YouTube Analytics ETL Pipeline - Enhanced with Real API
"""

import os
from scripts.extract import extract_data, extract_sample_data

print("🚀 Starting Enhanced YouTube Data Pipeline...")

try:
    # STEP 1: EXTRACT
    print("\n" + "=" * 50)
    print("STEP 1: EXTRACTING DATA")
    print("=" * 50)

    # Try to use real YouTube API if key is available
    api_key = os.getenv('YOUTUBE_API_KEY')

    if api_key:
        print("🔑 Using YouTube Data API")
        from scripts.extract import extract_data

        channels_df, videos_df = extract_data(api_key)
    else:
        print("🔧 No API key found - using sample data")
        print("💡 Tip: Set YOUTUBE_API_KEY environment variable for real data")
        from scripts.extract import extract_sample_data

        channels_df, videos_df = extract_sample_data()

    # STEP 2: TRANSFORM
    print("\n" + "=" * 50)
    print("STEP 2: TRANSFORMING DATA")
    print("=" * 50)
    from scripts.transform import transform_data

    clean_channels, clean_videos = transform_data(channels_df, videos_df)

    # STEP 3: LOAD
    print("\n" + "=" * 50)
    print("STEP 3: LOADING DATA")
    print("=" * 50)
    from scripts.load import load_data

    success = load_data(clean_channels, clean_videos)

    if success:
        print("\n🎉 ENHANCED PIPELINE COMPLETED SUCCESSFULLY!")
        print("📁 Check the 'data' folder for your output files")
        print("\n📊 SUMMARY:")
        print(f"   - Channels processed: {len(clean_channels)}")
        print(f"   - Videos processed: {len(clean_videos)}")
        print(f"   - Files created: data/channels.csv, data/videos.csv")

        # Show sample of data
        if not clean_channels.empty:
            print(f"\n📈 Sample Channel: {clean_channels.iloc[0]['title']}")
            print(f"   Subscribers: {clean_channels.iloc[0]['subscriber_count']:,}")
            print(f"   Views: {clean_channels.iloc[0]['view_count']:,}")

    else:
        print("\n❌ Pipeline failed!")

except Exception as e:
    print(f"\n💥 Error: {e}")
    print("Please check your setup and try again")

    if success:
        print("\n🎉 ENHANCED PIPELINE COMPLETED SUCCESSFULLY!")
        print("📁 Check the 'data' folder for your output files")
        print("\n📊 SUMMARY:")
        print(f"   - Channels processed: {len(clean_channels)}")
        print(f"   - Videos processed: {len(clean_videos)}")
        print(f"   - Database: youtube_analytics.db")
        print(f"   - CSV files: data/channels.csv, data/videos.csv")

        # API information
        print("\n🌐 REST API READY!")
        print("   To start the API server, run:")
        print("   python run_api.py")
        print("   Then visit: http://localhost:8000/docs")