from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date
from .database import engine, Base, get_db
from . import models
from .routers import auth, admin, student, staff

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Food Management System")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# templates
templates = Jinja2Templates(directory="templates")

# include routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(student.router)
app.include_router(staff.router)

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    # Get today's menu
    today = date.today()
    menu = db.query(models.Menu).filter(models.Menu.date == today).first()
    
    # Get active plans
    plans = db.query(models.FoodPlan).filter(models.FoodPlan.is_active == True).all()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "menu": menu,
        "plans": plans
    })

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard/student")
def student_dashboard(request: Request):
    return templates.TemplateResponse("dashboard_student.html", {"request": request})

@app.get("/dashboard/admin")
def admin_dashboard(request: Request):
    return templates.TemplateResponse("dashboard_admin.html", {"request": request})

@app.get("/dashboard/staff")
def staff_dashboard(request: Request):
    return templates.TemplateResponse("dashboard_staff.html", {"request": request})
