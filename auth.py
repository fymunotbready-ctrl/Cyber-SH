
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from supabase import create_client, Client

# ─────────────────────────────────────────────
#  SUPABASE SETUP
# ─────────────────────────────────────────────

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_ANON_KEY environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# ─────────────────────────────────────────────
#  REQUEST/RESPONSE MODELS
# ─────────────────────────────────────────────

class GitHubAuthRequest(BaseModel):
    access_token: str

class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    user_metadata: dict = {}

# ─────────────────────────────────────────────
#  AUTHENTICATION ENDPOINTS
# ─────────────────────────────────────────────

def setup_auth_routes(app: FastAPI):
    """
    Setup authentication routes for Cyber-SH
    Call this in your main app: setup_auth_routes(app)
    """
    
    # ✅ GitHub OAuth Login
    @app.post("/auth/github/login")
    async def github_login(request: GitHubAuthRequest):
        """
        Login with GitHub OAuth token
        Frontend should get the token from GitHub OAuth flow
        """
        try:
            # Sign in with GitHub OAuth provider
            response = supabase.auth.sign_in_with_oauth(
                provider="github",
                options={"redirect_to": f"{SUPABASE_URL}/auth/v1/callback"}
            )
            return {
                "success": True,
                "user": response.user,
                "session": response.session
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    # ✅ Email/Password Sign Up
    @app.post("/auth/signup")
    async def signup(request: SignupRequest):
        """
        Sign up with email and password
        """
        try:
            response = supabase.auth.sign_up({
                "email": request.email,
                "password": request.password
            })
            return {
                "success": True,
                "user": response.user,
                "message": "Check your email to confirm signup"
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    # ✅ Email/Password Login
    @app.post("/auth/login")
    async def login(request: LoginRequest):
        """
        Login with email and password
        """
        try:
            response = supabase.auth.sign_in_with_password({
                "email": request.email,
                "password": request.password
            })
            return {
                "success": True,
                "user": response.user,
                "session": response.session
            }
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ Get Current User
    @app.get("/auth/user")
    async def get_user(token: str = Query(...)):
        """
        Get current authenticated user
        Pass JWT token as query parameter
        """
        try:
            user = supabase.auth.get_user(token)
            return {
                "success": True,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "user_metadata": user.user_metadata or {}
                }
            }
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

    # ✅ Logout (Sign Out)
    @app.post("/auth/logout")
    async def logout(token: str = Query(...)):
        """
        Sign out and invalidate session
        """
        try:
            supabase.auth.sign_out(token)
            return {
                "success": True,
                "message": "Logged out successfully"
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    # ✅ Refresh Session
    @app.post("/auth/refresh")
    async def refresh_session(refresh_token: str = Query(...)):
        """
        Refresh JWT token using refresh token
        """
        try:
            response = supabase.auth.refresh_session(refresh_token)
            return {
                "success": True,
                "session": response.session
            }
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    # ✅ Health Check
    @app.get("/auth/health")
    async def auth_health():
        """
        Check if authentication service is working
        """
        return {
            "status": "ok",
            "auth": "enabled",
            "providers": ["github", "email"]
        }
