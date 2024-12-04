from fastapi import FastAPI
from routers import users, institutions, sessions, slots

app = FastAPI()

# Include routes
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(institutions.router, prefix="/api/v1", tags=["Institutions"])
app.include_router(sessions.router, prefix="/api/v1", tags=["Sessions"])
app.include_router(slots.router, prefix="/api/v1", tags=["Slots"])
