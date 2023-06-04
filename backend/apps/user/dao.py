from typing import Any
from sqlalchemy.exc import SQLAlchemyError
from apps import db
from apps.user.models import User, UserProfile, InsurancePlan, Insurance, Blacklist
from utils.security  import generate_password_hash


class UserInsuranceDao():
    @staticmethod
    def add_user_insurance(
            customer_name: str,
            email_address: str,
            password: str,
            insurance_plan_name: str,
            insured_amount: int,
            activated: bool = False
    ) -> tuple:
        """
        Create new record in DB when user signs up.

        Args:
            customer_name (str): Name of the customer
            email_address (str): Email address of the customer
            password (str): Random generated password
            insurance_plan_name (str): Insurance plan name chosen by customer
            insured_amount (int): Insured amount chosen by customer

        Returns:
            tuple: status, message, result
                    status is boolean value indicating success (True) or Failure(False),
                    message is a string about the error occurred if any, otherwise None,
                    result is the actual response generated from DB Query or None otherwise.
        """
        # Hash the password before making an entry into database
        user = User(
                    customer_name = customer_name,
                    email_address = email_address,
                    password = generate_password_hash(password)
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
            try:
                db.session.add(user)
                db.session.add(user_profile)
                db.session.add(insurance_plan)
                db.session.add(insurance)
            except SQLAlchemyError as err:
                print("Failed to add insurance data into database. {}.".format(str(err)))
                return False, "Failed to update database.", None
   
        return True, None, insurance
    
class UserDao:
    @staticmethod
    def add_user(
            customer_name: str,
            email_address: str,
            password: str
            ) -> tuple:
        """
        Create new user in database.

        Args:
            customer_name (str): Name of the customer
            email_address (str): Email address of the customer
            password (str): Random generated password

        Returns:
            tuple: status, message, result
                    status is boolean value indicating success (True) or Failure(False),
                    message is a string about the error occurred if any, otherwise None,
                    result is the actual response generated from DB Query or None otherwise.
        """
        user = User(
                    customer_name = customer_name,
                    email_address = email_address,
                    password = password
                )
        with db.session.begin():
            try:
                db.session.add(user)
            except SQLAlchemyError as err:
                print("Failed to add user data into database. {}.".format(str(err)))
                return False, "Failed to update database.", None
                  
        return True, None, user

    @staticmethod
    def get_user_by_email(
            email_address: str,
            ) -> tuple:
        """
        Get user from database by passing email id.

        Args:
            email_address (str): Email address of the customer

        Returns:
            tuple: status, message, result
                    status is boolean value indicating success (True) or Failure(False),
                    message is a string about the error occurred if any, otherwise None,
                    result is the actual response generated from DB Query or None otherwise.
        """
        result = None

        with db.session.begin():
            try:
                result = User.query.filter_by(email_address=email_address).first()
                
            except SQLAlchemyError as err:
                print("Failed to search user by email in database. {}.".format(str(err)))
                return False, "Failed to update database.", None
            
        return True, None, result
            
    @staticmethod
    def update_profile_by_activation(
            user: User,
            activated: bool
            ) -> tuple:
        """
        Update activation status of given user.

        Args:
            user (User): User whose activation status needs to be updated.
            activated (bool): Activation status, whether or not activated.

        Returns:
            tuple: status, message, result
                    status is boolean value indicating success (True) or Failure(False),
                    message is a string about the error occurred if any, otherwise None,
                    result is the actual response generated from DB Query or None otherwise.
        """
        try:
            user.userprofiles.activated = activated
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as err:
            print("Failed to update user activation in database. {}.".format(str(err)))
            return False, "Failed to update database.", None
        
        return True, None, user.userprofiles.activated

class UserProfileDao:
    @staticmethod
    def add_profile(
            activation_status: str,
            customerprofile: User,
            activated: bool = False            
            ) -> tuple:
        """
        Add new profile in database.

        Args:
            activation_status (str): Activation status of customer.
            customerprofile (User): The customer whose profile is added.
            activated (bool, optional): If user has clicked on confirmation email then he is activated. Defaults to False.

        Returns:
            tuple: status, message, result
                    status is boolean value indicating success (True) or Failure(False),
                    message is a string about the error occurred if any, otherwise None,
                    result is the actual response generated from DB Query or None otherwise.
        """
        user_profile = UserProfile(
                    activation_status = activation_status,
                    customerprofile = customerprofile,
                    activated = activated
                )

        with db.session.begin():
            try:
                db.session.add(user_profile)
            except SQLAlchemyError as err:
                print("Failed to add user profile data into database. {}.".format(str(err)))
                return False, "Failed to update database.", None
                   
        return True, None, user_profile
    
    @staticmethod
    def get_profile_by_user(
            user: str
            ) -> tuple:
        """
        Search given profile in database by using FK user id.

        Args:
            user (str): User (Foreign Key) whose profile needs to be searched.

        Returns:
            tuple: status, message, result
                    status is boolean value indicating success (True) or Failure(False),
                    message is a string about the error occurred if any, otherwise None,
                    result is the actual response generated from DB Query or None otherwise.
        """
        result = None

        with db.session.begin():
            try:
                result = db.session.query(UserProfile).join(
                    User, User.id == UserProfile.customerprofile_id
                )

                if result is not None:
                    result = result.first()

            except SQLAlchemyError as err:
                print("Failed to get profile by user from database. {}.".format(str(err)))
                return False, "Failed to update database.", None

        return True, None, result
    
    @staticmethod
    def update_profile_by_activation(
            user_profile: UserProfile,
            activated: bool
            ) -> tuple:
        """
        Update activation status of given user profile.

        Args:
            user_profile (int): User profile which needs to be updated.
            activated (bool): Activation status, whether or not activated.

        Returns:
            tuple: status, message, result
                    status is boolean value indicating success (True) or Failure(False),
                    message is a string about the error occurred if any, otherwise None,
                    result is the actual response generated from DB Query or None otherwise.
        """
        try:
            user_profile.activated = activated
            db.session.add(user_profile)
            db.session.commit()
        except SQLAlchemyError as err:
            print("Failed to update profile by activation in database. {}.".format(str(err)))
            return False, "Failed to update database.", None
        
        return True, None, None

class InsurancePlanDao:
    @staticmethod
    def add_insurance_plan(
            insurance_plan_name: str
            ) -> tuple:
        """
        Create new insurance plan in database.

        Args:
            insurance_plan_name (str): Insurance plan name chosen by customer

        Returns:
            tuple: status, message, result
                    status is boolean value indicating success (True) or Failure(False),
                    message is a string about the error occurred if any, otherwise None,
                    result is the actual response generated from DB Query or None otherwise.
        """
        insurance_plan = InsurancePlan(
                    insurance_plan_name = insurance_plan_name             
                )

        with db.session.begin():
            try:
                db.session.add(insurance_plan)
            except SQLAlchemyError as err:
                print("Failed to add insurance plan in database. {}.".format(str(err)))
                return False, "Failed to update database.", None
            
        return True, None, insurance_plan
    
class InsuranceDao:
    @staticmethod
    def add_insurance(
            insured_amount: int,
            user: User,
            insurance_plan: InsurancePlan
            ) -> tuple:
        """
        Create new insurance in database.

        Args:
            insured_amount (int): Insured amount chosen by customer
            user (User): The customer who is creating insurance
            insurance_plan (InsurancePlan): The insurance plan chosen by customer

        Returns:
            tuple: status, message, result
                    status is boolean value indicating success (True) or Failure(False),
                    message is a string about the error occurred if any, otherwise None,
                    result is the actual response generated from DB Query or None otherwise.
        """
        insurance = Insurance(
                    insured_amount = insured_amount,
                    user = user,
                    insurance_plan = insurance_plan             
                )

        with db.session.begin():
            try:
                db.session.add(insurance)
            except SQLAlchemyError as err:
                print("Failed to add insurance in database. {}.".format(str(err)))
                return False, "Failed to update database.", None

        return True, None, insurance

class BlacklistDao:
    @staticmethod
    def add_blacklist(
            email_address: str,
            reason: str
            ) -> tuple:
        """
        Create new blacklisted email in database.

        Args:
            email_address (str): Email address of the customer
            reason (str): Reason for blacklisting

        Returns:
            tuple: status, message, result
                    status is boolean value indicating success (True) or Failure(False),
                    message is a string about the error occurred if any, otherwise None,
                    result is the actual response generated from DB Query or None otherwise.
        """
        blacklist = Blacklist(
                    email_address = email_address,
                    reason = reason
                )
        
        with db.session.begin():
            try:
                db.session.add(blacklist)
            except SQLAlchemyError as err:
                print("Failed to add blacklist in database. {}.".format(str(err)))
                return False, "Failed to update database.", None
            
        return True, None, blacklist
    
    @staticmethod
    def get_blacklist_by_email(
            email_address: str
            ) -> bool:
        """
        Find if given email id is blacklisted in database.

        Args:
            email_address (str): Email address of the customer

        Returns:
            tuple: status, message, result
                    status is boolean value indicating success (True) or Failure(False),
                    message is a string about the error occurred if any, otherwise None,
                    result is the actual response generated from DB Query or None otherwise.
        """
        result = None

        with db.session.begin():
            try:
                result = db.session.query(Blacklist.id).filter_by(email_address=email_address).first()
            except SQLAlchemyError as err:
                print("Failed to get blacklist by email from database. {}.".format(str(err)))
                return False, "Failed to update database.", None
        
        return True, None, result
