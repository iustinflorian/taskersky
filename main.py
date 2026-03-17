from database import collection
from models import TaskModel
from fastapi import FastAPI
from bson import ObjectId
from fastapi import HTTPException

# creating the app instance
app = FastAPI(title="Taskersky | Personal Task Tracking")

# this is a simple GET route, 'async' meaning it can handle other requests while waiting
@app.get("/")
async def root():
    return {"status": "Taskersky is up and running!"}

@app.post("/tasks/write")
async def create_task(task: TaskModel):
    # 'task.dict()' converts the Pydantic objects into Python dictionary
    # MongoDB only understands dict/JSON, not Pydantic classes
    task_dict = task.dict()

    # 'await' tells Python to send to MongoDB and wait until it's saved
    new_task = await collection.insert_one(task_dict)

    return {
        "id": str(new_task.inserted_id),
        "message": "Successfully saved to the database"
    }

@app.get("/tasks/read")
async def get_tasks():
    # create a cursor to find all documents in `tasks`
    # find() prepares the query
    cursor = collection.find()

    # fetch data and convert to Python list
    # we use `await` to wait for the `to_list` to finish
    tasks = await cursor.to_list(length=100)

    # MongoDB stores ID as objects that can't be sent as JSON
    # we loop through each task and convert `_id` field to string
    for task in tasks:
        task["_id"] = str(task["_id"])

    # return clean list with tasks
    return tasks

@app.put("/tasks/update/{task_id}")
async def update_task(task_id: str):
    # the whole server crashed from entering a wrong id in swagger
    # to fix that we check if the id is valid and throw an exception
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid ID Format.")

    # search for the task with the specified id
    # convert the string `task_id` into MongoDB ObjectId
    query = {"_id": ObjectId(task_id)}

    # define what to change (complete task)
    # $set is a special MongoDB operator
    new_values = {"$set": {"completed": True}}

    # update the first entry
    result = await collection.update_one(query, new_values)

    # check if task was found and updated
    if result.modified_count == 1:
        return {"message": "Task marked as completed!"}
    
    return {"message": "Task not found/ already completed."}

@app.delete("/tasks/delete/{task_id}")
async def delete_task(task_id: str):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid ID Format.")
    
    query = {"_id": ObjectId(task_id)}
    result = await collection.delete_one(query)
    if result.deleted_count == 1:
        return {"message": "Task deleted successfully!"}
    
    return {"message": "Task not found/ already deleted."}