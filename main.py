import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static
import google.generativeai as genai
from datetime import datetime, timedelta
import random
import json
import requests
from geopy.geocoders import Nominatim
from typing import Tuple, Dict, Optional
import logging
from streamlit_extras.colored_header import colored_header
from streamlit_extras.app_logo import add_logo
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import tweepy
from tweepy.errors import TweepyException
from typing import List, Dict
import os
from PIL import Image
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import isodate
from datetime import datetime, timedelta
from streamlit_folium import st_folium
import folium.plugins

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config with enhanced styling
st.set_page_config(
    page_title="Team_Nexus Disaster Predictor",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/gamerson96/Team_NEXUS',
        'Report a bug': "https://github.com/gamerson96/Team_NEXUS",
        'About': "Enhanced Disaster AI Predictor v2.0 .It is Developed and created by Team_Nexus"
    }
)

# Custom CSS
st.markdown("""
    <style>
    .homepage-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(to right, #1e3c72, #2a5298);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .results-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
    }
    .stButton>button {
    width: 100%;
    border-radius: 25px;
    height: 3em;
    font-weight: bold;
    background-color: #4682b4;
    color: white;
    }
    .sidebar .sidebar-content {
        background-color: #f5f5f5;
    }
    .disaster-card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .st-emotion-cache-1y4p8pa {
        max-width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Load API keys from environment variables or Streamlit secrets
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]
    EMAIL_ADDRESS = st.secrets["EMAIL_ADDRESS"]
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
    TWITTER_API_KEY = st.secrets["TWITTER_API_KEY"]
    TWITTER_API_SECRET = st.secrets["TWITTER_API_SECRET"]
    TWITTER_ACCESS_TOKEN = st.secrets["TWITTER_ACCESS_TOKEN"]
    TWITTER_ACCESS_TOKEN_SECRET = st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
    YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
except Exception as e:
    logger.warning(f"Failed to load API keys from secrets: {e}")
    GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY'
    OPENWEATHER_API_KEY = 'YOUR_OPENWEATHER_API_KEY'
    EMAIL_ADDRESS = 'YOUR_EMAIL'
    EMAIL_PASSWORD = 'YOUR_PASSWORD'

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Set up Twitter API client
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

# Enhanced disaster types with more metadata
DISASTER_TYPES: Dict[str, Dict[str, any]] = {
    "Flood": {
        "color": "blue",
        "icon": "🌊",
        "base_severity": 5,
        "emergency_numbers": {
            "US": "1-800-525-0321",
            "UK": "999",
            "Global": "+1-202-501-4444"
        },
        "alert_levels": ["Advisory", "Watch", "Warning"]
    },
    "Earthquake": {
        "color": "red",
        "icon": "🌋",
        "base_severity": 7,
        "emergency_numbers": {
            "US": "1-800-525-0321",
            "UK": "999",
            "Global": "+1-202-501-4444"
        },
        "alert_levels": ["Minor", "Moderate", "Major"]
    },
    "Wildfire": {
        "color": "orange",
        "icon": "🔥",
        "base_severity": 6,
        "emergency_numbers": {
            "US": "911",
            "UK": "999",
            "Global": "+1-202-501-4444"
        },
        "alert_levels": ["Low", "Moderate", "Extreme"]
    },
    "Hurricane": {
        "color": "purple",
        "icon": "🌀",
        "base_severity": 8,
        "emergency_numbers": {
            "US": "1-800-621-FEMA",
            "UK": "999",
            "Global": "+1-202-501-4444"
        },
        "alert_levels": ["Category 1", "Category 3", "Category 5"]
    },
    "Tsunami": {
        "color": "teal",
        "icon": "🌊",
        "base_severity": 9,
        "emergency_numbers": {
            "US": "1-800-525-0321",
            "UK": "999",
            "Global": "+1-202-501-4444"
        },
        "alert_levels": ["Advisory", "Watch", "Warning"]
    }
}

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import isodate
from datetime import datetime, timedelta

class YouTubeService:
    """Service class to handle YouTube API operations"""
    def __init__(self, api_key: str):
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def fetch_disaster_videos(
        self, 
        disaster_type: str, 
        location: str, 
        max_results: int = 5
    ) -> List[Dict]:
        """
        Fetch relevant YouTube videos about the disaster and location.

        Args:
            disaster_type: Type of disaster (e.g., "Flood", "Earthquake")
            location: Location name
            max_results: Maximum number of videos to return

        Returns:
            List of dictionaries containing video information
        """
        try:
            # Construct the search query
            query = f"{disaster_type} {location} disaster"

            # Execute the search request
            search_response = self.youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=max_results,
                type='video',
                order='relevance',
                safeSearch='strict',
                relevanceLanguage='en'
            ).execute()

            # Get video IDs for fetching additional details
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]

            if not video_ids:
                return []

            # Get detailed video information
            videos_response = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            ).execute()

            # Format the video information
            formatted_videos = []
            for video in videos_response.get('items', []):
                # Convert duration from ISO 8601 format
                duration = isodate.parse_duration(video['contentDetails']['duration'])
                duration_str = str(duration).split('.')[0]  # Remove microseconds

                formatted_videos.append({
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'thumbnail_url': video['snippet']['thumbnails']['high']['url'],
                    'video_id': video['id'],
                    'channel_title': video['snippet']['channelTitle'],
                    'published_at': video['snippet']['publishedAt'],
                    'view_count': video['statistics'].get('viewCount', '0'),
                    'duration': duration_str,
                    'url': f"https://www.youtube.com/watch?v={video['id']}"
                })

            return formatted_videos

        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching YouTube videos: {e}")
            return []

def display_youtube_section(videos: List[Dict]):
    """Display YouTube videos in a formatted grid"""
    if not videos:
        st.info("No relevant videos found for this disaster and location.")
        return

    st.markdown("### 📺 Related Videos")

    # Create rows of videos (2 videos per row)
    for i in range(0, len(videos), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(videos):
                video = videos[i + j]
                with col:
                    st.markdown(
                        f"""
                        <div style="
                            border: 1px solid #ddd;
                            border-radius: 10px;
                            padding: 15px;
                            margin-bottom: 15px;
                            background-color: white;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1)
                        ">
                            <a href="{video['url']}" target="_blank">
                                <img src="{video['thumbnail_url']}" style="width: 100%; border-radius: 5px;">
                            </a>
                            <h4>{video['title']}</h4>
                            <p><strong>{video['channel_title']}</strong></p>
                            <p>Duration: {video['duration']} | Views: {int(video['view_count']):,}</p>
                            <a href="{video['url']}" target="_blank" style="
                                display: inline-block;
                                padding: 5px 10px;
                                background-color: #ff0000;
                                color: white;
                                text-decoration: none;
                                border-radius: 5px;
                                margin-top: 10px;
                            ">Watch on YouTube</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

