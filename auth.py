"""
auth.py — Cyber-SH Authentication Module (v1.5.0)

Fixes applied vs v1.4.1:
  1. Lazy Supabase init — no crash at startup if env vars missing
  2. GitHub OAuth — correct sign_in_with_oauth + exchange_code_for_session flow
  3. Auth tokens via Authorization: Bearer headers (not query params)
  4. get_user() correctly accesses .user attribute
  5. get_current_user() / get_optional_user() FastAPI dependencies
  6. Forgot-password endpoint
  7. Error messages sanitised — no internal detail leakage
  8. FIX: sign_out(token) → sign_out() — wrong supabase-py v2 signature
  9. FIX: reset_password_email → reset_password_for_email — method didn't exist
 10. Added structured logging throughout
"""

from __future__ import annotations

import logging
import os

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = logging.getLogger("cybersh.auth")

# ─────────────────────────────────────────────
#  SUPABASE SETUP — lazy init
# ─────────────────────────────────────────────

SUPABASE_URL      = os.getenv("SUPABASE_URL", "")
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
        logger.info("Supabase client initialised successfully.")
        return _supabase_client
    except Exception as exc:
        logger.exception("Failed to initialise Supabase client.")
        raise HTTPException(status_code=503, detail="Authentication service unavailable.") from exc


# ─────────────────────────────────────────────
#  BEARER TOKEN DEPENDENCY
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
    FastAPI dependency. Validates a JWT from the Authorization header.
    Returns the Supabase user object, or raises HTTP 401.

    Usage:
        @app.get("/api/protected")
        def protected(user = Depends(get_current_user)):
            ...
    """
    token = _extract_bearer(authorization)
    supabase = _get_supabase()
    try:
        result = supabase.auth.get_user(token)
        if not result or not result.user:
            raise HTTPException(status_code=401, detail="Invalid or expired token.")
        return result.user
    except HTTPException:
        raise
    except Exception:
        logger.debug("get_user() failed — token may be expired or invalid.")
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
        After GitHub approval, Supabase redirects back with a ?code= parameter.
        """
        supabase = _get_supabase()
        try:
            opts: dict = {}
            if redirect_to:
                opts["redirect_to"] = redirect_to
            response = supabase.auth.sign_in_with_oauth(
                {"provider": "github", "options": opts}
            )
            return {"success": True, "url": response.url}
        except Exception as exc:
            logger.warning("GitHub OAuth URL generation failed: %s", exc)
            raise HTTPException(status_code=400, detail="Failed to generate OAuth URL.")

    # ── GitHub OAuth — Step 2: exchange code for session ───────────────────
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
            logger.warning("GitHub OAuth code exchange failed.")
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
            if not response.user:
                raise HTTPException(status_code=400, detail="Sign up failed. Email may already be in use.")
            return {
                "success": True,
                "user": {"id": response.user.id, "email": response.user.email},
                "message": "Check your email to confirm your account.",
            }
        except HTTPException:
            raise
        except Exception:
            logger.warning("Sign up failed for email: %s", request.email[:5] + "***")
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
            logger.debug("Login failed for email: %s", request.email[:5] + "***")
            raise HTTPException(status_code=401, detail="Invalid email or password.")

    # ── Get Current User ────────────────────────────────────────────────────
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
            user = result.user
            if not user:
                raise HTTPException(status_code=401, detail="Invalid or expired token.")
            return {
                "success": True,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "user_metadata": user.user_metadata or {},
                },
            }
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired token.")

    # ── Logout ──────────────────────────────────────────────────────────────
    @app.post("/auth/logout")
    async def logout(authorization: str | None = Header(default=None)):
        """
        Sign out. Pass JWT as Authorization: Bearer <token>

        Note: supabase-py v2 sign_out() invalidates the server-side session.
        The client should also discard both access_token and refresh_token.
        """
        _extract_bearer(authorization)  # validate header is present and well-formed
        supabase = _get_supabase()
        try:
            # FIX: sign_out() takes no positional token arg in supabase-py v2
            supabase.auth.sign_out()
        except Exception:
            pass  # best-effort; client must discard tokens regardless
        return {"success": True, "message": "Logged out successfully."}

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
            # FIX: was reset_password_email (doesn't exist) → reset_password_for_email
            opts: dict = {}
            if request.redirect_to:
                opts["redirect_to"] = request.redirect_to
            supabase.auth.reset_password_for_email(
                request.email,
                options=opts if opts else None,
            )
        except Exception:
            pass  # intentional: never reveal whether the email exists
        # Always return the same response to prevent user enumeration
        return {"success": True, "message": "If that email exists, a reset link has been sent."}

    # ── Health Check ────────────────────────────────────────────────────────
    @app.get("/auth/health")
    async def auth_health():
        """Check if the authentication service is configured."""
        configured = bool(SUPABASE_URL and SUPABASE_ANON_KEY)
        return {
            "status": "ok" if configured else "unconfigured",
            "auth": "enabled" if configured else "disabled",
            "providers": ["github", "email"] if configured else [],
        }
