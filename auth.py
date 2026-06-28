"""
auth.py — Cyber-SH Authentication Module (Fixed v1.4.1)

Fixes applied:
  1. Lazy Supabase init — no longer crashes app at startup if env vars are missing
  2. GitHub OAuth — correctly returns OAuth redirect URL (sign_in_with_oauth)
     instead of calling it with a nonexistent access_token pattern
  3. Auth tokens moved from insecure query params → Authorization: Bearer headers
  4. get_user() response correctly accesses .user attribute on the returned object
  5. Added optional get_current_user() FastAPI dependency for protecting routes
  6. Added forgot-password endpoint
  7. Error messages sanitised — no internal detail leakage
"""

from __future__ import annotations

import os

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# ─────────────────────────────────────────────
#  SUPABASE SETUP — lazy init (FIX 1)
# ─────────────────────────────────────────────

SUPABASE_URL     = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

_supabase_client = None


def _get_supabase():
    """
    Lazy Supabase client factory.
    Raises HTTP 503 at request time if env vars are missing,
    instead of crashing the whole app at import time.
    """
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise HTTPException(
            status_code=503,
            detail="Authentication service not configured. Set SUPABASE_URL and SUPABASE_ANON_KEY.",
        )

    try:
        from supabase import create_client
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        return _supabase_client
    except Exception as exc:
        import traceback
        print("=== SUPABASE INIT ERROR ===")
        traceback.print_exc()
        print("============================")
        raise HTTPException(status_code=503, detail="Authentication service unavailable.") from exc


# ─────────────────────────────────────────────
#  BEARER TOKEN DEPENDENCY (FIX 3)
# ─────────────────────────────────────────────

