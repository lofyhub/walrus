from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import config
from businesses.router import business_routes
from reviews.router import reviews_routes
from users.router import users_routes
from auth.router import auth_routes
from reviewed_businesses.router import reviewed_business_routes
from config import settings

app = FastAPI()


origins = [settings.FRONTEND_URL]

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
app.include_router(reviewed_business_routes)

app_config = config


@app.get("/health")
async def health_check():
    return {"app_name": app_config.settings.APP_NAME, "status": "ok 👍 "}


if __name__ == "__main__":
    port = int(app_config.settings.PORT)

    app_module = "main:app"
    uvicorn.run(app_module, host="0.0.0.0", port=port, reload=True)
