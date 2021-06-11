from server.models.form import(
    FormSchema,
)
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

client = MongoClient(os.getenv("MONGODB_CONN"))
db = client["AutoCred"]
collection = db.form_collection


async def add_form(form_data: FormSchema):
    if hasattr(form_data, "id"):
        delattr(form_data, "id")
    form = collection.insert_one(form_data.dict(by_alias=True))
    form_data.id = form.inserted_id
    return {"form": form_data}


async def retrieve_all_form():
    forms = []
    for form in collection.find():
        forms.append(FormSchema(**form))
    return {"forms": forms}
