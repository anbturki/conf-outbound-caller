from app.api.utils.responses import create_response_model
from app.schemas.auth import AuthenticatedUser

AuthenticatedUserResponse = create_response_model(
    "AuthenticatedUserResponse", AuthenticatedUser
)
