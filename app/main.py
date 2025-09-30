from __future__ import annotations

from fastapi import FastAPI, HTTPException

from . import database
from .models import AvailabilityQuery, ScheduleRequest
from .services.scheduler import create_schedule, find_available_professionals

app = FastAPI(title="ERP Servicio - Programador de Turnos")


@app.get("/orders")
def list_orders():
    return database.list_orders()


@app.get("/professionals")
def list_professionals():
    return database.list_professionals()


@app.get("/schedules")
def list_schedules():
    return database.list_schedules()


@app.post("/availability")
def availability(query: AvailabilityQuery):
    return find_available_professionals(query)


@app.post("/schedules")
def schedule_service(request: ScheduleRequest):
    try:
        return create_schedule(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
