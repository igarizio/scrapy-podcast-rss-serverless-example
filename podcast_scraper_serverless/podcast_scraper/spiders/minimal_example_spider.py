"""Minimal example spider.

This module demonstrates how to create a spider that uses the pipeline,
items and exporters provided in scrapy_podcast_rss, to save the data to
a RSS file. This file can then be read with any podcast player.
"""
import datetime

import scrapy
import pytz
import uuid

from scrapy_podcast_rss import PodcastEpisodeItem, PodcastDataItem


class SampleSpider(scrapy.Spider):
    """Spider scrapes quotes to simulate scraping audio files."""
    name = "minimal"
    start_urls = ["http://quotes.toscrape.com/"]  # Used as a dummy request. This is not actually scraped.

    def parse(self, response):
        """Parses the starting page.

        No matter how many requests you make, your spider needs to yield
        at least ONE PodcastDataItem and one PodcastEpisodeItem for each
        episode before closing. The pipeline will order the PodcastEpisodeItems
        based on the order of instantiation (not the order of yielding).

        Keep in mind that this is a dummy spider. It serves only as an example.
        """
        podcast_data_item = PodcastDataItem()  # Item that stores information about the podcast.

        podcast_data_item['title'] = "Podcast Title"
        podcast_data_item['description'] = "Description of the podcast."
        podcast_data_item['url'] = self.start_urls[0]  # Podcast's url
        podcast_data_item['image_url'] = "https://live.staticflickr.com/4211/35400224382_9edcb984e5_c.jpg"

        yield podcast_data_item  # You MUST yield at least one PodcastDataItem before the spider closes.

        # This will probably need to be done with a new request and a new callback function.
        # Please refer to scrapy's documentation for this.
        episodes = simulate_episode_data(10)

        for episode in episodes:
            episode_item = PodcastEpisodeItem()  # Item that stores information about each episode.

            episode_item['title'] = episode['title']
            episode_item['description'] = episode['description']
            pub_date_tz = datetime.datetime.strptime(episode['publication_date'], "%m/%d/%Y").replace(tzinfo=pytz.UTC)
            episode_item['publication_date'] = pub_date_tz  # Publication date NEEDS to have a TIME ZONE.
            episode_item['guid'] = str(uuid.uuid4())  # Simulated identifier.
            episode_item['audio_url'] = "https://ia801803.us.archive.org/13/items/MOZARTSerenadeEineKleineNachtmusikK." \
                                        "525-NEWTRANSFER01.I.Allegro/01.I.Allegro.mp3 "  # Sample audio url.

            yield episode_item


def simulate_episode_data(n_episodes):
    """Simulates episodes data from a website."""
    start_date = datetime.datetime(2019, 1, 1)
    episodes_data = []
    for i in range(1, n_episodes + 1):
        title = f'Episode {i}'
        description = f'Description of episode {i}'
        publication_date = (start_date + datetime.timedelta(i)).strftime("%m/%d/%Y")
        episode_data = {'title': title, 'description': description, 'publication_date': publication_date}
        episodes_data.append(episode_data)

    return episodes_data
