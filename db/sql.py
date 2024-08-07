
drop_table = '''
    DROP TABLE IF EXISTS {}
'''

create_table = '''
    CREATE TABLE {} (
        id INTEGER PRIMARY KEY,
        title VARCHAR(50) NOT NULL,
        content VARCHAR(500) NOT NULL,
        published INTEGER NOT_NULL,
        created_at TEXT NOT NULL
    )
'''

delete_all = '''
    DELETE FROM {}
'''

