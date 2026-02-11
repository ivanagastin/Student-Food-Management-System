from app.database import SessionLocal, engine, Base
from app import models
from app.routers import auth

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # check if plans exist
    # Define plans with updated prices (x30 days)
    plans_data = [
        {"name": "Full Meal Plan", "price": 4500.0, "desc": "Breakfast, Lunch, and Dinner"},
        {"name": "Breakfast Only", "price": 1500.0, "desc": "Daily healthy breakfast"},
        {"name": "Lunch Only", "price": 1800.0, "desc": "Nutritious lunch options"},
        {"name": "Dinner Only", "price": 1800.0, "desc": "Light and heavy dinner options"},
        {"name": "Lunch & Dinner", "price": 3000.0, "desc": "Skip breakfast, enjoy the rest"}
    ]

    print("Updating/Creating plans...")
    for p_data in plans_data:
        plan = db.query(models.FoodPlan).filter(models.FoodPlan.name == p_data["name"]).first()
        if plan:
            # Update existing
            plan.price_monthly = p_data["price"]
            plan.description = p_data["desc"]
        else:
            # Create new
            new_plan = models.FoodPlan(
                name=p_data["name"], 
                price_monthly=p_data["price"], 
                description=p_data["desc"]
            )
            db.add(new_plan)
    
    db.commit()
    

    # Check if admin exists
    admin = db.query(models.User).filter(models.User.username == "admin").first()
    if not admin:
        print("Creating admin user (admin/admin)...")
        hashed_pw = auth.get_password_hash("admin")
        admin_user = models.User(username="admin", hashed_password=hashed_pw, role="admin")
        db.add(admin_user)
        db.commit()

    # Check if staff exists
    staff = db.query(models.User).filter(models.User.username == "staff").first()
    if not staff:
        print("Creating staff user (staff/staff)...")
        hashed_pw = auth.get_password_hash("staff")
        staff_user = models.User(username="staff", hashed_password=hashed_pw, role="staff")
        db.add(staff_user)
        db.commit()

    # Create dummy student
    student = db.query(models.User).filter(models.User.username == "student").first()
    if not student:
        print("Creating student user (student/student)...")
        hashed_pw = auth.get_password_hash("student")
        student_user = models.User(
            username="student", 
            hashed_password=hashed_pw, 
            role="student",
            roll_no="2024-CS-001",
            full_name="John Doe"
        )
        db.add(student_user)
        db.commit()

    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
