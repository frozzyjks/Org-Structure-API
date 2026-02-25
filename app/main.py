from fastapi import FastAPI
from app.models import department, employee
from app.api.v1 import department as department_router
from app.api.v1 import employee as employee_router

app = FastAPI(title="Organizational Structure API")

app.include_router(department_router.router)
app.include_router(employee_router.router)


@app.get("/")
async def root():
    return {"message": "API is running"}