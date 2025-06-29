from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from DB.database import Base


class ReelLink(Base):
    __tablename__ = "reellink"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id = mapped_column(BigInteger)
    user_name: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)
