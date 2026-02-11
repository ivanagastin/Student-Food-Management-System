from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import List
from .. import models, schemas, database
from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

def check_admin(user: models.User):
    if user.role != models.Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

@router.post("/menus", response_model=schemas.MenuResponse)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    check_admin(current_user)
    db_menu = db.query(models.Menu).filter(models.Menu.date == menu.date).first()
    if db_menu:
        # Update existing
        db_menu.breakfast_items = menu.breakfast_items
        db_menu.lunch_items = menu.lunch_items
        db_menu.dinner_items = menu.dinner_items
        db.commit()
        db.refresh(db_menu)
        return db_menu
    
    new_menu = models.Menu(**menu.dict())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu

@router.get("/menus/{date_str}", response_model=schemas.MenuResponse)
def get_menu(date_str: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    check_admin(current_user)
    # date_str format YYYY-MM-DD
    menu = db.query(models.Menu).filter(models.Menu.date == date_str).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu

@router.get("/students", response_model=List[schemas.StudentAdminView])
def get_all_students(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    check_admin(current_user)
    students = db.query(models.User).filter(models.User.role == models.Role.STUDENT).all()
    
    # Enrich with active subscription and attendance
    results = []
    today = date.today()
    
    for s in students:
        active_sub = db.query(models.Subscription).filter(
            models.Subscription.user_id == s.id,
            models.Subscription.status == "active"
        ).first()
        
        # Check attendance
        attendance = db.query(models.DailyAttendance).filter(
            models.DailyAttendance.user_id == s.id,
            models.DailyAttendance.date == today
        ).first()
        is_present = attendance.is_present if attendance else False
        
        sub_data = None
        if active_sub:
            sub_data = active_sub
            # Inject plan name manually or ensure relationship is loaded
            sub_data.plan_name = active_sub.plan.name if active_sub.plan else "Unknown Plan"

        # Create StudentAdminView using Pydantic's from_attributes (orm_mode)
        s_data = schemas.StudentAdminView(
            id=s.id,
            username=s.username,
            role=s.role,
            roll_no=s.roll_no,
            full_name=s.full_name,
            is_present_today=is_present,
            subscription=sub_data
        )
        results.append(s_data)
        
    return results

@router.post("/subscriptions/{sub_id}/cancel")
def cancel_subscription(sub_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    check_admin(current_user)
    sub = db.query(models.Subscription).filter(models.Subscription.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    sub.status = "cancelled"
    db.commit()
    return {"message": "Subscription cancelled successfully"}