class NewsService:
    """Service class to handle news-related operations"""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"

    def fetch_disaster_news(
        self, 
        disaster_type: str, 
        location: str, 
        days: int = 7,
        max_articles: int = 5
    ) -> List[Dict]:
        """
        Fetch news articles related to the disaster type and location.

        Args:
            disaster_type: Type of disaster (e.g., "Flood", "Earthquake")
            location: Location name
            days: Number of days to look back for news
            max_articles: Maximum number of articles to return

        Returns:
            List of dictionaries containing news articles
        """
        try:
            # Calculate the date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Construct the query
            query = f"{disaster_type} {location}"

            # Make the API request
            params = {
                'q': query,
                'from': start_date.strftime('%Y-%m-%d'),
                'to': end_date.strftime('%Y-%m-%d'),
                'sortBy': 'relevancy',
                'language': 'en',
                'apiKey': self.api_key
            }

            response = requests.get(self.base_url, params=params)
            response.raise_for_status()

            # Process the response
            news_data = response.json()
            articles = news_data.get('articles', [])

            # Format and return the articles
            formatted_articles = []
            for article in articles[:max_articles]:
                formatted_articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'published_at': article.get('publishedAt', ''),
                    'image_url': article.get('urlToImage', '')
                })

            return formatted_articles

        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []

def display_news_section(news_articles: List[Dict]):
    """Display news articles in a formatted way"""
    st.markdown("### 📰 Latest News Coverage")

    if not news_articles:
        st.info("No recent news articles found for this disaster and location.")
        return

    for article in news_articles:
        with st.container():
            st.markdown(
                f"""
                <div style="
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 15px;
                    background-color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1)
                ">
                    <h4>{article['title']}</h4>
                    <p><em>Source: {article['source']} | Published: {article['published_at']}</em></p>
                    <p>{article['description']}</p>
                    <a href="{article['url']}" target="_blank">Read more</a>
                </div>
                """,
                unsafe_allow_html=True
            )

