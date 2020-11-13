from .storage.monkey_patches import JWTAuthentication, FastAPIUsers
from .settings import settings
from .storage.models import user_db
from .storage.schemas.users import User, UserCreate, UserUpdate, UserDB


jwt_authentication = JWTAuthentication(
    secret=settings.SECRET,
    lifetime_seconds=3600,
    tokenUrl="/auth/jwt/login"
)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
