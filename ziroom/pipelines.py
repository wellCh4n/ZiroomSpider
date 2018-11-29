import os
from os.path import join


class ZiRoomPipeline(object):

    def __init__(self) -> None:
        super().__init__()
        self.cache_files = dict()

    def process_item(self, item, spider):
        path = os.path.abspath(join(os.getcwd(), 'csv'))
        if not os.path.exists(path):
            os.makedirs(path)

        item_dict = dict(item)
        csv_body = ','.join(str(x) for x in item_dict.values())

        file_name = join(path, 'output.csv')
        file = open(file_name, 'a+', encoding='utf-8')

        file.write(csv_body + '\n')

        return item
