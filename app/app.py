from fastapi import FastAPI, HTTPException 
from schemas import PostCreate

app = FastAPI()

notes = {
1: {"title: new notice", "content: mynotice"},
2: {"title: shopping reminder", "content: buy milk and bread"},
3: {"title: study note", "content: review fastapi basics"},
4: {"title: meeting", "content: team sync at 10am"},
5: {"title: idea", "content: personal knowledge api concept"},
6: {"title: todo", "content: clean workspace"},
7: {"title: reminder", "content: call mom"},
8: {"title: learning", "content: sqlite persistence test"},
9: {"title: thought", "content: keep project simple"},
10: {"title: note", "content: error handling needs work"},
11: {"title: task", "content: push project to git"},
12: {"title: habit", "content: drink more water"},
13: {"title: plan", "content: finish api endpoints"},
14: {"title: idea", "content: add search later"},
15: {"title: reminder", "content: backup database file"},
16: {"title: learning", "content: understand uvicorn errors"},
17: {"title: note", "content: refactor after mvp"},
18: {"title: thought", "content: simple is better"},
19: {"title: task", "content: test delete endpoint"},
20: {"title: plan", "content: stop overengineering"}

}

@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit: 
        return list(notes.values())[:limit]
    return notes 

@app.get("/posts/{id}")
def get_post(id: int):
    if id not in notes:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return notes.get(id)


@app.post("/posts")                  # This section below requires that the function only recieves of the PostCreate Schema - and not allow the return of other schema
def create_posts(post: PostCreate) -> PostCreate: # fastapi knows automatically that we are recieving a request-body because of pedantic
    new_notice = {"title": post.title, "content": post.content} 
    notes[max(notes.keys()) + 1] = new_notice 
    return new_notice   # because we specified the schema with "-> PostCreate " we can only return that format specified in our schema. 

