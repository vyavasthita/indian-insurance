from typing import Any
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadData
from apps import configuration


class TokenHelper:
    def __init__(self) -> None:
        self._serializer = URLSafeTimedSerializer(configuration.SECRET_KEY)

    def generate_confirmation_token(self, email) -> tuple:
        """
        Generate Email Token.

        We use the URLSafeTimedSerializer to generate a token 
        using the email address obtained during user sign up.

        User email is encoded in the generated token.

        Args:
            email (str): Email of customer

        Returns:
            tuple: status, message, result
                    status is boolean value indicating success (True) or Failure(False),
                    message is a string about the error occurred if any, otherwise None,
                    result is the actual response generated from DB Query or None otherwise.
        """
        result = None

        try:
            result = self._serializer.dumps(email, salt=configuration.SECURITY_PASSWORD_SALT)
        except (BadData, Exception) as err:
            print("Failed to generate confirmation token.")
            return False, "Failed to generate confirmation token.", None
        
        return True, None, result

    def validate_token(self, token) -> tuple:
        """
        Validate the given token.

        If the token has not expired, then it will return an email.

        Returns:
            tuple: status, message, result
                    status is boolean value indicating success (True) or Failure(False),
                    message is a string about the error occurred if any, otherwise None,
                    result is the actual response generated from DB Query or None otherwise.
        """
        try:
            email = self._serializer.loads(
                token,
                salt=configuration.SECURITY_PASSWORD_SALT,
                max_age=configuration.EMAIL_TOKEN_EXPIRATION
            )
        except BadData as err:
            print("Email confirmation link is invalid or has expired")
            return False, "Email confirmation link is invalid or has expired.", None

        return True, None, email