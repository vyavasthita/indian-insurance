from apps import db
from apps.user.models import User


class UserDao:
    def create_user(
            self,
            customer_name: str,
            email_address: str,
            insurance_plan_name: str,
            insured_amount: int
            ) -> User:
        """
        Create new user in database.

        Args:
            customer_name (str): Name of the customer
            email_address (str): Email address of the customer
            insurance_plan_name (str): Insurance plan chosen by customer
            insured_amount (int): Insurance amount chosen by customer

        Returns:
            User: newly created user object
        """
        user = User(
                    customer_name = customer_name,
                    email_address = email_address,
                    insurance_plan_name = insurance_plan_name,
                    insured_amount = insured_amount,
                )
        db.session.add(user)
        db.session.commit()
        return user
    

user_dao = UserDao()
