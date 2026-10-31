"""
CLAIMSIGHT AI - Authentication API Endpoints
"""

import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from app.core.database import get_database
from app.auth.security import hash_password, verify_password, create_access_token, get_current_user
from app.schemas.auth import UserLogin, UserRegister, TokenResponse, UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin):
    db = get_database()
    user = db.users.find_one({"email": payload.email.lower()})
    if not user or not verify_password(payload.password, user.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Please verify your email and password."
        )

    token = create_access_token(
        data={"sub": user["user_id"], "email": user["email"], "role": user.get("role", "investigator")}
    )

    clean_user = {
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user["email"],
        "role": user.get("role", "investigator"),
        "department": user.get("department", "Claims Investigation")
    }

    return {"access_token": token, "token_type": "bearer", "user": clean_user}

@router.post("/register", response_model=TokenResponse)
def register(payload: UserRegister):
    db = get_database()
    existing = db.users.find_one({"email": payload.email.lower()})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

    user_id = f"usr-{int(datetime.datetime.now().timestamp() * 1000)}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    new_user = {
        "user_id": user_id,
        "name": payload.name,
        "email": payload.email.lower(),
        "password_hash": hash_password(payload.password),
        "role": payload.role if payload.role in ["admin", "investigator", "claimant"] else "investigator",
        "department": payload.department,
        "active": True,
        "created_at": now
    }
    db.users.insert_one(new_user)

    token = create_access_token(
        data={"sub": user_id, "email": new_user["email"], "role": new_user["role"]}
    )

    clean_user = {
        "user_id": user_id,
        "name": new_user["name"],
        "email": new_user["email"],
        "role": new_user["role"],
        "department": new_user["department"]
    }

    return {"access_token": token, "token_type": "bearer", "user": clean_user}

@router.get("/me")
def get_profile(current_user: dict = Depends(get_current_user)):
    return current_user

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(current_user: dict = Depends(get_current_user)):
    token = create_access_token(
        data={"sub": current_user["user_id"], "email": current_user["email"], "role": current_user.get("role", "investigator")}
    )
    return {"access_token": token, "token_type": "bearer", "user": current_user}

