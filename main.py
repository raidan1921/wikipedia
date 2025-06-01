import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from wiki_scraper import traverse_articles_async
from frequency import compute_frequency, filter_by_percentile

app = FastAPI(
    title="Wikipedia Word Frequency API",
    version="2.0.0",
)

class KeywordRequest(BaseModel):
    article: str
    depth: int
    ignore_list: list[str] = []
    percentile: int = 0

@app.get("/word-frequency")
async def word_frequency(
    article: str = Query(..., description="The title of the Wikipedia article to start from"),
    depth: int = Query(..., ge=0, description="Depth of traversal within linked articles")
):
    try:
        words = await traverse_articles_async(article, depth)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

    freq = compute_frequency(words)
    return freq

@app.post("/keywords")
async def keywords(request: KeywordRequest):
    try:
        words = await traverse_articles_async(request.article, request.depth)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    freq = compute_frequency(words)
    filtered = filter_by_percentile(
        freq, request.percentile, set(request.ignore_list)
    )
    return filtered

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)