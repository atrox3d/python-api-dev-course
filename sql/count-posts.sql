-- SQLite

-- show users and posts ordered by user
SELECT users.id, users.email, posts.id, posts.title, posts.content
FROM posts
RIGHT JOIN users
on users.id = posts.owner_id
ORDER BY users.id;

-- show count of posts per user, including users without posts (NULL)
SELECT users.id, COUNT(*) 
FROM posts
RIGHT JOIN users
ON posts.owner_id = users.id
GROUP BY users.id;

-- show count of posts per user, excluding users without posts (NULL)
SELECT users.id, COUNT(posts.id)
FROM posts
RIGHT JOIN users
on users.id = posts.owner_id
GROUP BY users.id;
