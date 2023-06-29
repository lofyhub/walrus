from fastapi import FastAPI
import uvicorn
from config.config import settings
from routes.business import business_routes

app=FastAPI()
app.include_router(business_routes)

@app.get('/health')
async def health_check():
    return {
        'app_name': settings.APP_NAME,
        'status':'ok 👍 '
        }

if __name__ == "__main__":
    port = settings.PORT

    app_module = "main:app"
    uvicorn.run(app_module, host="0.0.0.0", port=port, reload=True)