import os
import re
import ssl
import uuid
import time
import requests
from lxml import etree
from urllib.error import HTTPError
from urllib.request import urlretrieve

from .db_oper import fetch_title
from tools import gen_path

from config import FILTER_BLOG
from config import HELLO_WORLD_DB

# 全局取消证书验证（使用python urllib时出现[SSL: CERTIFICATE_VERIFY_FAILED]报错的解决方案）
ssl._create_default_https_context = ssl._create_unverified_context

_hlwd_db = '/data/hello_world'

_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'uuid_tt_dd=10_17440591400-1566540027018-475801; dc_session_id=10_1566540027018.170336; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_17440591400-1566540027018-475801!1788*1*PC_VC; smidV2=20190823142102f8fa184e37cafdf0adbc88337c1e835f00cc1c7f03c8a1fd0; Hm_ct_e5ef47b9f471504959267fd614d579cd=6525*1*10_17440591400-1566540027018-475801; __yadk_uid=HkrNA39b2yvA17uARJ2DLfztq3pIJibO; Hm_lvt_e5ef47b9f471504959267fd614d579cd=1569226319,1570779466,1571026423; Hm_lpvt_e5ef47b9f471504959267fd614d579cd=1571026423; __gads=Test; acw_tc=2760823215722447503147003e9de8e40dd331448130b6d6d72f5149d4f6b1; SESSION=81fe089d-ab17-40c9-951a-257ecb983d53; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1572595973,1572595991,1572596055,1572596126; announcement=%257B%2522isLogin%2522%253Afalse%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fblogdev.blog.csdn.net%252Farticle%252Fdetails%252F102605809%2522%252C%2522announcementCount%2522%253A0%252C%2522announcementExpire%2522%253A3600000%257D; acw_sc__v2=5dc379a2f178e210bd3d6fd81cbe96cbf3ae73a8; dc_tos=q0ktd7; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1573091757; c-login-auto=27',
    'Host': 'blog.csdn.net',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1'
}


def crawl_first(blog_type: str) -> list:
    """解析首页，返回符合条件的链接"""
    links = []

    tree = etree.HTML(
        requests.get(
            f'https://www.csdn.net/nav/{blog_type}',
            headers=_headers
        ).text
    )

    # 定位到每一篇博客
    blogs: list = tree.xpath('.//li[@class="clearfix"]')

    for blog in blogs:

        # 解析获取文章链接、文章访问量
        try:
            title = blog.xpath('.//div/div[1]/h2/a/text()')[0].strip()
            link = blog.xpath('.//div/div[1]/h2/a/@href')[0]
        except IndexError:
            continue

        # 过滤文章
        if (link not in FILTER_BLOG  # 过滤禁止的文章
                and not fetch_title(title)):  # 过滤已存在的文章
            links.append((title, link))

    return links


def crawl_second(link: str) -> tuple:
    """获取解析文章内容"""
    page_text = requests.get(link, headers=_headers).text
    # with open('text.html', 'w', encoding='UTF-8') as f:
    #     f.write(page_text)
    tree = etree.HTML(page_text)
    content = re.search(r'<article class="baidu_pl">.+?</article>', page_text, flags=re.S).group()
    all_img_link = re.findall(r'(https://img-blog\.csdnimg\.cn.+?)"', content, re.S)
    return content, all_img_link


def down_img(img_link: str, now_img_links: list):
    """下载图片并返回新的图片链接"""
    try:
        img_name = f'{str(uuid.uuid4())}.png'
        year_month = time.strftime('%Y-%m')
        now_ai_dir = gen_path(HELLO_WORLD_DB, 'media/ai', year_month)
        img_path = gen_path(now_ai_dir, img_name)

        # 若目录不存在，则创建目录
        os.path.exists(now_ai_dir) or os.mkdir(now_ai_dir)

        try:
            # 开始下载图片
            urlretrieve(img_link, img_path)

            # 将完工的图片链接添加到就绪队列
            now_img_links.append((img_link, f'/media/ai/{year_month}/{img_name}'))

        except HTTPError as e:
            # 下载出错则删除未成功下载的图片
            os.remove(img_path)
            print(e)

    except Exception as e:
        print(e)
