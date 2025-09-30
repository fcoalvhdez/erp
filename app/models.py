from __future__ import annotations

from datetime import date, datetime, time
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class Weekday(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"

    @classmethod
    def from_python_weekday(cls, value: int) -> "Weekday":
        mapping = {
            0: cls.monday,
            1: cls.tuesday,
            2: cls.wednesday,
            3: cls.thursday,
            4: cls.friday,
            5: cls.saturday,
            6: cls.sunday,
        }
        return mapping[value]


class Order(BaseModel):
    id: int
    code: str
    client: str
    service: str
    region: str
    profession_required: str
    details: str


class Professional(BaseModel):
    id: int
    full_name: str
    profession: str
    region: str


class ScheduleSlot(BaseModel):
    id: int
    order_id: int
    professional_id: int
    start: datetime
    end: datetime


class AvailabilityQuery(BaseModel):
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    profession: str
    region: str

    @validator("end_date")
    def validate_dates(cls, value: date, values: dict[str, date]) -> date:
        start_date = values.get("start_date")
        if start_date and value < start_date:
            raise ValueError("end_date must be greater than or equal to start_date")
        return value

    @validator("end_time")
    def validate_times(cls, value: time, values: dict[str, time]) -> time:
        start_time = values.get("start_time")
        if start_time and value <= start_time:
            raise ValueError("end_time must be greater than start_time")
        return value


class ScheduleRequest(BaseModel):
    order_id: int
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    profession: str
    region: str
    weekdays: Optional[List[Weekday]] = Field(
        default=None,
        description="Days of week to schedule. If omitted, all days within the range are used.",
    )
    professional_id: Optional[int] = Field(
        default=None,
        description="Explicit professional assignment. If omitted, the first available professional is used.",
    )

    @validator("end_date")
    def validate_date_order(cls, value: date, values: dict[str, date]) -> date:
        start_date = values.get("start_date")
        if start_date and value < start_date:
            raise ValueError("end_date must be after start_date")
        return value

    @validator("end_time")
    def validate_time_order(cls, value: time, values: dict[str, time]) -> time:
        start_time = values.get("start_time")
        if start_time and value <= start_time:
            raise ValueError("end_time must be after start_time")
        return value


class ScheduleResponse(BaseModel):
    created_slots: List[ScheduleSlot]
    professional: Professional
    order: Order
