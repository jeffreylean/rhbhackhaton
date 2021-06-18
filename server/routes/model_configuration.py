import pandas
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import pickle
from typing import List
from server.repository.model_configuration_repository import (
    add_configuration,
    delete_configuration,
    update_configuration,
    retrieve_all_configurations,
    retrieve_configuration_by_id,
    delete_configurations,
)
from server.models.model_configuration import (
    ModelConfigurationSchema,
    ResponseModel,
    UpdateModelConfigurationModel,
    ErrorResponseModel,
)

router = APIRouter()


@router.post(
    "/AddConfiguration", response_description="add model configuration into database"
)
async def add_model_configuration_data(configuration: ModelConfigurationSchema):
    new_configuration = await add_configuration(configuration)
    return ResponseModel(new_configuration, "configuration added successfully")


@router.get(
    "/RetrieveAllConfigurations",
    response_description="retrieve all model configuration data",
)
async def get_all_configurations():
    all_configurations = await retrieve_all_configurations()
    return ResponseModel(
        all_configurations, "All configurations successfully retrieved"
    )


@router.get(
    "/RetrieveConfigurationById/{id}",
    response_description="retrive configuration by id",
)
async def get_configuration_by_id(id):
    configuration = await retrieve_configuration_by_id(id)
    if configuration:
        return ResponseModel(configuration, "Configuration  retrieved successfully")
    return ErrorResponseModel("An error occured.", 404, "Configuration  does not exist")


@router.put("/UpdateConfiguration/{id}", response_description="update configuration/")
async def update_configuration_by_id(
    id, req: UpdateModelConfigurationModel = Body(...)
):
    configuration = await update_configuration(id, req)
    if configuration:
        return ResponseModel(configuration, "Configuration  updated successfully")
    return ErrorResponseModel("An error occured", 404, "Updating Error")


@router.delete("/DeleteConfiguration/{id}", response_description="Delete configuration")
async def delete_configuration_by_id(id: str):
    delete = await delete_configuration(id)
    if delete:
        return ResponseModel(
            "Configuration with ID:{} is deleted".format(id),
            "Configuration deleted successfully",
        )
    return ErrorResponseModel(
        "An error occured", 404, "Configuration  with id {} doesn't exist".format(id)
    )


@router.post("/DeleteConfigurations", response_description="Delete Configurations")
async def delete_configuration_by_ids(ids: List[str]):
    delete = await delete_configuration(ids)
    if delete:
        return ResponseModel("", "Configurations deleted successfully")
    return ErrorResponseModel("An error occured", 404, "Configurations doest not exist")
