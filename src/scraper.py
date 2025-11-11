thonimport requests
from bs4 import BeautifulSoup
import json
import os

class YouTubeScraper:
    def __init__(self, channel_url):
        self.channel_url = channel_url
        self.channel_id = self.extract_channel_id(channel_url)
        self.channel_data = {}

    def extract_channel_id(self, url):
        # Extract the channel ID from the given URL
        # Assuming the channel URL format is "https://www.youtube.com/@channel_name"
        parts = url.split('@')
        return parts[-1] if len(parts) > 1 else None

    def fetch_channel_details(self):
        response = requests.get(self.channel_url)
        if response.status_code != 200:
            raise Exception("Failed to fetch channel data")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        self.channel_data['name'] = soup.find('meta', {'name': 'title'})['content']
        self.channel_data['description'] = soup.find('meta', {'name': 'description'})['content']
        self.channel_data['subscribers'] = self.get_subscribers(soup)

    def get_subscribers(self, soup):
        subscriber_text = soup.find('span', {'class': 'yt-subscriber-count'}).text.strip()
        return subscriber_text

    def get_video_data(self):
        # Fetch video data (up to 30 videos)
        videos = []
        for i in range(1, 31):
            video_url = f"{self.channel_url}/videos?page={i}"
            response = requests.get(video_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                videos.append(self.extract_video_info(soup))
        return videos

    def extract_video_info(self, soup):
        # Extract video metadata (title, views, likes)
        video_info = {}
        video_info['title'] = soup.find('h1').text
        video_info['views'] = soup.find('span', {'class': 'view-count'}).text
        video_info['likes'] = soup.find('button', {'aria-label': 'Like this video'}).text.strip()
        return video_info

    def save_data(self):
        with open(f"{self.channel_id}_data.json", 'w') as f:
            json.dump(self.channel_data, f, indent=4)

if __name__ == "__main__":
    url = "https://www.youtube.com/@rtbf_info"
    scraper = YouTubeScraper(url)
    scraper.fetch_channel_details()
    video_data = scraper.get_video_data()
    scraper.save_data()