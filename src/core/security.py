from authx import AuthX, AuthXConfig

from core.config import settings


JWT_SECRET_KEY = settings.core.JWT_SECRET_KEY

config = AuthXConfig()
config.JWT_SECRET_KEY = JWT_SECRET_KEY
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_REFRESH_COOKIE_NAME = "refresh_token"
config.JWT_ALGORITHM = "HS256"
config.JWT_TOKEN_LOCATION = ["cookies", "headers"]

security = AuthX(config)
