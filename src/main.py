from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config.config import settings

from businesses.router import business_routes
from reviews.router import reviews_routes
from users.router import  users_routes
from auth.router import auth_routes

app=FastAPI()


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(business_routes)
app.include_router(reviews_routes)
app.include_router(users_routes)
app.include_router(auth_routes)

@app.get('/health')
async def health_check():
    return {
        'app_name': settings.APP_NAME,
        'status':'ok 👍 '
        }

if __name__ == "__main__":
    port = int(settings.PORT)

    app_module = "main:app"
    uvicorn.run(app_module, host="0.0.0.0", port=port, reload=True)