from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from enum import Enum

class Role(str, Enum):
    STUDENT = "student"
    ADMIN = "admin"
    STAFF = "staff"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: Role = Role.STUDENT

class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

class FoodPlanBase(BaseModel):
    name: str
    price_monthly: float
    description: Optional[str] = None

class FoodPlanCreate(FoodPlanBase):
    pass

class FoodPlanResponse(FoodPlanBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class MenuBase(BaseModel):
    date: date
    breakfast_items: Optional[str] = None
    lunch_items: Optional[str] = None
    dinner_items: Optional[str] = None

class MenuCreate(MenuBase):
    pass

class MenuResponse(MenuBase):
    id: int
    
    class Config:
        from_attributes = True

class SubscriptionCreate(BaseModel):
    plan_id: int
    start_date: date
    end_date: date

class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan_id: int
    status: str
    start_date: date
    end_date: date
    
    class Config:
        from_attributes = True

class SubscriptionAdminDetails(SubscriptionResponse):
    plan_name: str

class StudentAdminView(UserResponse):
    roll_no: Optional[str] = None
    full_name: Optional[str] = None
    is_present_today: bool = False
    subscription: Optional[SubscriptionAdminDetails] = None
