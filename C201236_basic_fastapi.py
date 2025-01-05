from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# Updated internal information for news articles
news = {
    1: {
        "id": 1,
        "title": "The Adventures of Sherlock Holmes: The Master Detective",
        "content": "A deep dive into the methods and adventures of Sherlock Holmes, the world's greatest detective.",
        "author": "Dr. John Watson"
    },
    2: {
        "id": 2,
        "title": "The Time Traveler's Dilemma",
        "content": "Exploring the paradoxes and ethical questions surrounding time travel through the eyes of a time traveler.",
        "author": "H.G. Wells"
    },
    3: {
        "id": 3,
        "title": "The Mysterious Island: A Tale of Survival",
        "content": "The story of a group of survivors who are stranded on a mysterious island and their struggle for survival.",
        "author": "Jules Verne"
    },
    4: {
        "id": 4,
        "title": "Journey to the Center of the Earth",
        "content": "An exciting expedition to the Earth's core, filled with scientific wonders and dangerous creatures.",
        "author": "Jules Verne"
    },
    5: {
        "id": 5,
        "title": "The Secret Garden: A Magical Transformation",
        "content": "A story about the transformation of a neglected garden and the healing power of nature.",
        "author": "Frances Hodgson Burnett"
    },
    6: {
        "id": 6,
        "title": "The War of the Worlds: Earth's Battle for Survival",
        "content": "A thrilling account of humanity's struggle for survival against Martian invaders.",
        "author": "H.G. Wells"
    },
    7: {
        "id": 7,
        "title": "The Adventures of Tom Sawyer: A Journey of Youth",
        "content": "A classic tale of a young boy’s adventures growing up along the Mississippi River.",
        "author": "Mark Twain"
    },
    8: {
        "id": 8,
        "title": "The Call of the Wild: A Story of Survival",
        "content": "A gripping narrative of Buck, a dog who is taken from his home and forced to survive in the wild.",
        "author": "Jack London"
    },
    9: {
        "id": 9,
        "title": "Moby-Dick: The Hunt for the Great White Whale",
        "content": "A relentless quest to capture the elusive Moby-Dick, a giant white whale.",
        "author": "Herman Melville"
    },
    10: {
        "id": 10,
        "title": "1984: A Dystopian Future",
        "content": "A chilling story of a totalitarian regime that controls every aspect of society, from thought to action.",
        "author": "George Orwell"
    }
}

class News(BaseModel):
    title: str
    content: str | None = None
    author: str

@app.get("/")
def heartbeat():
    return {"message": "Hello, I am Nuzhat!"}

# Get all news
@app.get("/all_news")
def all_news():
    return news

# Filter news by title using query parameters
@app.get("/news")
def news_by_title(title_contains: str):
    filtered_news = []
    for single_news in news.values():
        if title_contains.lower() in single_news["title"].lower():
            filtered_news.append(single_news)

    if not filtered_news:
        return {"data": f"No news found with title containing '{title_contains}'"}
    
    return filtered_news

# Filter news by author and title using path and query parameters
@app.get("/news/{author}")
def news_filter_by_author_title(author: str, title_contains: str = None):
    filtered_news = [news for news in news.values() if news["author"].lower() == author.lower()]
    
    if title_contains:
        filtered_news = [news for news in filtered_news if title_contains.lower() in news["title"].lower()]
        if not filtered_news:
            return {"data": f"No news found from author {author} with title containing {title_contains}"}
    
    return filtered_news

@app.get("/news/{id}")
def news_by_id(id: int):
    if id not in news:
        return {"error": f"News with id {id} not found"}
    return news[id]

@app.post("/create-news")
def create_news(response_news: News):
    id = max(news.keys()) + 1
    news[id] = {
        "id": id,
        "title": response_news.title,
        "content": response_news.content,
        "author": response_news.author
    }
    return news[id]

if __name__ == '__main__':
    uvicorn.run("C201210_basic_fastapi:app", host='localhost', port=8000, reload=True)
