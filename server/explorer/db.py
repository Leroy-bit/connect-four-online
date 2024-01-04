from base.entity import BaseEntity
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
import config

class DBAccessor(BaseEntity):

    class Base(DeclarativeBase):
        pass

    class User(Base):
        __tablename__ = 'users'
        id: Mapped[int] = mapped_column(primary_key=True, unique=True)
        first_name: Mapped[str] = mapped_column()
        last_name: Mapped[str] = mapped_column(nullable=True)
        username: Mapped[str] = mapped_column(nullable=True)
        language_code: Mapped[str] = mapped_column(nullable=True)
        is_blocked: Mapped[bool] = mapped_column()
        connections: Mapped[int] = mapped_column()
        rating: Mapped[int] = mapped_column()

    async def setup(self) -> None:
        self.engine = create_async_engine(f'sqlite+aiosqlite://{config.BASE_DIR}/server/main.db', echo=True)
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

    async def _getUser(self, session: AsyncSession, user_id: int) -> User | None:
        user = await session.get(self.User, user_id)
        return user

    async def _addUser(
            self, 
            session: AsyncSession, 
            user_id: int, 
            first_name: str, 
            last_name: str, 
            username: str, 
            language_code: str
        ) -> User:
        
        user = self.User(
            id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            language_code=language_code,
            is_blocked=False,
            connections=0,
            rating=0
        )
        session.add(user)
        return user

    async def handleUser(
            self, 
            user_id: int, 
            first_name: str, 
            last_name: str, 
            username: str, 
            language_code: str, 
            is_connection: bool = False) -> None:

        async with self.session() as session:
            user = await self._getUser(session, user_id)
            if not user:
                user = await self._addUser(session, user_id, first_name, last_name, username, language_code)
            if is_connection:
                user.connections += 1
            await session.commit()
