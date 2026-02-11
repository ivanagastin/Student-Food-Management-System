from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    print("Hashing 'admin'...")
    h = pwd_context.hash("admin")
    print(f"Success: {h}")
except Exception as e:
    print(f"Error: {e}")
