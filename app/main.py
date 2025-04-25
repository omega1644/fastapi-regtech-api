# ============================================================
# app/main.py
# ============================================================
from fastapi import FastAPI
from app.api.routes import auth, verifications, admin, health
from app.api.deps import startup_mongo

app = FastAPI(title="RegTech Verifier demo (Mongo)")

# initialise mongo on startup
@app.on_event("startup")
async def on_startup():
    await startup_mongo()

app.include_router(auth.router)
app.include_router(verifications.router)
app.include_router(admin.router)
app.include_router(health.router)
