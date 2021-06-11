from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import(
    add_form,
    retrieve_all_form
)
from server.models.form import(
    ErrorResponseModel,
    ResponseModel,
    FormSchema,
    UpdateFormModel,
)


router = APIRouter()


@router.post("/AddNewForm", response_description="form data added into database")
async def add_form_data(form: FormSchema):
    new_form = await add_form(form)
    return ResponseModel(new_form, "form added successfully.")


@router.get("/RetrieveAllForms", response_description="retrieve all form data")
async def retrieve_all_form_data():
    allForms = await retrieve_all_form()
    return ResponseModel(allForms, "All form successfully retrieved")
