from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_all
import uvicorn

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "JobCollector API is running"}

@app.get("/scrape")
async def scrape(query: str = Query(None), location: str = Query(None)):
    print(f"Received request: query={query}, location={location}")
    jobs = scrape_all(query, location)
    return jobs

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
