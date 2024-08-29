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

-- the right query
SELECT posts.*, COUNT(votes.post_id) as votes
FROM posts LEFT JOIN votes
ON posts.id = votes.post_id
-- WHERE posts.id = 1
GROUP BY posts.id;

-- fixed vote count in sqlalchemy
SELECT posts.id AS posts_id, posts.title AS posts_title, 
posts.content AS posts_content, posts.published AS posts_published, 
posts.created_at AS posts_created_at, posts.owner_id AS posts_owner_id, 
count(votes.post_id) AS votes 
FROM posts LEFT OUTER JOIN votes 
ON posts.id = votes.post_id GROUP BY posts.id

-- practice
SELECT posts.id, votes.post_id
FROM posts LEFT JOIN votes
ON posts.id = votes.post_id;

SELECT posts.id, COUNT(*)
FROM posts LEFT JOIN votes
ON posts.id = votes.post_id
GROUP BY  posts.id;

SELECT posts.id, COUNT(votes.post_id)
FROM posts LEFT JOIN votes
ON posts.id = votes.post_id
GROUP BY posts.id;

SELECT posts.id, post.title, votes.post_id
FROM posts LEFT JOIN votes
ON posts.id = votes.post_id;

SELECT posts.id, posts.title, COUNT(votes.post_id), users.email
FROM posts LEFT JOIN votes
ON posts.id = votes.post_id
LEFT JOIN users
ON votes.user_id == users.id
GROUP BY votes.post_id;

SELECT posts.id, posts.title,users.email
FROM posts LEFT JOIN votes
ON posts.id = votes.post_id
LEFT JOIN users
ON votes.user_id == users.id
;