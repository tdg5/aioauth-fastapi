from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
)
import uuid
from aioauth_fastapi.crypto import make_random_password, pbkdf2, verify

from sqlalchemy.orm import declarative_base

Base = declarative_base()  # type: ignore


class BaseTable(Base):  # type: ignore
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )


class UserTable(BaseTable):
    __tablename__ = "user"

    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    is_superuser = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)

    def __init__(self, *args, **kwargs):
        password = kwargs.pop("password", None)

        if password is not None:
            self.set_password(password)
        else:
            self.set_random_password()

        super().__init__(*args, password=self.password, **kwargs)

    def set_password(self, password) -> None:
        """
        Sets users password using pbkdf2.
        """
        self.password = pbkdf2(password)

    def set_random_password(self) -> str:
        """
        Set random password.
        """
        password = make_random_password()
        self.password = pbkdf2(password)
        return password

    def verify_password(self, password: str) -> bool:
        """
        Verify users password
        """
        return verify(password, self.password)


class ClientTable(BaseTable):
    __tablename__ = "client"

    client_id = Column(String)
    client_secret = Column(String)
    grant_types = Column(ARRAY(String))
    response_types = Column(ARRAY(String))
    redirect_uris = Column(ARRAY(String))
    scope = Column(String)


class AuthorizationCodeTable(BaseTable):
    __tablename__ = "authorization_code"

    code = Column(String)
    client_id = Column(String)
    redirect_uri = Column(String)
    response_type = Column(String)
    scope = Column(String)
    auth_time = Column(Integer)
    expires_in = Column(Integer)
    code_challenge = Column(String)
    code_challenge_method = Column(String)
    nonce = Column(String)


class TokenTable(BaseTable):
    __tablename__ = "token"

    access_token = Column(String)
    refresh_token = Column(String)
    scope = Column(String)
    issued_at = Column(Integer)
    expires_in = Column(Integer)
    client_id = Column(String)
    token_type = Column(String)
    revoked = Column(Boolean)