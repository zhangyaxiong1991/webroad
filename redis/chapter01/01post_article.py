import time

import redis

ONE_WEEK_IN_SECONDS = 7*24*60*60

def post_article(conn, user, title, link):
    """
    添加一篇文章
    """
    # 获取atricle_id(获取后自增1)
    article_id = str(conn.incr("article:id"))

    # 存储文章信息 article_id user title link add_time
    add_time = time.time()
    conn.hmset("article:"+article_id, {
        'title': title,
        'user': user,
        'add_time': add_time,
        'link': link,
        'votes': 1,
    })

    # 创建已投票用户set
    conn.sadd("article:voted:"+article_id, user)

    # 设置已投票用户set的过期值，过期后无法再投票
    conn.expire("article:voted:"+article_id, ONE_WEEK_IN_SECONDS)

    # 获取文章初始分数并存执zset中
    conn.zadd("article:scores", article_id, add_time)
    conn.zadd("article:times", article_id, add_time)

    return article_id

if __name__ == "__main__":
    conn = redis.Redis(host="127.0.0.1", port=6379, db=0)
    post_article(conn, 'test', 'art01', '/arts/01')
    # conn.zadd("article:test", test=1)
