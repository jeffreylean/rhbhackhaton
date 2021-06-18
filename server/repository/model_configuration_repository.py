from server.models.model_configuration import (
    ModelConfigurationSchema,
    UpdateModelConfigurationModel,
)
from bson.objectid import ObjectId
from server.repository.repo_connection import configuration_collection


async def add_configuration(configuration_data: ModelConfigurationSchema):
    if hasattr(configuration_data, "id"):
        delattr(configuration_data, "id")
    configuration = await configuration_collection.insert_one(
        configuration_data.dict(by_alias=True)
    )
    configuration_data.id = configuration.inserted_id
    return configuration_data


async def retrieve_all_configurations():
    configurations = []
    async for configuration in configuration_collection.find():
        configurations.append(ModelConfigurationSchema(**configuration))
    return {"configurations": configurations}


async def retrieve_configuration_by_id(id: str):
    configuration = await configuration_collection.find_one({"_id": ObjectId(id)})
    if configuration:
        configuration = ModelConfigurationSchema(**configuration)
        return {"configuration": configuration}


async def update_configuration(id: str, configuration: UpdateModelConfigurationModel):
    configuration = {k: v for k, v in configuration.dict().items() if v is not None}

    if len(configuration) >= 1:
        result = await configuration_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": configuration}
        )

        if result.modified_count == 1:
            configuration = await configuration_collection.find_one(
                {"_id": ObjectId(id)}
            )
            configuration = ModelConfigurationSchema(**configuration)
            if configuration:
                return configuration

    if (
        existing := configuration_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return existing


async def delete_configuration(id: str):
    if (
        configuration := configuration_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        await configuration_collection.delete_one({"_id": ObjectId(id)})
        return True


async def delete_configurations(ids: list):
    if len(ids) > 0:
        for count, value in enumerate(ids):
            ids[count] = ObjectId(value)
        configuration_collection.delete_many({"_id": {"$in": ids}})
        configuration = configuration_collection.find({"_id": {"$in": ids}})
        if configuration:
            return True
