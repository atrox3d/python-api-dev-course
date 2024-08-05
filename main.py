from fastapi import Body, FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "welcome to my api"}

@app.get('/posts')
def get_posts():
    return {'data': 'this is your post'}

@app.post('/createpost')
def create_post(
                    payload:dict # =Body()
                ):
    print(f'{payload = }')
    return {
        'message': {
            'succesfully created': payload
        }
    }