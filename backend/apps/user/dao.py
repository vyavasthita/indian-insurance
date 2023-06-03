from typing import Any
from apps import db
from apps.user.models import User, UserProfile, InsurancePlan, Insurance, Blacklist


class UserInsuranceDao():
    @staticmethod
    def add_user_insurance(
            customer_name: str,
            email_address: str,
            password: str,
            insurance_plan_name: str,
            insured_amount: int,
            activated: bool = False
    ) -> Insurance:
        """
        Create new record in DB when user signs up.

        Args:
            customer_name (str): Name of the customer
            email_address (str): Email address of the customer
            password (str): Random generated password
            insurance_plan_name (str): Insurance plan name chosen by customer
            insured_amount (int): Insured amount chosen by customer

        Returns:
            Insurance: Newly created insurance object
        """    
        user = User(
                    customer_name = customer_name,
                    email_address = email_address,
                    password = password
                )
        
        user_profile = UserProfile(
                    customerprofile = user
                )

        insurance_plan = InsurancePlan(
                    insurance_plan_name = insurance_plan_name             
                )

        insurance = Insurance(
                    insured_amount = insured_amount,
                    user = user,
                    insurance_plan = insurance_plan             
                )

        with db.session.begin():
            db.session.add(user)
            db.session.add(user_profile)
            db.session.add(insurance_plan)
            db.session.add(insurance)

        return insurance
    
class UserDao:
    @staticmethod
    def add_user(
            customer_name: str,
            email_address: str,
            password: str
            ) -> User:
        """
        Create new user in database.

        Args:
            customer_name (str): Name of the customer
            email_address (str): Email address of the customer
            password (str): Random generated password

        Returns:
            User: Newly created user object
        """
        user = User(
                    customer_name = customer_name,
                    email_address = email_address,
                    password = password
                )
        with db.session.begin():
            db.session.add(user)
        
        return user

    @staticmethod
    def get_user_by_email(
            email_address: str,
            ) -> Any:
        """
        Get user from database by passing email id.

        Args:
            email_address (str): Email address of the customer

        Returns:
            Any: User, if found in database or None
        """
        with db.session.begin():
            return db.session.query(User.id).filter_by(email_address=email_address).first()
    
class UserProfileDao:
    @staticmethod
    def add_profile(
            activation_status: str,
            customerprofile: User,
            activated: bool = False            
            ) -> UserProfile:
        """
        Add new profile in database.

        Args:
            activation_status (str): Activation status of customer.
            customerprofile (User): The customer whose profile is added.
            activated (bool, optional): If user has clicked on confirmation email then he is activated. Defaults to False.

        Returns:
            UserProfile: Newly created UserProfile object
        """
        user_profile = UserProfile(
                    activation_status = activation_status,
                    customerprofile = customerprofile,
                    activated = activated
                )

        with db.session.begin():
            db.session.add(user_profile)
        
        return user_profile
    
    @staticmethod
    def get_profile_by_user(
            user: str
            ) -> UserProfile:
        """
        Search given profile in database by using FK user id.

        Args:
            user (str): User (Foreign Key) whose profile needs to be searched.

        Returns:
            UserProfile: Customer profile from database
        """
        with db.session.begin():
            return db.session.query(UserProfile).join(
                User, User.id == UserProfile.customerprofile_id
            ).first()

    @staticmethod
    def update_profile_by_activation(
            user_profile: UserProfile,
            activated: bool
            ) -> None:
        """
        Update activation status of given user profile.

        Args:
            user_profile (int): User profile which needs to be updated.
            activated (bool): Activation status, whether or not activated.

        Returns:
            None: NA
        """
        user_profile.activated = activated
        db.session.add(user_profile)
        db.session.commit()

class InsurancePlanDao:
    @staticmethod
    def add_insurance_plan(
            insurance_plan_name: str
            ) -> InsurancePlan:
        """
        Create new insurance plan in database.

        Args:
            insurance_plan_name (str): Insurance plan name chosen by customer

        Returns:
            InsurancePlan: newly created insurance plan object
        """
        insurance_plan = InsurancePlan(
                    insurance_plan_name = insurance_plan_name             
                )

        with db.session.begin():
            db.session.add(insurance_plan)

        return insurance_plan
    
class InsuranceDao:
    @staticmethod
    def add_insurance(
            insured_amount: int,
            user: User,
            insurance_plan: InsurancePlan
            ) -> Insurance:
        """
        Create new insurance in database.

        Args:
            insured_amount (int): Insured amount chosen by customer
            user (User): The customer who is creating insurance
            insurance_plan (InsurancePlan): The insurance plan chosen by customer

        Returns:
            Insurance: Newly created insurance object
        """
        insurance = Insurance(
                    insured_amount = insured_amount,
                    user = user,
                    insurance_plan = insurance_plan             
                )

        with db.session.begin():
            db.session.add(insurance)

        return insurance

class BlacklistDao:
    @staticmethod
    def add_blacklist(
            email_address: str,
            reason: str
            ) -> Blacklist:
        """
        Create new blacklisted email in database.

        Args:
            email_address (str): Email address of the customer
            reason (str): Reason for blacklisting

        Returns:
            Blacklist: newly created blacklist object
        """
        blacklist = Blacklist(
                    email_address = email_address,
                    reason = reason
                )
        
        with db.session.begin():
            db.session.add(blacklist)

        return blacklist
    
    @staticmethod
    def get_blacklist_by_email(
            email_address: str
            ) -> bool:
        """
        Find if given email id is blacklisted in database.

        Args:
            email_address (str): Email address of the customer

        Returns:
            bool: Whether or not given user id is blacklisted
        """
        with db.session.begin():
            return db.session.query(Blacklist.id).filter_by(email_address=email_address).first() is not None
