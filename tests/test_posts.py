import tests.debug

def  setup_module():
    tests.debug.DEBUG = True

def test_get_all_posts(authorized_client):
    response = authorized_client.get('/posts')
    assert response.status_code == 200
    print(response.json())

def test_posts(session, fake_models_post):
    session.add_all(fake_models_post)
    session.commit()
