import pytest
import csv
import os
from sqlalchemy import text
from apps.user.dao import BlacklistDao


email_file = os.path.join("tests/sample_test_schema", "emails.csv")


def read_test_data_from_csv(file_name):
    with open(file_name, newline="") as csvfile:
        data = csv.reader(csvfile, delimiter=",")
        next(data)  # skip header row

        return [row[0] for row in data if row]

# @pytest.mark.parametrize("email_addresses", read_test_data_from_csv(email_file))
# @pytest.mark.database
# def test_add_unique_email(db, email_addresses):
#     is_success, message, blacklist = BlacklistDao.add_blacklist(email_address=email_addresses)

#     assert is_success == True
#     assert blacklist.id > 0
#     assert blacklist.email_address == email_addresses
