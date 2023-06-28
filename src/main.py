from fastapi import FastAPI
import uvicorn
from config.config import settings

app=FastAPI()

@app.get('/health')
async def health_check():
    return {
        'app_name': settings.app_name,
        'status':'ok 👍 '
        }

if __name__ == "__main__":
    port = settings.PORT

    app_module = "main:app"
    uvicorn.run(app_module, host="0.0.0.0", port=port, reload=True)