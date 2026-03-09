from db import get_connection
from models.workorder import Crew


async def list_crews() -> list[Crew]:
    async with get_connection() as conn:
        cursor = conn.cursor()
        await cursor.execute(
            "SELECT AMCREW, ORGID, AMCREWTYPE, DESCRIPTION FROM MAXIMO.AMCREW"
        )
        rows = await cursor.fetchall()

    cols = [c[0].lower() for c in cursor.description]
    return [Crew(**dict(zip(cols, row))) for row in rows]
