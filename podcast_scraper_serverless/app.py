"""This module defines the lambda_handler
"""
import json

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from custom_process import CustomProcess


def spider_process(spider, settings=None):
    """Runs a scrapy CrawlerRunner"""
    runner = CrawlerRunner(settings)
    deferred = runner.crawl(spider)
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()


def run_spider(event):
    """Runs selected spider from event.

    This function runs the scrapy crawler on a multiprocessing
    Process. This is a workaround to avoid errors when the container
    is re-utilized and the scrapy is trying to start the a Twisted
    reactor again (this generates an exception).
    Note: The function expects that event has a pathParameter
    with key spider_name.
    Event example:
    {
      "pathParameters": {
        "spider_name": "spider_name_here"
      }
    }
    Example URL for API call:
    "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/spider/spider_name_here"

    :param event: event from lambda handler.
    :return: dictionary with response.
    """
    settings = get_project_settings()
    spider_name = event['pathParameters']['spider_name']
    output_bucket = settings['OUTPUT_BUCKET']
    settings['OUTPUT_URI'] = f"s3://{output_bucket}/{spider_name}-rss.xml"

    p = CustomProcess(target=spider_process, args=(spider_name, settings))
    p.start()
    p.join()

    if not p.exception:
        status_code = 200
        message = 'Success'
    else:
        error, traceback = p.exception
        status_code = 500
        message = 'Internal error:\n' + traceback

    return {
        "statusCode": status_code,
        "body": json.dumps({
            "message": message
        }),
    }


def lambda_handler(event, context):
    response = run_spider(event)
    return response
