import oracledb
from contextlib import asynccontextmanager
from config import settings

pool: oracledb.AsyncConnectionPool | None = None


async def _ensure_pool():
    global pool
    if pool is None:
        # python-oracledb thin mode supports Autonomous DB wallet natively —
        # no Oracle Client installation required.
        pool = oracledb.create_pool_async(
            user=settings.db_user,
            password=settings.db_password,
            dsn=settings.db_dsn,
            wallet_location=settings.wallet_dir,
            wallet_password=settings.wallet_password or None,
            min=2,
            max=10,
            increment=1,
        )


async def close_pool():
    if pool:
        await pool.close()


@asynccontextmanager
async def get_connection():
    await _ensure_pool()
    async with pool.acquire() as conn:
        yield conn
