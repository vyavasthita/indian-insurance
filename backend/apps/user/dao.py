from apps import db
from apps.user.models import User, UserProfile, InsurancePlan, Insurance, Blacklist


class InsuranceDBDao():
    @staticmethod
    def add_user_insurance(
            customer_name: str,
            email_address: str,
            password: str,
            insurance_plan_name: str,
            insured_amount: int,
            activation_status: str = 'pending'
    ) -> Insurance:
        """
        Create new record in DB when user signs up.

        Args:
            customer_name (str): Name of the customer
            email_address (str): Email address of the customer
            password (str): Random generated password
            insurance_plan_name (str): Insurance plan name chosen by customer
            insured_amount (int): Insured amount chosen by customer
            activation_status (str): Activation status of customer. Default is 'pending'.

        Returns:
            Insurance: Newly created insurance object
        """    
        user = User(
                    customer_name = customer_name,
                    email_address = email_address,
                    password = password
                )

        user_profile = UserProfile(
                    activation_status = activation_status,
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
            User: newly created user object
        """
        user = User(
                    customer_name = customer_name,
                    email_address = email_address,
                    password = password
                )

        return user
    

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
