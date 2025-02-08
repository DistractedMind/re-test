from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="test Swagger API", version="1.0")

# Define a simple Pydantic model for our item
class Item(BaseModel):
    id: int
    name: str
    description: str = None

# In-memory storage for items; in a real app, you'd use a database
items: Dict[int, Item] = {}

# GET: Retrieve all items
@app.get("/items/", response_model=Dict[int, Item])
def get_items():
    """
    Retrieve all items.
    """
    return items

# GET: Retrieve a single item by its ID
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """
    Retrieve an item by its ID.
    """
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

# POST: Create a new item
@app.post("/items/", response_model=Item, status_code=201)
def create_item(item: Item):
    """
    Create an item. The item must have a unique ID.
    """
    if item.id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item.id] = item
    return item

# PUT: Update an existing item
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    """
    Update an existing item by its ID.
    """
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return item

# DELETE: Remove an item by its ID
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    """
    Delete an item by its ID.
    """
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return None
