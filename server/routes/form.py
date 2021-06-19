import pandas
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import pickle
from typing import List
from server.predmarketvalue import VerifyMarket

from server.repository.form_repository import (
    add_form,
    retrieve_all_form,
    retrieve_form_by_id,
    update_form,
    delete_form,
    delete_forms,
)
from server.models.form import (
    ErrorResponseModel,
    ResponseModel,
    FormSchema,
    UpdateFormModel,
)
from server.utility import vectorize, calculate_score
from server.repository.model_configuration_repository import (
    retrieve_configuration_by_id,
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
        return ResponseModel(
            "form with ID:{} is deleted".format(id), "form deleted successfully"
        )
    return ErrorResponseModel(
        "An error occured", 404, "form with id {} doesn't exist".format(id)
    )


@router.post("/DeleteForms", response_description="Delete Form")
async def delete_form_by_ids(ids: List[str]):
    delete = await delete_forms(ids)
    if delete:
        return ResponseModel("", "forms deleted successfully")
    return ErrorResponseModel("An error occured", 404, "form doest not exist")


@router.post(
    "/Predict/{id}", response_description="Predict credit scoring on each form"
)
async def predict_credit_score(
    id: str, configId: str, req: UpdateFormModel = Body(...)
):
    loanPredictModel = pickle.load(open("loanpredict_model.pkl", "rb"))
    interestPredictModel = pickle.load(open("interestpredict_model.pkl", "rb"))
    configuration = await retrieve_configuration_by_id(configId)
    form = req
    if req:
        vectorized_value = vectorize(
            [
                [
                    form.currBankAccBalance,
                    form.totalOutstandingLoan,
                    form.premiseType,
                    form.coreBusinessType,
                    form.staffNumber,
                    form.loanTerm,
                    form.collateralType,
                    form.collateralValue,
                    form.installment,
                ]
            ]
        )
        loanResult = loanPredictModel.predict(vectorized_value).tolist()
        interestResult = interestPredictModel.predict(vectorized_value).tolist()
    marketTrend = VerifyMarket(form.coreBusinessType)
    loanAmount = form.loanAmount
    final_score = calculate_score(
        loanResult[0], form.interestRate, marketTrend, loanAmount, configuration
    )
    result = [loanResult[0], interestResult[0], final_score]
    return ResponseModel(result, "Credit Predict Successfully")
