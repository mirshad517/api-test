from fastapi import FastAPI

app = FastAPI(title='test')



@app.get('/')
def index():
    return {'test':'test api'}