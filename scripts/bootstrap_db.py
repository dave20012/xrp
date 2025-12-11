from __future__ import annotations

import asyncio
import logging

from sqlalchemy.exc import SQLAlchemyError

from xrp_platform.data.storage import Base, engine


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("bootstrap_db")


async def init_db() -> None:
    logger.info("Initializing database schemas")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database schemas created successfully")
    except SQLAlchemyError as exc:
        logger.exception("Failed to initialize database", exc_info=exc)
        raise
    finally:
        await engine.dispose()


def main() -> None:
    asyncio.run(init_db())


if __name__ == "__main__":
    main()
