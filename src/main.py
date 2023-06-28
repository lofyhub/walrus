from fastapi import FastAPI
import uvicorn

app=FastAPI()

@app.get('/health')
async def health_check():
    return {'status':'ok 👍 '}

if __name__ == "__main__":
    port = int(8000)

    app_module = "main:app"
    uvicorn.run(app_module, host="0.0.0.0", port=port, reload=True)