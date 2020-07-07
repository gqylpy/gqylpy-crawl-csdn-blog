import time
from concurrent.futures import ThreadPoolExecutor

from .crawl import down_img
from .crawl import crawl_first
from .crawl import crawl_second
from .db_oper import create_blog
from .process_data import quote_data
from .process_data import filter_copyright

from config import POOL_NUMBER
from config import FETCH_BLOG_TYPE
from config import CRAWL_INTERVAL_TIME


def main():
    title: str
    link: str

    while True:
        try:
            for blog_type in FETCH_BLOG_TYPE:
                # 获取符合条件的文章链接
                data: list = crawl_first(blog_type)

                print(f'{blog_type}, 已获取 {len(data)} 篇文章')

                # 获取这篇优质文章的内容
                for title, link in data:
                    print(title, '--已开始')

                    new_img_lists = []
                    content, all_img_link = crawl_second(link)

                    # 开始下载图片
                    if all_img_link:
                        tp = ThreadPoolExecutor(POOL_NUMBER)
                        [tp.submit(down_img, link, new_img_lists) for link in all_img_link]
                        tp.shutdown()

                    # 编码数据并写入数据库
                    create_blog(*quote_data(title, content, new_img_lists), blog_type)

                    time.sleep(CRAWL_INTERVAL_TIME)
                time.sleep(CRAWL_INTERVAL_TIME)
        except Exception as e:
            print(title, '--已报错', e)
