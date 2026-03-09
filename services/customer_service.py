from fastapi import HTTPException
from faker import Faker
import random
from models.customer import Customer, Meter, UsageRecord
from datetime import date, timedelta

fake = Faker()

RATE_PLANS = ["Residential Standard", "Residential Time-of-Use", "Small Business", "Large Commercial", "Agricultural"]
SERVICE_STATUSES = ["Active", "Active", "Active", "Suspended", "Inactive"]
METER_TYPES = ["Smart Meter", "AMR", "Manual Read"]

# In-memory store — seeded deterministically per account number
_CUSTOMERS: dict[str, Customer] = {}
_METERS: dict[str, Meter] = {}


def _seed_customer(account_number: str) -> Customer:
    f = Faker()
    f.seed_instance(account_number)
    rng = random.Random(account_number)
    return Customer(
        account_number=account_number,
        name=f.name(),
        email=f.email(),
        phone=f.phone_number(),
        service_status=rng.choice(SERVICE_STATUSES),
        rate_plan=rng.choice(RATE_PLANS),
        account_since=f.date_between(start_date="-20y", end_date="-1y").isoformat(),
        balance_due=round(rng.uniform(-50, 500), 2),
    )


def _seed_meter(account_number: str) -> Meter:
    f = Faker()
    f.seed_instance(account_number + "-meter")
    rng = random.Random(account_number + "-meter")
    return Meter(
        meter_id=f.bothify(text="MTR-#######"),
        account_number=account_number,
        meter_type=rng.choice(METER_TYPES),
        last_read_kwh=round(rng.uniform(1000, 80000), 2),
        last_read_date=f.date_between(start_date="-30d", end_date="today").isoformat(),
    )


def _get_or_create(account_number: str) -> Customer:
    if account_number not in _CUSTOMERS:
        _CUSTOMERS[account_number] = _seed_customer(account_number)
        _METERS[account_number] = _seed_meter(account_number)
    return _CUSTOMERS[account_number]


# Pre-seed 20 customers
for i in range(1, 21):
    acct = f"ELEC-{i:06d}"
    _get_or_create(acct)


async def get_customer(account_number: str) -> Customer:
    customer = _CUSTOMERS.get(account_number.upper())
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer {account_number} not found")
    return customer


async def list_customers(name: str | None, status: str | None, limit: int) -> list[Customer]:
    results = list(_CUSTOMERS.values())
    if name:
        results = [c for c in results if name.lower() in c.name.lower()]
    if status:
        results = [c for c in results if c.service_status.lower() == status.lower()]
    return results[:limit]


async def get_meter(account_number: str) -> Meter:
    _get_or_create(account_number.upper())
    meter = _METERS.get(account_number.upper())
    if not meter:
        raise HTTPException(status_code=404, detail="Meter not found")
    return meter


async def get_usage(account_number: str, months: int) -> list[UsageRecord]:
    _get_or_create(account_number.upper())
    rng = random.Random(account_number)
    records = []
    for m in range(months):
        read_date = (date.today().replace(day=1) - timedelta(days=m * 30)).isoformat()
        kwh = round(rng.uniform(200, 1500), 2)
        records.append(UsageRecord(
            read_date=read_date,
            kwh_used=kwh,
            cost=round(kwh * 0.13, 2),  # $0.13/kWh
        ))
    return records
