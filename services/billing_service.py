from fastapi import HTTPException
from db import get_connection
from models.billing import Bill, Payment, PaymentRequest


async def get_bills(account_number: str, limit: int) -> list[Bill]:
    async with get_connection() as conn:
        cursor = conn.cursor()
        await cursor.execute(
            """
            SELECT bill_id, account_number,
                   TO_CHAR(bill_date, 'YYYY-MM-DD') AS bill_date,
                   TO_CHAR(due_date, 'YYYY-MM-DD') AS due_date,
                   amount_due, amount_paid, status
            FROM bills
            WHERE account_number = :acct
            ORDER BY bill_date DESC
            FETCH FIRST :limit ROWS ONLY
            """,
            acct=account_number.upper(),
            limit=limit,
        )
        rows = await cursor.fetchall()

    cols = [c[0].lower() for c in cursor.description]
    return [Bill(**dict(zip(cols, row))) for row in rows]


async def get_bill(account_number: str, bill_id: str) -> Bill:
    async with get_connection() as conn:
        cursor = conn.cursor()
        await cursor.execute(
            """
            SELECT bill_id, account_number,
                   TO_CHAR(bill_date, 'YYYY-MM-DD') AS bill_date,
                   TO_CHAR(due_date, 'YYYY-MM-DD') AS due_date,
                   amount_due, amount_paid, status
            FROM bills
            WHERE account_number = :acct AND bill_id = :bill_id
            """,
            acct=account_number.upper(),
            bill_id=bill_id,
        )
        row = await cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail=f"Bill {bill_id} not found")

    cols = [c[0].lower() for c in cursor.description]
    return Bill(**dict(zip(cols, row)))


async def create_payment(account_number: str, req: PaymentRequest) -> Payment:
    async with get_connection() as conn:
        cursor = conn.cursor()
        await cursor.execute(
            """
            INSERT INTO payments (account_number, payment_date, amount, method)
            VALUES (:acct, SYSDATE, :amount, :method)
            RETURNING payment_id, TO_CHAR(payment_date, 'YYYY-MM-DD') INTO :pid, :pdate
            """,
            acct=account_number.upper(),
            amount=req.amount,
            method=req.method,
            pid=cursor.var(str),
            pdate=cursor.var(str),
        )
        payment_id = cursor.bindvars["pid"].getvalue()
        payment_date = cursor.bindvars["pdate"].getvalue()
        await conn.commit()

    return Payment(
        payment_id=payment_id,
        account_number=account_number.upper(),
        payment_date=payment_date,
        amount=req.amount,
        method=req.method,
    )
