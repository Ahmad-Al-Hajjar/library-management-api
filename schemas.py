from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
class UserRequest(BaseModel):
    name :str = Field(min_length=4)
    user_name :str = Field(min_length=4)
    password :str = Field(min_length=8)
    amount :Decimal = Field(ge=0)
    is_admin :bool =False 

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id :int
    name :str
    user_name :str
    amount :Decimal

class BookRequest(BaseModel):
    name : str = Field(min_length=1)
    author : str = Field(min_length=1)
    copies : int = Field(ge=0)
    cost : Decimal = Field(ge=0)


class BookUpdate(BaseModel):
    name : str
    author : str
    copies : int
    cost : Decimal   
 
class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    name : str
    author : str
    copies : int
    cost : Decimal



class BorrowRequest(BaseModel):
    book_id : int

class ReturnRequest(BaseModel):
    book_id : int    



class LoginRequest(BaseModel):
    user_name : str
    password : str

class TokenResponse(BaseModel):
    access_token : str
    token_type : str    