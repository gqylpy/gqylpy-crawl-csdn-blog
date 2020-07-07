import random
from urllib.parse import quote

from tools import db
from tools import DBConn
from tools import exec_sql
from tools import gen_path

from config import FE
from config import DB_DIR
from config import VISIT_RANGE
from config import PRAISE_RANGE
from config import COMMENT_COUNT_RANGE
from config import COMMENT_TIME_ADD_DAY

_gqy_uid = 6

_channel = (
    (6, '书籍'),
    (1, '前端'),
    (2, '后端'),
    (3, '运维'),
    (4, '数据库'),
    (5, '其它'),
)

_channels = {
    'python': 2,
    'java': 2,
    'web': 1,
    'arch': 2,
    'db': 4,
    'game': 1,
    'mobile': 1,
    'ops': 2,
    'sec': 2,
    'cloud': 2,
    'engineering': 5,
    'iot': 2,
    'fund': 5,
    'avi': 5,
    'other': 5
}

_types = (
    ('original', '原'),
    ('repost', '转'),
    ('translated', '译'),
)

_comment_list = list(exec_sql(f'''
    SELECT content
    FROM comment
    ORDER BY RAND()
''', database=db.gqylpy))


def create_blog(title: str, content: str, description: str, blog_type: str) -> bool:
    """写入文章内容"""
    cur = DBConn(database=db.hello_world)

    try:
        # 插入文章内容
        cur.execute(f'''
            INSERT INTO article(content, markdown_content)
            VALUES {str((content, content))}
        ''')

        # 插入文章信息
        cur.execute('SELECT LAST_INSERT_ID()')  # 获取当前db链接中最后一次插入的数据的id
        cur.execute(f'''
            INSERT INTO blog(title, description, praise, visit, channel, type, 
              is_private, is_draft, is_delete, release_date, tags, content_id, user_id)
            VALUES ('{title}', '{description}', 
              {random.randint(*PRAISE_RANGE)}, -- 点赞量
              {random.randint(*VISIT_RANGE)}, -- 访问量
              '{_channels.get(blog_type, 5)}', -- 首页分类
              'original', 0, 0, 0, NOW(6), '',
              {cur.fetchone[0]}, {_gqy_uid})
        ''')

        # 获取这篇文章的id
        cur.execute('SELECT LAST_INSERT_ID()')
        last_insert_id = cur.fetchone[0]

        # 给文章添加评论
        for comment, in random.sample(_comment_list, random.randint(*COMMENT_COUNT_RANGE)):
            cur.execute("SELECT id FROM user WHERE username LIKE 'user%' ORDER BY RAND() LIMIT 1")
            cur.execute(f'''
                INSERT INTO comment(content, is_delete, comment_date, blog_id, user_id)
                VALUES ('{quote(comment)}', 0, 
                  DATE_ADD(NOW(), INTERVAL {random.uniform(*COMMENT_TIME_ADD_DAY)} DAY),
                  {last_insert_id}, {cur.fetchone[0]})
            ''')

        rtn = True

    except Exception as e:
        cur.conn.rollback()
        print(e)
        rtn = False

    cur.conn_commit()
    return rtn


def fetch_title(title: str):
    return exec_sql(f'''
        SELECT id
        FROM blog
        WHERE title = '{quote(title)}'
    ''', fetchone=True, database=db.hello_world)
