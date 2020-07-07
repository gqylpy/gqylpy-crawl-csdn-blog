import re
from urllib.parse import quote

from tools import gen_path

from config import FE
from config import DB_DIR
from config import WLMJ_VISIT_LINK
from config import WLMJ_PAYMENT_LINK
from config import DESCRIBE_REPLACE_STRING
from config import ARTICLE_DESCRIPTION_LENGTH

_wlmj_file = gen_path(DB_DIR, 'wlmj.html')


def filter_copyright(content: str) -> str:
    """过滤版权信息"""
    copyright_info = re.search(
        r'(<div class="article-copyright">.+?)<link',
        content, flags=re.S
    )

    if copyright_info is None:
        return content

    return content.replace(copyright_info.group(1), '')


def quote_data(title: str, content: str, now_img_links: list) -> tuple:
    """编码数据并提取出描述信息"""

    # 过滤版权信息
    content = filter_copyright(content)

    # 提取描述信息
    description = re.sub(r'<.+?>', '', content, flags=re.S)
    for string in DESCRIBE_REPLACE_STRING:
        description = description.replace(string, '')

    # 替换图片链接
    for old_link, now_link in now_img_links:
        content = content.replace(old_link, now_link)

    title = quote(title)
    content = quote(content)
    description = quote(description[:ARTICLE_DESCRIPTION_LENGTH])

    return title, content, description
