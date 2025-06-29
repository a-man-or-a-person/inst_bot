from DB.database import Base, async_engine, async_session_factory
from DB.models import ReelLink
from sqlalchemy import select


async def add_link(user_id, user_name, link):
    async with async_session_factory() as session:
        new_link = ReelLink(user_id=user_id, user_name=user_name, link=link)
        session.add(new_link)
        await session.commit()


async def get_links() -> list:
    async with async_session_factory() as session:
        links = select(ReelLink.id, ReelLink.user_id, ReelLink.user_name, ReelLink.link).select_from(ReelLink)
        links = await session.execute(links)
        return list(map(lambda x: "\t".join(map(str, x)), list(links)))


async def delete_link(id) -> None:
    async with async_session_factory() as session:
        stmt = select(ReelLink).where(ReelLink.id == id)
        result = await session.execute(stmt)
        selected_reel = result.scalar_one_or_none()

        if selected_reel:
            await session.delete(selected_reel)
            await session.commit()


async def create_tables():
    async with async_engine.connect() as conn:
        async_engine.echo = True
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
