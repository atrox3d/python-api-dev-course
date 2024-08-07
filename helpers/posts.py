from datetime import datetime as dt
from models.post import Post, Posts


posts = Posts(posts=[
    Post(title='defaul post 1', content='default content 1', id=1, 
         created_at=dt.today().strftime('%Y-%m-%d %H:%M:%S')),
    Post(title='defaul post 2', content='default content 2', id=2,
         created_at=dt.today().strftime('%Y-%m-%d %H:%M:%S')),
])

