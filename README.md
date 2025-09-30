# Programador de servicios

Este prototipo implementa un servicio REST sencillo para programar órdenes de servicios con profesionales disponibles.

## Características principales

- Listado de órdenes disponibles con la información necesaria para seleccionar la orden a programar.
- Listado de profesionales con su región y profesión.
- Endpoints para consultar disponibilidad de profesionales filtrando por fechas, horarios, profesión y regional.
- Creación de programaciones individuales o en serie indicando los días de la semana entre las fechas establecidas.
- Validaciones básicas para evitar traslapes de turnos en el calendario de cada profesional.
- Datos de ejemplo cargados en memoria para probar rápidamente el flujo de programación.

## Requisitos

- Python 3.11+
- Dependencias definidas en `requirements.txt`

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

## Ejecución

Ejecuta la API utilizando Uvicorn:

```bash
uvicorn app.main:app --reload
```

La documentación automática de la API estará disponible en `http://127.0.0.1:8000/docs`.

## Endpoints disponibles

| Método | Ruta | Descripción |
| --- | --- | --- |
| `GET` | `/orders` | Lista las órdenes de servicio disponibles. |
| `GET` | `/professionals` | Lista los profesionales registrados. |
| `GET` | `/schedules` | Consulta todas las programaciones realizadas. |
| `POST` | `/availability` | Consulta profesionales disponibles según filtros de fecha, hora, región y profesión. |
| `POST` | `/schedules` | Crea nuevas programaciones individuales o seriadas. |

### Ejemplo de solicitud para `/availability`

```json
{
  "start_date": "2024-05-01",
  "end_date": "2024-05-05",
  "start_time": "08:00",
  "end_time": "12:00",
  "profession": "Enfermera",
  "region": "Centro"
}
```

### Ejemplo de solicitud para `/schedules`

```json
{
  "order_id": 1,
  "start_date": "2024-05-01",
  "end_date": "2024-05-10",
  "start_time": "08:00",
  "end_time": "10:00",
  "profession": "Enfermera",
  "region": "Centro",
  "weekdays": ["monday", "wednesday", "friday"],
  "professional_id": 1
}
```

Si no se especifica `professional_id`, el sistema seleccionará automáticamente el primer profesional disponible que cumpla con los criterios.

## Próximos pasos sugeridos

- Persistir la información en una base de datos real.
- Implementar autenticación y roles de usuarios administradores.
- Conectar con calendarios externos (Google Calendar, Outlook) para sincronizar los eventos programados.
- Incorporar interfaz web para administración visual de la malla de turnos.
