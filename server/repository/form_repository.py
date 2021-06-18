from server.models.form import (
    FormSchema,
    UpdateFormModel,
)
from bson.objectid import ObjectId
from server.repository.repo_connection import form_collection


async def add_form(form_data: FormSchema):
    if hasattr(form_data, "id"):
        delattr(form_data, "id")
    form = await form_collection.insert_one(form_data.dict(by_alias=True))
    form_data.id = form.inserted_id
    return {"form": form_data}


async def retrieve_all_form():
    forms = []
    async for form in form_collection.find():
        forms.append(FormSchema(**form))
    return {"forms": forms}


async def retrieve_form_by_id(id: str):
    form = await form_collection.find_one({"_id": ObjectId(id)})
    if form:
        form = FormSchema(**form)
        return {"form": form}


async def update_form(id: str, form: UpdateFormModel):
    form = {k: v for k, v in form.dict().items() if v is not None}

    if len(form) >= 1:
        result = await form_collection.update_one({"_id": ObjectId(id)}, {"$set": form})

        if result.modified_count == 1:
            form = await form_collection.find_one({"_id": ObjectId(id)})
            form = FormSchema(**form)
            if form:
                return form

    if (existing := form_collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing


async def delete_form(id: str):
    if (form := form_collection.find_one({"_id": ObjectId(id)})) is not None:
        await form_collection.delete_one({"_id": ObjectId(id)})
        return True


async def delete_forms(ids: list):
    if len(ids) > 0:
        for count, value in enumerate(ids):
            ids[count] = ObjectId(value)
        form_collection.delete_many({"_id": {"$in": ids}})
        form = form_collection.find({"_id": {"$in": ids}})
        if form:
            return True
