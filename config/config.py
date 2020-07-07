import os


def _gen_path(*args: str) -> 'An absolute path':
    # Generate an absolute path.
    return os.path.abspath(os.path.join(*args))


BASE_DIR = _gen_path(os.path.dirname(os.path.dirname(__file__)))

DB_DIR = _gen_path(BASE_DIR, 'db')
LOG_DIR = _gen_path(BASE_DIR, 'log')

IN_SERVER = True

# 文件编码
FE = 'UTF-8'

DATETIME_FORMAT = '%F %T'

BLOG_DOMAIN = 'blog.gqylpy.com'

# 获取的文章类型
FETCH_BLOG_TYPE = ['python', 'web', 'java', 'db', 'ops', 'arch', 'game', 'mobile',
                   'sec', 'cloud', 'engineering', 'iot', 'fund', 'avi', 'other']
# mobile-安卓开发 ops-运维 arch-架构 game-游戏开发 sec-安全
# cloud-云计算/大数据 iot-物联网 fund-计算机基础 avi-印视频开发 other-其它

# 爬取的访问量不低于此值
CRAWL_MIN_ACCESS = 500

# 每次爬取间隔时长
CRAWL_INTERVAL_TIME = 60 * 2

WLMJ_VISIT_LINK = 'http://blog.gqylpy.com/gqy/401/'

WLMJ_PAYMENT_LINK = 'http://www.gqylpy.com/get_wlmj_pwd'

# 文档描述长度
ARTICLE_DESCRIPTION_LENGTH = 150

# 描述信息替换的字符
DESCRIBE_REPLACE_STRING = [' ', '\n', '\t', '&nbsp;', ]

# 赞范围
PRAISE_RANGE = 10, 90

# 访问量范围
VISIT_RANGE = 180, 600

# 评论总数范围
COMMENT_COUNT_RANGE = 0, 4

HELLO_WORLD_DB = '/data/hello_world/'

POOL_NUMBER = 5

COMMENT_TIME_ADD_DAY = 0.3, 15

# 过滤这些博客
FILTER_BLOG = [
    'https://blog.csdn.net/qq_31456593/article/details/88606284',
]
