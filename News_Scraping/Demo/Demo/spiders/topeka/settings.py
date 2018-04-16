# Scrapy settings for topeka project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'topeka'

SPIDER_MODULES = ['topeka.spiders']
NEWSPIDER_MODULE = 'topeka.spiders'

ITEM_PIPELINES = ['topeka.pipelines.TopekaPipeline']
#COMMANDS_MODULE = 'topeka.commands'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'topeka (+http://www.yourdomain.com)'
