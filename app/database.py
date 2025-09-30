from __future__ import annotations

from datetime import datetime, timedelta
from itertools import count
from typing import Dict, List

from .models import Order, Professional, ScheduleSlot


_professionals: Dict[int, Professional] = {
    1: Professional(id=1, full_name="Ana Gómez", profession="Enfermera", region="Centro"),
    2: Professional(id=2, full_name="Luis Martínez", profession="Fisioterapeuta", region="Centro"),
    3: Professional(id=3, full_name="Laura Pérez", profession="Enfermera", region="Norte"),
    4: Professional(id=4, full_name="Carlos Ruiz", profession="Fisioterapeuta", region="Norte"),
    5: Professional(id=5, full_name="María Silva", profession="Enfermera", region="Centro"),
}

_orders: Dict[int, Order] = {
    1: Order(
        id=1,
        code="ORD-001",
        client="Clínica Central",
        service="Cuidado domiciliario",
        region="Centro",
        profession_required="Enfermera",
        details="Paciente postoperatorio con visitas diarias.",
    ),
    2: Order(
        id=2,
        code="ORD-002",
        client="Hospital del Norte",
        service="Terapia física",
        region="Norte",
        profession_required="Fisioterapeuta",
        details="Sesiones de rehabilitación tres veces por semana.",
    ),
}

_schedules: Dict[int, ScheduleSlot] = {}
_schedule_id_seq = count(1)


def list_professionals() -> List[Professional]:
    return list(_professionals.values())


def list_orders() -> List[Order]:
    return list(_orders.values())


def get_order(order_id: int) -> Order | None:
    return _orders.get(order_id)


def get_professional(professional_id: int) -> Professional | None:
    return _professionals.get(professional_id)


def list_schedules() -> List[ScheduleSlot]:
    return list(_schedules.values())


def add_schedule(order_id: int, professional_id: int, start: datetime, end: datetime) -> ScheduleSlot:
    schedule_id = next(_schedule_id_seq)
    slot = ScheduleSlot(
        id=schedule_id,
        order_id=order_id,
        professional_id=professional_id,
        start=start,
        end=end,
    )
    _schedules[schedule_id] = slot
    return slot


def remove_future_data() -> None:
    """Utility to clear schedules during tests."""

    _schedules.clear()
    global _schedule_id_seq
    _schedule_id_seq = count(1)
