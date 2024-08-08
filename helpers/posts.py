from datetime import datetime as dt
from models.post import Post, Posts


posts = Posts(posts=[
    Post(title='defaul post 1', content='default content 1', id=1),
    Post(title='defaul post 2', content='default content 2', id=2)
])

