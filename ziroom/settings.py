SPIDER_MODULES = ['ziroom.spiders']
NEWSPIDER_MODULE = 'ziroom.spiders'

ITEM_PIPELINES = {
    'ziroom.pipelines.ZiRoomPipeline': 1
}

DOWNLOAD_DELAY = 5

LOG_LEVEL = 'WARN'
