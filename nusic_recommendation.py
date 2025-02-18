import google.generativeai as genai
import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# Load the .env file
load_dotenv()

# API Keys
GEMINIAI_API_KEY = os.getenv("GEMINIAI_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

genai.configure(api_key=GEMINIAI_API_KEY)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

def interpret_mood(mood):
    """
    Use GeminiAI to interpret the user's mood and generate keywords
    """
    prompt = f"Generate 10 music-related keywords for a {mood} mood."
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    
    keywords = response.text.strip().split(", ")
    return keywords

def get_recommendations(keywords):
    """
    Use Spotify API to fetch music recommendations based on keywords
    """
    query = " ".join(keywords)
    results = sp.search(q=query, type="track", limit=10)
    recommendations = []
    for track in results["tracks"]["items"]:
        recommendations.append({
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "url": track["external_urls"]["spotify"]
        })
    return recommendations

def main():
    """
    Main function to interact with the user and display recommendations.
    """
    print("Welcome to the AI-Based Music Recommendation System!")
    mood = input("How are you feeling today? (e.g., happy, sad, energetic); ")
    
    print("Analyzing your mood...")
    keywords = interpret_mood(mood)
    print(f"Keywords: {', '.join(keywords)}")
    
    print("Fetching recommendations...")
    recommendations = get_recommendations(keywords)
    
    print("\nHere are your music recommendations:")
    for i, track in enumerate(recommendations, 1):
        print(f"{i}. {track['name']} by {track['artist']}")
        print(f" Listen here: {track['url']}\n")

if __name__ == "__main__":
    main()