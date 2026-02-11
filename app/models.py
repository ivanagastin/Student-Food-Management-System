from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class Role(str, enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"
    STAFF = "staff"

class MealTime(str, enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    role = Column(String(20), default=Role.STUDENT)
    hashed_password = Column(String(100), nullable=False)
    
    # New fields
    roll_no = Column(String(20), unique=True, nullable=True)
    full_name = Column(String(100), nullable=True)
    
    # Relationships
    subscriptions = relationship("Subscription", back_populates="student")
    attendance = relationship("DailyAttendance", back_populates="student")

class DailyAttendance(Base):
    __tablename__ = "daily_attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, nullable=False)
    is_present = Column(Boolean, default=False)

    student = relationship("User", back_populates="attendance")

class FoodPlan(Base):
    __tablename__ = "food_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)  # e.g., "Full Meal", "Breakfast Only"
    price_monthly = Column(Float, nullable=False)
    description = Column(String(200))
    is_active = Column(Boolean, default=True)

    subscriptions = relationship("Subscription", back_populates="plan")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("food_plans.id"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(20), default="active") # active, paused, cancelled
    
    student = relationship("User", back_populates="subscriptions")
    plan = relationship("FoodPlan", back_populates="subscriptions")

class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False)
    breakfast_items = Column(Text, nullable=True) # Stored as comma separated or JSON string
    lunch_items = Column(Text, nullable=True)
    dinner_items = Column(Text, nullable=True)