class AlertService:
    def __init__(self, email_address: str, email_password: str):
        self.email_address = email_address
        self.email_password = email_password

    def send_alert(self, recipient: str, disaster_type: str, severity: float, location: str) -> Tuple[bool, str]:
        try:
            if not self._validate_email(recipient):
                return False, "Invalid email format"

            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = recipient
            msg['Subject'] = f"URGENT: {disaster_type} Alert for {location}"

            alert_level = self._get_alert_level(disaster_type, severity)
            body = self._create_alert_message(disaster_type, severity, location, alert_level)
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            return True, "Alert sent successfully"
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP Authentication failed")
            return False, "Email authentication failed. Please check your email and password."
        except Exception as e:
            logger.error(f"Failed to send alert: {e}")
            return False, f"Alert system error: {str(e)}"

    def _validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def _get_alert_level(self, disaster_type: str, severity: float) -> str:
        alert_levels = DISASTER_TYPES[disaster_type]["alert_levels"]
        if severity < 4:
            return alert_levels[0]
        elif severity < 7:
            return alert_levels[1]
        else:
            return alert_levels[2]

    def _create_alert_message(self, disaster_type: str, severity: float, location: str, alert_level: str) -> str:
        emergency_numbers = DISASTER_TYPES[disaster_type]["emergency_numbers"]
        message = f"""
EMERGENCY ALERT: {disaster_type} {alert_level}

Location: {location}
Severity Level: {severity:.1f}/10
Alert Level: {alert_level}

Emergency Contact Numbers:
USA: {emergency_numbers['US']}
UK: {emergency_numbers['UK']}
International: {emergency_numbers['Global']}

Safety Instructions:
{self._get_safety_instructions(disaster_type)}

Please follow local authority instructions and stay safe.
        """
        return message

    def _get_safety_instructions(self, disaster_type: str) -> str:
        instructions = {
            "Flood": "1. Move to higher ground\n2. Avoid walking through floodwater\n3. Follow evacuation orders",
            "Earthquake": "1. Drop, Cover, and Hold On\n2. Stay away from windows\n3. Be prepared for aftershocks",
            "Wildfire": "1. Evacuate immediately if ordered\n2. Keep emergency supplies ready\n3. Follow evacuation routes",
            "Hurricane": "1. Stay indoors\n2. Keep away from windows\n3. Have emergency supplies ready",
            "Tsunami": "1. Move inland immediately\n2. Get to high ground\n3. Wait for all-clear signal"
        }
        return instructions.get(disaster_type, "Follow local authority instructions")

def simulate_disaster_data(
    disaster_type: str,
    duration_hours: int,
    initial_intensity: float,
    coordinates: Tuple[float, float]
) -> pd.DataFrame:
    """Simulate disaster data over time with realistic progression."""
    timestamps = pd.date_range(
        start=datetime.now(),
        periods=duration_hours,
        freq='H'
    )

    base_severity = DISASTER_TYPES[disaster_type]["base_severity"]
    severity = [initial_intensity]

    for i in range(1, duration_hours):
        change = np.random.normal(0, 0.5)
        cyclical = np.sin(i * np.pi / 12) * 0.3

        new_severity = severity[-1] + change + cyclical
        new_severity = max(1, min(10, new_severity))
        severity.append(new_severity)

    data = pd.DataFrame({
        'timestamp': timestamps,
        'severity': severity,
        'latitude': coordinates[0],
        'longitude': coordinates[1]
    })

    return data

def get_coordinates(location_name: str) -> Tuple[float, float]:
    """Get coordinates for a given location using Nominatim."""
    try:
        geolocator = Nominatim(user_agent="disaster_predictor")
        location = geolocator.geocode(location_name)
        if location:
            return (location.latitude, location.longitude)
        else:
            return (34.0522, -118.2437)  # Default to LA
    except Exception as e:
        logger.error(f"Error getting coordinates: {e}")
        return (34.0522, -118.2437)

