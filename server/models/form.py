from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class FormSchema(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    applicantName: str = Field(...)
    applicantIc: str = Field(...)
    phoneNumber: str = Field(...)
    email: EmailStr = Field(...)
    correspondenceAddress: str = Field(...)
    businessAddress: str = Field(...)
    loanStatus: str = Field(...)
    applicationType: str = Field(...)
    loanAmount: float = Field(...)
    loanTerm: int = Field(...)
    interestRate: float = Field(...)
    companyName: str = Field(...)
    coreBusinessType: str = Field(...)
    staffNumber: int = Field(...)
    lastTotalSales: float = Field(...)
    premiseType: str = Field(...)
    collateralType: str = Field(...)
    collateralValue: float = Field(...)
    currBankAccBalance: float = Field(...)
    totalOutstandingLoan: float = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class UpdateFormModel(BaseModel):
    applicantName: Optional[str]
    applicantIc: Optional[str]
    phoneNumber: Optional[str]
    email: Optional[EmailStr]
    correspondenceAddress: Optional[str]
    businessAddress: Optional[str]
    loanStatus: Optional[str]
    applicationType: Optional[str]
    loanAmount: Optional[float]
    loanTerm: Optional[int]
    companyName: Optional[str]
    coreBusinessType: Optional[str]
    staffNumber: Optional[int]
    lastTotalSales: Optional[float]
    premiseType: Optional[str]
    collatetional: Optional[str]
    collateralValue: Optional[float]
    currBankAccBalance: Optional[float]
    totalOutstandingLoan: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