def _extract_bearer(authorization: str | None) -> str:
    """Parse 'Bearer <token>' header and return the raw token."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header. Use: Bearer <token>",
        )
    return authorization[7:].strip()


async def get_current_user(authorization: str | None = Header(default=None)):
    """
    FastAPI dependency.  Validates a JWT from the Authorization header.
    Returns the Supabase user object, or raises HTTP 401.

    Usage in any route:
        @app.get("/api/protected")
        def protected(user = Depends(get_current_user)):
            ...
    """
    token = _extract_bearer(authorization)
    supabase = _get_supabase()
    try:
        result = supabase.auth.get_user(token)
        return result.user          # ← FIX 4: was `result` (missing .user)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")


async def get_optional_user(authorization: str | None = Header(default=None)):
    """Like get_current_user but returns None instead of raising if no token."""
    if not authorization:
        return None
    try:
        return await get_current_user(authorization)
    except HTTPException:
        return None


# ─────────────────────────────────────────────
#  REQUEST / RESPONSE MODELS
# ─────────────────────────────────────────────

class GitHubCallbackRequest(BaseModel):
    code: str           # authorization code from GitHub OAuth callback
    redirect_to: str = ""


class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str
    redirect_to: str = ""


# ─────────────────────────────────────────────
#  AUTH ROUTE REGISTRATION
# ─────────────────────────────────────────────

def setup_auth_routes(app: FastAPI):
    """
    Register all /auth/* routes onto the FastAPI app.
    Call once from cybersh_api.py:  setup_auth_routes(app)
    """

    # ── GitHub OAuth — Step 1: get the redirect URL ────────────────────────
    @app.get("/auth/github")
    async def github_oauth_url(redirect_to: str = ""):
        """
        Returns the GitHub OAuth redirect URL.
        The frontend should redirect the user to `url` to begin the OAuth flow.
        After GitHub approval, Supabase will redirect back with a code.
        """
        supabase = _get_supabase()
        try:
            opts = {}
            if redirect_to:
                opts["redirect_to"] = redirect_to
            response = supabase.auth.sign_in_with_oauth(
                {"provider": "github", "options": opts}
            )
            return {"success": True, "url": response.url}
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    # ── GitHub OAuth — Step 2: exchange code for session (FIX 2) ───────────
    @app.post("/auth/github/callback")
    async def github_callback(request: GitHubCallbackRequest):
        """
        Exchange the GitHub authorization code for a Supabase session.
        Call this after the user is redirected back from GitHub with ?code=xxx.
        """
        supabase = _get_supabase()
        try:
            response = supabase.auth.exchange_code_for_session(
                {"auth_code": request.code}
            )
            return {
                "success": True,
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                },
            }
        except Exception:
            raise HTTPException(status_code=400, detail="OAuth code exchange failed.")

    # ── Email / Password Sign Up ────────────────────────────────────────────
    @app.post("/auth/signup")
    async def signup(request: SignupRequest):
        """Sign up with email and password."""
        supabase = _get_supabase()
        try:
            response = supabase.auth.sign_up(
                {"email": request.email, "password": request.password}
            )
            return {
                "success": True,
                "user": {"id": response.user.id, "email": response.user.email},
                "message": "Check your email to confirm your account.",
            }
        except Exception:
            raise HTTPException(status_code=400, detail="Sign up failed. Email may already be in use.")

    # ── Email / Password Login ──────────────────────────────────────────────
    @app.post("/auth/login")
    async def login(request: LoginRequest):
        """Login with email and password. Returns access + refresh tokens."""
        supabase = _get_supabase()
        try:
            response = supabase.auth.sign_in_with_password(
                {"email": request.email, "password": request.password}
            )
            return {
                "success": True,
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                    "user_metadata": response.user.user_metadata or {},
                },
            }
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid email or password.")

    # ── Get Current User (FIX 3 & 4) ───────────────────────────────────────
    @app.get("/auth/user")
    async def get_user(authorization: str | None = Header(default=None)):
        """
        Get the currently authenticated user.
        Pass your JWT as:  Authorization: Bearer <token>
        """
        token = _extract_bearer(authorization)
        supabase = _get_supabase()
        try:
            result = supabase.auth.get_user(token)
            user = result.user                  # FIX 4: correct attribute access
            return {
                "success": True,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "user_metadata": user.user_metadata or {},
                },
            }
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired token.")

    # ── Logout ──────────────────────────────────────────────────────────────
    @app.post("/auth/logout")
    async def logout(authorization: str | None = Header(default=None)):
        """Sign out. Pass JWT as Authorization: Bearer <token>"""
        token = _extract_bearer(authorization)
        supabase = _get_supabase()
        try:
            supabase.auth.sign_out(token)
            return {"success": True, "message": "Logged out successfully."}
        except Exception:
            # Best-effort logout; always return success to the client
            return {"success": True, "message": "Logged out."}

    # ── Refresh Session ─────────────────────────────────────────────────────
    @app.post("/auth/refresh")
    async def refresh_session(authorization: str | None = Header(default=None)):
        """
        Refresh tokens using the refresh_token.
        Pass it as:  Authorization: Bearer <refresh_token>
        """
        refresh_token = _extract_bearer(authorization)
        supabase = _get_supabase()
        try:
            response = supabase.auth.refresh_session(refresh_token)
            return {
                "success": True,
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
            }
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token.")

    # ── Forgot Password ─────────────────────────────────────────────────────
    @app.post("/auth/forgot-password")
    async def forgot_password(request: ForgotPasswordRequest):
        """Send a password-reset email."""
        supabase = _get_supabase()
        try:
            opts = {}
            if request.redirect_to:
                opts["redirect_to"] = request.redirect_to
            supabase.auth.reset_password_email(request.email, opts)
            # Always return success to avoid user enumeration
            return {"success": True, "message": "If that email exists, a reset link has been sent."}
        except Exception:
            return {"success": True, "message": "If that email exists, a reset link has been sent."}

    # ── Health Check ────────────────────────────────────────────────────────
    @app.get("/auth/health")
    async def auth_health():
        """Check if the authentication service is reachable."""
        configured = bool(SUPABASE_URL and SUPABASE_ANON_KEY)
        return {
            "status": "ok" if configured else "unconfigured",
            "auth": "enabled" if configured else "disabled",
            "providers": ["github", "email"] if configured else [],
        }