def fetch_disaster_tweets(disaster_type: str, location: str, count: int = 5) -> List[Dict]:
    """
    Fetch recent tweets related to the disaster type and location.
    """
    query = f"{disaster_type} {location}"
    tweets = []

    try:
        for tweet in tweepy.Cursor(twitter_api.search_tweets, q=query, tweet_mode="extended").items(count):
            tweets.append({
                "text": tweet.full_text,
                "created_at": tweet.created_at,
                "user": tweet.user.screen_name
            })
    except TweepyException as e:
        logger.error(f"Error fetching tweets: {e}")
        # Add some mock tweets as a fallback
        tweets = [
            {"text": f"Stay safe during the {disaster_type} in {location}! Follow official guidelines.", "created_at": datetime.now(), "user": "EmergencyAlert"},
            {"text": f"Latest update on the {disaster_type} situation in {location}. Authorities are responding.", "created_at": datetime.now() - timedelta(hours=1), "user": "NewsUpdate"},
            {"text": f"Community coming together to support those affected by the {disaster_type} in {location}.", "created_at": datetime.now() - timedelta(hours=2), "user": "CommunityHelp"}
        ]

    return tweets

def display_disaster_news(disaster_type: str, location: str):
    """Display recent tweets or mock news related to the disaster."""
    st.markdown("### 📰 Recent News and Updates")

    tweets = fetch_disaster_tweets(disaster_type, location)

    if tweets:
        for tweet in tweets:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px; background-color: #f9f9f9;">
                <p><strong>@{tweet['user']}</strong> - {tweet['created_at'].strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>{tweet['text']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent tweets found for this disaster and location. Please check your internet connection or try again later.")

def display_send_alert_section(disaster_type: str, intensity: float, location_name: str):
    st.markdown("""
    <style>
    .send-alert-container {
        background-color: #f0f8ff;
        border: 0px solid #4682b4;
        border-radius: 0px;
        padding: 1px;
        margin-top: 10px;
    }
    .send-alert-header {
        color: #4682b4;
        font-size: 24px;
        margin-bottom: 15px;
    }
    .send-alert-button {
        background-color: #4682b4;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="send-alert-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="send-alert-header">📢 Send Alert</h3>', unsafe_allow_html=True)

    recipient_email = st.text_input("Enter recipient email:", key="alert_email")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Disaster Type:** {disaster_type}")
        st.markdown(f"**Intensity:** {intensity:.1f}/10")
        st.markdown(f"**Location:** {location_name}")

    with col2:
        if st.button("Send Alert", key="send_alert", help="Click to send an alert email"):
            if recipient_email:
                alert_service = AlertService(st.secrets["EMAIL_ADDRESS"], st.secrets["EMAIL_PASSWORD"])
                success, message = alert_service.send_alert(recipient_email, disaster_type, intensity, location_name)
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.warning("Please enter a recipient email address.")

    st.markdown('</div>', unsafe_allow_html=True)

def get_weather_data(coordinates: Tuple[float, float]) -> Dict:
    """Get current weather data for the location."""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={coordinates[0]}&lon={coordinates[1]}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        logger.error(f"Error getting weather data: {e}")
        return {}

def create_enhanced_map(data: pd.DataFrame, disaster_type: str, location_name: str) -> None:
    """
    Create and display an enhanced interactive map with improved stability and error handling.
    """
    try:
        # Create the map container with error handling
        with st.container():
            col1, col2 = st.columns([1.2, 3])

            with col1:
                # Control panel
                st.markdown("### 🗺️ Map Controls")
                show_historic = st.checkbox("Show Historic Events", value=True)
                show_facilities = st.checkbox("Show Emergency Facilities", value=True)
                show_impact_zones = st.checkbox("Show Impact Zones", value=True)

                map_style = st.selectbox(
                    "Map Style",
                    ["Default", "Satellite", "OpenStreetMap"],
                    index=0
                )

                # Quick metrics with error handling
                try:
                    st.markdown("### 📊 Quick Metrics")
                    current_severity = data['severity'].iloc[-1] if not data.empty else 0
                    initial_severity = data['severity'].iloc[0] if not data.empty else 0
                    st.metric(
                        "Current Severity",
                        f"{current_severity:.1f}/10",
                        delta=f"{current_severity - initial_severity:.1f}"
                    )
                except Exception as e:
                    st.warning("Unable to display metrics. Please check your data.")
                    logger.error(f"Metrics error: {e}")

            with col2:
                try:
                    # Initialize map with fallback coordinates
                    default_lat = data['latitude'].iloc[0] if not data.empty else 34.0522
                    default_lon = data['longitude'].iloc[0] if not data.empty else -118.2437

                    # Set up base maps with error handling
                    base_maps = {
                        "Default": "cartodbpositron",
                        "Satellite": "CartoDB.DarkMatter",  # Changed to more stable tile
                        "OpenStreetMap": "OpenStreetMap"
                    }

                    # Create the map with safe defaults
                    m = folium.Map(
                        location=[default_lat, default_lon],
                        zoom_start=10,
                        tiles=base_maps.get(map_style, "cartodbpositron")
                    )

                    # Add main marker with safe data access
                    latest_severity = data['severity'].iloc[-1] if not data.empty else 5.0
                    color = DISASTER_TYPES.get(disaster_type, {}).get("color", "blue")

                    folium.Marker(
                        location=[default_lat, default_lon],
                        popup=folium.Popup(
                            f"""
                            <div style='width: 200px'>
                                <h4>{disaster_type} Event</h4>
                                <p><b>Location:</b> {location_name}</p>
                                <p><b>Severity:</b> {latest_severity:.1f}/10</p>
                                <p><b>Status:</b> {get_status_text(latest_severity)}</p>
                            </div>
                            """,
                            max_width=200
                        ),
                        icon=folium.Icon(color=get_severity_color(latest_severity), icon='info-sign')
                    ).add_to(m)

                    # Add optional layers with safety checks
                    if show_impact_zones:
                        try:
                            base_radius = {
                                "Flood": 5000,
                                "Earthquake": 10000,
                                "Wildfire": 3000,
                                "Hurricane": 15000,
                                "Tsunami": 8000
                            }.get(disaster_type, 5000)

                            impact_radius = base_radius * (latest_severity / 5)

                            folium.Circle(
                                location=[default_lat, default_lon],
                                radius=impact_radius,
                                color=color,
                                fill=True,
                                fillOpacity=0.2,
                                popup=f"Impact Zone - {impact_radius/1000:.1f} km radius"
                            ).add_to(m)
                        except Exception as e:
                            logger.error(f"Impact zone error: {e}")

                    # Add historic events with safety checks
                    if show_historic:
                        try:
                            historic_group = folium.FeatureGroup(name='Historic Events')
                            historic_events = generate_historic_events(disaster_type, default_lat, default_lon)

                            for event in historic_events:
                                folium.CircleMarker(
                                    location=[event['lat'], event['lon']],
                                    radius=5,
                                    color='gray',
                                    fill=True,
                                    popup=f"Historic {disaster_type}<br>Date: {event['date']}<br>Severity: {event['severity']}/10"
                                ).add_to(historic_group)

                            historic_group.add_to(m)
                        except Exception as e:
                            logger.error(f"Historic events error: {e}")

                    # Add facilities with safety checks
                    if show_facilities:
                        try:
                            facilities_group = folium.FeatureGroup(name='Emergency Facilities')
                            facilities = generate_emergency_facilities(default_lat, default_lon)

                            for facility in facilities:
                                folium.Marker(
                                    location=[facility['lat'], facility['lon']],
                                    popup=f"{facility['name']}<br>{facility['type']}<br>{facility['contact']}",
                                    icon=folium.Icon(color='lightgray', icon=facility['icon'])
                                ).add_to(facilities_group)

                            facilities_group.add_to(m)
                        except Exception as e:
                            logger.error(f"Facilities error: {e}")

                    # Add legend with safety check
                    try:
                        add_minimal_legend(m, disaster_type, latest_severity)
                    except Exception as e:
                        logger.error(f"Legend error: {e}")

                    # Render map with error handling and timeout
                    try:
                        st_folium(m, width=800, height=500, returned_objects=[])
                    except Exception as e:
                        st.error("Unable to display map. Please try refreshing the page.")
                        logger.error(f"Map rendering error: {e}")

                except Exception as e:
                    st.error("Error initializing map. Please check your data and try again.")
                    logger.error(f"Map initialization error: {e}")

    except Exception as e:
        st.error("An unexpected error occurred while creating the map.")
        logger.error(f"Overall map creation error: {e}")

def add_minimal_legend(m: folium.Map, disaster_type: str, severity: float):
    """Add a minimal legend to the map"""
    legend_html = f"""
        <div style="
            position: fixed; 
            bottom: 50px; 
            right: 50px; 
            width: auto;
            background-color: white;
            border: 1px solid grey;
            padding: 6px;
            font-size: 12px;
            border-radius: 4px;
            ">
            <p style="margin: 0"><b>{disaster_type}</b> | Severity: {severity:.1f}/10</p>
        </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

# Helper functions remain the same as in the previous version
def get_severity_color(severity: float) -> str:
    """Get color based on severity level"""
    if severity <= 3:
        return 'green'
    elif severity <= 6:
        return 'orange'
    else:
        return 'red'

def get_status_text(severity: float) -> str:
    """Get status text based on severity level"""
    if severity <= 3:
        return 'Monitoring'
    elif severity <= 6:
        return 'Warning'
    else:
        return 'Critical'

def generate_historic_events(disaster_type: str, center_lat: float, center_lon: float) -> List[Dict]:
    """Generate simulated historic disaster events"""
    events = []
    for _ in range(3):  # Reduced to 3 historic events
        lat_offset = random.uniform(-0.05, 0.05)
        lon_offset = random.uniform(-0.05, 0.05)
        days_ago = random.randint(1, 1825)
        event_date = datetime.now() - timedelta(days=days_ago)

        events.append({
            'lat': center_lat + lat_offset,
            'lon': center_lon + lon_offset,
            'date': event_date.strftime('%Y-%m-%d'),
            'severity': round(random.uniform(3, 9), 1)
        })

    return events

def generate_emergency_facilities(center_lat: float, center_lon: float) -> List[Dict]:
    """Generate simulated emergency facilities"""
    facilities = []
    facility_types = [
        {'name': 'Hospital', 'icon': 'plus', 'type': 'Medical'},
        {'name': 'Fire Station', 'icon': 'fire-extinguisher', 'type': 'Fire Response'},
        {'name': 'Evacuation Center', 'icon': 'home', 'type': 'Shelter'}
    ]

    for facility in facility_types:
        lat_offset = random.uniform(-0.03, 0.03)
        lon_offset = random.uniform(-0.03, 0.03)

        facilities.append({
            'lat': center_lat + lat_offset,
            'lon': center_lon + lon_offset,
            'name': facility['name'],
            'type': facility['type'],
            'icon': facility['icon'],
            'contact': f'+1-555-{random.randint(1000, 9999)}'
        })

    return facilities

def display_analytics(data: pd.DataFrame) -> None:
    """Display analytics and visualizations for the disaster data."""
    st.markdown("### 📊 Disaster Analytics")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=data, x='timestamp', y='severity', ax=ax)
    ax.set_title('Disaster Severity Over Time')
    ax.set_xlabel('Time')
    ax.set_ylabel('Severity')
    st.pyplot(fig)

    st.markdown("#### Key Statistics")
    cols = st.columns(4)
    cols[0].metric("Peak Severity", f"{data['severity'].max():.1f}")
    cols[1].metric("Average Severity", f"{data['severity'].mean():.1f}")
    cols[2].metric("Current Severity", f"{data['severity'].iloc[-1]:.1f}")
    cols[3].metric("Hours Simulated", len(data))

def run_simulation(disaster_type: str, location_name: str, duration_hours: int, intensity: float) -> None:
    """Run the complete disaster simulation and display results."""
    coordinates = get_coordinates(location_name)
    data = simulate_disaster_data(disaster_type, duration_hours, intensity, coordinates)
    weather_data = get_weather_data(coordinates)

    st.markdown(f"## 🎯 Prediction Results for {location_name}")
    create_enhanced_map(data, disaster_type, location_name)
    display_analytics(data)
    display_recommendations(data, disaster_type, location_name, weather_data)

    # Initialize NewsService with the API key
    news_service = NewsService(st.secrets["NEWS_API_KEY"])

    # Initialize YouTube service
    youtube_service = YouTubeService(st.secrets["YOUTUBE_API_KEY"])

    # Fetch and display videos
    videos = youtube_service.fetch_disaster_videos(disaster_type, location_name)
    display_youtube_section(videos)

    # Fetch and display news
    news_articles = news_service.fetch_disaster_news(disaster_type, location_name)
    display_news_section(news_articles)

    # Display Twitter updates (existing feature)
    display_disaster_news(disaster_type, location_name)

def display_recommendations(data: pd.DataFrame, disaster_type: str, location_name: str, weather_data: Dict):
    """Display emergency recommendations and alerts."""
    st.markdown("### 🚨 Emergency Response Recommendations")

    current_severity = data['severity'].iloc[-1]
    alert_level = DISASTER_TYPES[disaster_type]["alert_levels"][
        min(int(current_severity / 4), len(DISASTER_TYPES[disaster_type]["alert_levels"]) - 1)
    ]

    # Create metrics cards
    metrics_cols = st.columns(3)
    with metrics_cols[0]:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Current Severity</h4>
                <h2>{current_severity:.1f}/10</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
    with metrics_cols[1]:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Alert Level</h4>
                <h2>{alert_level}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
    with metrics_cols[2]:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>Location</h4>
                <h2>{location_name}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Safety Instructions
    st.markdown("### 🛡️ Safety Instructions")
    safety_cols = st.columns(2)

    with safety_cols[0]:
        st.markdown("#### Immediate Actions:")
        if disaster_type == "Flood":
            st.markdown("""
            1. Move to higher ground immediately
            2. Avoid walking or driving through flood waters
            3. Follow evacuation orders without delay
            4. Turn off utilities at main switches if safe
            5. Disconnect electrical appliances
            """)
        elif disaster_type == "Earthquake":
            st.markdown("""
            1. Drop, Cover, and Hold On
            2. Stay away from windows and exterior walls
            3. If indoors, stay there until shaking stops
            4. Be prepared for aftershocks
            5. Check for injuries and damage
            """)
        elif disaster_type == "Wildfire":
            st.markdown("""
            1. Follow evacuation orders immediately
            2. Close all windows and doors
            3. Remove flammable curtains and furniture
            4. Turn on lights for visibility in smoke
            5. Take emergency supply kit
            """)
        elif disaster_type == "Hurricane":
            st.markdown("""
            1. Stay indoors and away from windows
            2. Monitor official weather updates
            3. Keep emergency supplies accessible
            4. Fill bathtubs and containers with water
            5. Stay in a small, interior room
            """)
        elif disaster_type == "Tsunami":
            st.markdown("""
            1. Move inland immediately
            2. Get to high ground quickly
            3. Follow evacuation routes
            4. Stay away from the coast
            5. Wait for official all-clear signal
            """)

    with safety_cols[1]:
        st.markdown("#### Preparation Steps:")
        st.markdown("""
        1. Prepare an emergency kit containing:
           - Water (1 gallon per person per day)
           - Non-perishable food
           - First aid supplies
           - Flashlights and batteries
           - Important documents

        2. Create a communication plan:
           - Emergency contact numbers
           - Family meeting points
           - Out-of-area contact person

        3. Stay informed:
           - Monitor local news
           - Follow official social media
           - Keep emergency radio handy
        """)

    # Additional Resources Section
    st.markdown("### 📚 Additional Resources")
    resources_cols = st.columns(3)

    with resources_cols[0]:
        st.markdown("#### Official Links")
        st.markdown("""
        - [Local Emergency Services](https://example.com/emergency)
        - [Weather Updates](https://weather.com)
        - [Evacuation Routes](https://example.com/evacuation)
        """)

    with resources_cols[1]:
        st.markdown("#### Emergency Supplies")
        st.markdown("""
        - [Emergency Kit Checklist](https://example.com/checklist)
        - [First Aid Guide](https://example.com/firstaid)
        - [Safety Equipment](https://example.com/equipment)
        """)

    with resources_cols[2]:
        st.markdown("#### Community Support")
        st.markdown("""
        - [Volunteer Opportunities](https://example.com/volunteer)
        - [Donation Centers](https://example.com/donate)
        - [Community Forums](https://example.com/community)
        """)
def gemini_search(query: str, disaster_type: str) -> str:
    """
    Perform a search using Google's Gemini AI and return the response.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        You are an AI assistant specializing in disaster preparedness and response for all types of natural and man-made disasters. Your knowledge covers a wide range of events including but not limited to floods, earthquakes, hurricanes, wildfires, tsunamis, volcanic eruptions, tornadoes, landslides, extreme weather events, pandemics, and industrial accidents.

        Current focus: {disaster_type}

        User query: {query}

        Please provide accurate, relevant, and helpful information in response to the user's query. Your response should:
        1. Directly address the user's question with factual, up-to-date information.
        2. If the query is about {disaster_type}, provide specific details relevant to that disaster type.
        3. If the query is about a different disaster type, acknowledge this and provide information about that disaster instead.
        4. Include safety measures, preparation tips, and emergency responses when applicable.
        5. Offer general disaster preparedness advice if the query is broad or not disaster-specific.
        6. If the query is completely unrelated to disasters or preparedness, politely redirect the user to ask about relevant topics.

        Aim for a concise yet comprehensive response, prioritizing the most critical information first. If appropriate, mention reliable sources or organizations for further information.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error in Gemini search: {e}")
        return "Sorry, I couldn't process your query at the moment. Please try again later."

def main():
    """Main application function."""

    # Update the CSS for better mobile responsiveness
    st.markdown("""
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 300px;
            max-width: 100%;
        }
        [data-testid="stSidebar"][aria-expanded="false"] {
            min-width: 300px;
            margin-left: -300px;
        }
        @media (max-width: 768px) {
            [data-testid="stSidebar"][aria-expanded="true"] {
                min-width: 100%;
                max-width: 100%;
            }
            [data-testid="stSidebar"][aria-expanded="false"] {
                margin-left: -100%;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    

    # Specify the paths to the images
    header_image_path = "images/header_image.png"
    logo_image_path = "images/logo_image.png"


    if os.path.exists(header_image_path):
        try:
            header_image = Image.open(header_image_path)
            # Resize the header image to a specific size (e.g., 800x200 pixels)
            resized_header_image = header_image.resize((400, 125))
            st.image(resized_header_image, use_column_width=True)
        except Exception as e:
            st.error(f"Error loading header image: {e}")
    else:
        st.error(f"Header image not found at path: {header_image_path}")
    # Colored header with description
    st.markdown("<h2 style='color: #3B82F6;'>Enhanced Disaster AI Predictor by Team_Nexus</h2>", unsafe_allow_html=True)
    st.write("Advanced prediction and alert system for natural disasters",
        color_name="blue-70"
    )

    try:
        with st.sidebar:
            if os.path.exists(logo_image_path):
                try:
                    logo_image = Image.open(logo_image_path)
                    # Resize the logo image to a specific size (e.g., 100x100 pixels)
                    resized_logo_image = logo_image.resize((380, 380))
                    st.image(resized_logo_image)
                except Exception as e:
                    st.error(f"Error loading logo image: {e}")
            else:
                st.error(f"Logo image not found at path: {logo_image_path}")
            colored_header(
                label="Scenario Configuration",
                description="Set up your disaster prediction parameters",
                color_name="blue-30"
            )

            disaster_type = st.selectbox(
                "Select Disaster Type",
                list(DISASTER_TYPES.keys()),
                format_func=lambda x: f"{DISASTER_TYPES[x]['icon']} {x}"
            )

            location_name = st.text_input("Enter Location", "Hyderabad, India")

            st.markdown("### Simulation Parameters")
            duration_hours = st.slider("Duration (hours)", 12, 72, 24)
            intensity = st.slider("Initial Intensity", 1, 10, 5)

            if st.button("Generate Prediction", type="primary"):
                with st.spinner("🔄 Running simulation..."):
                    run_simulation(disaster_type, location_name, duration_hours, intensity)

        # Improved Gemini-powered search section
        st.markdown("### Ask about Disaster Preparedness")
        user_query = st.text_input("Enter your question about disaster preparedness:")
        if st.button("Search", key="gemini_search"):
            if user_query:
                with st.spinner("Searching..."):
                    response = gemini_search(user_query, disaster_type)
                    st.markdown(f"### Response:\n{response}")
            else:
                st.warning("Please enter a question before searching.")

        # New alert section using display_send_alert_section
        display_send_alert_section(disaster_type, intensity, location_name)

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        logger.exception("Main app error")

if __name__ == "__main__":
    main()
