# scrapy-podcast-rss-serverless

This is a serverless example for [scrapy-podcast-rss](https://github.com/igarizio/scrapy-podcast-rss).  
To try it, you need to install scrapy-podcast-rss:
```console
$ pip install scrapy-podcast-rss
```

## Configuration
You need to have installed and configured [AWS SAM CLI](https://aws.amazon.com/serverless/sam/)
You can then [fork](https://github.com/igarizio/scrapy-podcast-rss-serverless/fork) or clone 
this repo and review some of the configurations:
- ``samconfig.toml``: Check ``stack_name``, ``s3_bucket``, ``s3_prefix``, ``region``.
- ``template.yaml``: Check ``Timeout``. Additionally, uncomment the schedule part
    if you want to schedule crawls.
- ``podcast_scraper/settings.py``: Set ``OUTPUT_BUCKET``.
- ``podcast_scraper/spiders``: Add any new spider you want (you can also just test
    the ``minimal`` spider).

## AWS SAM CLI
```console
$ sam build --use-container
$ sam deploy
```

## Firing a crawl
1. Look up for ``ScrapePodcastsApi`` output when deploying.  
   The URL will look like ``https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/spider/{spider_name}``.  
   Replace ``{spider_name}`` with the name of your spider (or ``minimal`` to run
   the example).
2. Make a get request to the URL.