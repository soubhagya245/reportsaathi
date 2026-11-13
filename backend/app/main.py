from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import health, auth, lab_reports   # <-- add lab_reports
# other routers (if any) go here

app = FastAPI(title="ReportSaathi API", version="0.1.0")

# CORS – allow Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(lab_reports.router, prefix="/api")   # <-- new line

# No further changes needed – the backend will now serve the OCR & fixture endpoints.