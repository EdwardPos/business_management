from fastapi import FastAPI

app = FastAPI()

PROJECT = 'Business Management System'


@app.get("/")
async def proj_name():
    return f'Starting a PTU8 Project: {PROJECT}'
