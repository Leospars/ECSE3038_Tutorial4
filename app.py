from bson import ObjectId 
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
import asyncio

from pydantic import BaseModel, BeforeValidator, Field
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Annotated
from os import getenv
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = getenv("MONGO_URI", "mongodb://localhost:27017") # Default to local MongoDB

PyObjectID = Annotated[str, BeforeValidator(str)]

class Person(BaseModel):
    id: PyObjectID | None = Field(default=None, alias="_id")
    name: str
    occupation: str
    address: str

class PersonCollection(BaseModel):
    persons: list[Person]     

app = FastAPI()

connection = AsyncIOMotorClient(MONGO_URI)
db = connection.get_database("people")

@app.post("/person")
async def create_person(person_req: Person):
    person_dict = person_req.model_dump()
    inserted_person = await db["people"].insert_one(person_dict)
    
    person = await db["people"].find_one({"_id": inserted_person.inserted_id})
    return Person(**person)

@app.get("/person")
async def get_persons():
    person_collection = await db["people"].find().to_list(length=100)
    return PersonCollection(persons=person_collection)

@app.get("/person/{person_id}")
async def get_person(person_id: PyObjectID):
    person = await db["people"].find_one({"_id": ObjectId(person_id)})
    if not person:
        raise HTTPException({"message": "Person not found"}, status_code=404)


@app.delete("/person/{person_id}")
async def delete_person(person_id: PyObjectID):
    if await get_person(person_id) is None:
        raise HTTPException(detail={"message": "Person not found"}, status_code=404)
    
    await db["people"].delete_one({"_id": ObjectId(person_id)})
    return Response(status_code=204)

class PersonUpdate(BaseModel):
    name: str | None = None
    occupation: str | None = None
    address: str | None = None

@app.patch("/person/{person_id}")
async def update_person(person_id: PyObjectID, person_req: PersonUpdate):
    person_id = ObjectId(person_id) # Convert to bson ObjectId for MongoDB query
    if not get_person(person_id):
        raise HTTPException(detail={"message": "Person not found"}, status_code=404)

    try: 
        coll = db.people
        if person_req.name:
            coll.update_one({"_id": person_id}, {"$set": {"name": person_req.name}})
        if person_req.occupation:
            coll.update_one({"_id": person_id}, {"$set": {"occupation": person_req.occupation}})
        if person_req.address:
            coll.update_one({"_id": person_id}, {"$set": {"address": person_req.address}})
        
        person = await coll.find_one({"_id": person_id})
        return Person(**person)
    except:
        raise HTTPException(detail={"message": "Update failed"}, status_code=404)