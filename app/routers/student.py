from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from .. import models, schemas, database
from .auth import get_current_user

router = APIRouter(prefix="/student", tags=["Student"])

@router.get("/menu/today", response_model=schemas.MenuResponse)
def get_todays_menu(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    today = date.today()
    menu = db.query(models.Menu).filter(models.Menu.date == today).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not set for today")
    return menu

@router.get("/plans", response_model=List[schemas.FoodPlanResponse])
def get_plans(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    plans = db.query(models.FoodPlan).filter(models.FoodPlan.is_active == True).all()
    return plans

@router.post("/subscribe", response_model=schemas.SubscriptionResponse)
def subscribe_to_plan(subscription: schemas.SubscriptionCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Check if already subscribed
    existing_sub = db.query(models.Subscription).filter(
        models.Subscription.user_id == current_user.id,
        models.Subscription.status == "active"
    ).first()
    
    if existing_sub:
        raise HTTPException(status_code=400, detail="You already have an active subscription")

    new_sub = models.Subscription(
        user_id=current_user.id,
        plan_id=subscription.plan_id,
        start_date=subscription.start_date,
        end_date=subscription.end_date,
        status="active"
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return new_sub

@router.get("/subscription", response_model=List[schemas.SubscriptionResponse])
def get_my_subscriptions(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    subs = db.query(models.Subscription).filter(models.Subscription.user_id == current_user.id).all()
    return subs
