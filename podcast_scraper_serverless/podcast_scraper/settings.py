BOT_NAME = 'podcast_scraper'

SPIDER_MODULES = ['podcast_scraper.spiders']
NEWSPIDER_MODULE = 'podcast_scraper.spiders'

SCHEDULER_DEBUG = 'True'
LOG_LEVEL = 'DEBUG'
# LOG_FILE = './logs/log.txt'

# app.py will use OUTPUT_BUCKET to generate an OUTPUT_URI
# using OUTPUT_BUCKET and spider_name.
OUTPUT_BUCKET = 'output-rss-bucket-name'

ITEM_PIPELINES = {
    'scrapy_podcast_rss.pipelines.PodcastPipeline': 300,
}
