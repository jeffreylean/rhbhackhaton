from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import pickle
from typing import List

from server.database import(
    add_form,
    retrieve_all_form,
    retrieve_form_by_id,
    update_form,
    delete_form,
    delete_forms,
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
async def get_all_form():
    allForms = await retrieve_all_form()
    return ResponseModel(allForms, "All form successfully retrieved")


@router.get("/RetrieveFormById/{id}", response_description="retrive form by id")
async def get_form_by_id(id):
    form = await retrieve_form_by_id(id)
    if form:
        return ResponseModel(form, "form retrieved successfully")
    return ErrorResponseModel("An error occured.", 404, "Form does not exist")


@router.put("/UpdateForm/{id}", response_description="update form")
async def update_form_by_id(id, req: UpdateFormModel = Body(...)):
    form = await update_form(id, req)
    if form:
        return ResponseModel(form, "form updated successfully")
    return ErrorResponseModel("An error occured", 404, "Updating Error")


@router.delete("/DeleteForm/{id}", response_description="Delete Form")
async def delete_form_by_id(id: str):
    delete = await delete_form(id)
    if delete:
        return ResponseModel("form with ID:{} is deleted".format(id), "form deleted successfully")
    return ErrorResponseModel(
        "An error occured", 404, "form with id {} doesn't exist".format(id)
    )


@router.post("/DeleteForms", response_description="Delete Form")
async def delete_form_by_ids(ids: List[str]):
    delete = await delete_forms(ids)
    if delete:
        return ResponseModel("", "forms deleted successfully")
    return ErrorResponseModel("An error occured", 404, "form doest not exist")


@router.get("/Predict/{id}", response_description="Predict credit scoring on each form")
async def predict_credit_score(id: str):
    model = pickle.load(open("finalized_model.pkl", "rb"))
    form = await retrieve_form_by_id(id)
    form = form["form"]
    if form:
        pred_name = model.predict(
            [[5000, 4000, 1, 5, 20, 8, 2, 7000, 4, 10000]]).tolist()
        return ResponseModel("Credit score of form ID:{} has been predicted.\n The value is {}".format(id, pred_name[0]), "Credit Predict Successfully")
