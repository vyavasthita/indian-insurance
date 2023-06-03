from typing import Any
from itsdangerous import URLSafeTimedSerializer
from apps import configuration


class TokenHelper:
    def __init__(self) -> None:
        self._serializer = URLSafeTimedSerializer(configuration.SECRET_KEY)

    def generate_confirmation_token(self, email) -> str:
        """
        Generate Email Token.

        We use the URLSafeTimedSerializer to generate a token 
        using the email address obtained during user sign up.

        User email is encoded in the generated token.

        Args:
            email (str): Email of customer

        Returns:
            str: Signed string with email encoded
        """

        return self._serializer.dumps(email, salt=configuration.SECURITY_PASSWORD_SALT)

    def validate_token(self, token) -> Any:
        """
        Validate the given token.

        If the token has not expired, then it will return an email.

        Returns:
            Any: If token expired False is return else decoded email address
        """
        try:
            email = self._serializer.loads(
                token,
                salt=configuration.SECURITY_PASSWORD_SALT,
                max_age=configuration.EMAIL_TOKEN_EXPIRATION
            )
        except:
            return False

        return email