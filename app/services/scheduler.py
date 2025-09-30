from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Iterable, List, Sequence

from .. import database
from ..models import (
    AvailabilityQuery,
    Order,
    Professional,
    ScheduleRequest,
    ScheduleResponse,
    ScheduleSlot,
    Weekday,
)


def _combine_datetime(day: date, start_time: time, end_time: time) -> tuple[datetime, datetime]:
    start_dt = datetime.combine(day, start_time)
    end_dt = datetime.combine(day, end_time)
    return start_dt, end_dt


def _weekday_matches(day: date, weekdays: Sequence[Weekday] | None) -> bool:
    if not weekdays:
        return True
    weekday_enum = Weekday.from_python_weekday(day.weekday())
    return weekday_enum in weekdays


def _iter_days(start_date: date, end_date: date) -> Iterable[date]:
    current = start_date
    while current <= end_date:
        yield current
        current = current + timedelta(days=1)


def _professional_schedules(professional_id: int) -> List[ScheduleSlot]:
    return [slot for slot in database.list_schedules() if slot.professional_id == professional_id]


def _overlaps(slot: ScheduleSlot, start: datetime, end: datetime) -> bool:
    return not (slot.end <= start or slot.start >= end)


def find_available_professionals(query: AvailabilityQuery) -> List[Professional]:
    professionals = [
        p
        for p in database.list_professionals()
        if p.profession.lower() == query.profession.lower()
        and p.region.lower() == query.region.lower()
    ]

    available = []
    for professional in professionals:
        slots = _professional_schedules(professional.id)
        if _is_professional_available(slots, query):
            available.append(professional)
    return available


def _is_professional_available(slots: List[ScheduleSlot], query: AvailabilityQuery) -> bool:
    for day in _iter_days(query.start_date, query.end_date):
        day_start, day_end = _combine_datetime(day, query.start_time, query.end_time)
        if any(_overlaps(slot, day_start, day_end) for slot in slots):
            return False
    return True


def create_schedule(request: ScheduleRequest) -> ScheduleResponse:
    order = database.get_order(request.order_id)
    if not order:
        raise ValueError(f"Order {request.order_id} not found")

    professionals = find_available_professionals(
        AvailabilityQuery(
            start_date=request.start_date,
            end_date=request.end_date,
            start_time=request.start_time,
            end_time=request.end_time,
            profession=request.profession,
            region=request.region,
        )
    )

    professional: Professional | None = None

    if request.professional_id:
        professional = database.get_professional(request.professional_id)
        if not professional:
            raise ValueError(f"Professional {request.professional_id} not found")
        if professional not in professionals:
            raise ValueError("The selected professional is not available for the requested period")
    else:
        professional = professionals[0] if professionals else None

    if not professional:
        raise ValueError("No professionals available for the requested period")

    created_slots: List[ScheduleSlot] = []
    for day in _iter_days(request.start_date, request.end_date):
        if not _weekday_matches(day, request.weekdays):
            continue
        start_dt, end_dt = _combine_datetime(day, request.start_time, request.end_time)
        # Ensure availability hasn't changed between iterations
        existing_slots = _professional_schedules(professional.id)
        if any(_overlaps(slot, start_dt, end_dt) for slot in existing_slots):
            raise ValueError("Professional is no longer available for one of the requested slots")
        created_slots.append(database.add_schedule(order.id, professional.id, start_dt, end_dt))

    if not created_slots:
        raise ValueError("The schedule request did not produce any time slots")

    return ScheduleResponse(created_slots=created_slots, professional=professional, order=order)
