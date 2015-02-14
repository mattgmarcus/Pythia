from app import db
from datetime import datetime

class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer)
    loan_amount = db.Column(db.Integer)
    funded_amount = db.Column(db.Integer)
    funded_amount_investors = db.Column(db.Float)
    term = db.Column(db.Integer)
    interest_rate = db.Column(db.Float)
    installment = db.Column(db.Float)
    grade = db.Column(db.String) # Possible to store as numbers. But also don't want to be sequential
    sub_grade = db.Column(db.String)
    employee_title = db.Column(db.String)
    employment_length = db.Column(db.Integer)
    home_ownership = db.Column(db.String) # It's the first character of the string from LC
    annual_income = db.Column(db.Float)
    is_income_verified = db.Column(db.Boolean)
    loan_status = db.Column(db.String)
    payment_plan = db.Column(db.Boolean)
    purpose = db.Column(db.String)
    zip_code = db.Column(db.String) # Not integer because last two numbers omitted. Could also just store the first three values in integer
    address_state = db.Column(db.String)
    debt_to_income = db.Column(db.Float)
    delinq_2yrs = db.Column(db.Integer)
    inq_last_6mths = db.Column(db.Integer)
    mths_since_last_delinq = db.Column(db.Integer)
    mth_since_last_record = db.Column(db.Integer)
    open_credit_lines = db.Column(db.Integer)
    public_records = db.Column(db.Integer)
    revolving_balance = db.Column(db.Integer)
    revolving_util = db.Column(db.Float)
    total_accounts = db.Column(db.Integer)
    initial_list_status = db.Column(db.String) # Either "w" or "f"
    outstanding_principal = db.Column(db.Float)
    outstanding_principal_investors = db.Column(db.Float)
    total_payment = db.Column(db.Float)
    total_payment_investors = db.Column(db.Float)
    total_received_principal = db.Column(db.Float)
    total_received_interest = db.Column(db.Float)
    total_received_late_fees = db.Column(db.Float)
    recoveries = db.Column(db.Float)
    collection_recovery_fee = db.Column(db.Float)
    last_payment_amount = db.Column(db.Float)
    collections_12_mths = db.Column(db.Integer)
    mths_since_last_major_derog = db.Column(db.Integer)
    policy_code = db.Column(db.Integer) # 1 = publicly available, 2 = not publicly available

    is_test_data = db.Column(db.Boolean)

    def __init__(self, data):
        self.id = int(data["id"])
        self.member_id = int(data["member_id"])
        self.loan_amount = int(data["loan_amnt"])
        self.funded_amount = int(data["funded_amnt"])
        self.funded_amount_investors = float(data["funded_amnt_inv"])
        self.term = int(data["term"].split(" ")[0])
        self.interest_rate = float(data["int_rate"][0:-1])
        self.installment = float(data["installment"])
        self.grade = data["grade"]
        self.sub_grade = data["sub_grade"]
        self.employee_title = data["emp_title"]

        self.employment_length = self.__parse_length(data["emp_length"])

        self.home_ownership = data["home_ownership"][0]
        self.annual_income = float(data["annual_inc"])
        self.is_income_verified = (data["is_inc_v"] == "Verified")

        self.loan_status = data["loan_status"]
        self.payment_plan = (data["pymnt_plan"] == "y")
        self.purpose = data["purpose"]
        self.zip_code = data["zip_code"]
        self.address_state = data["addr_state"]
        self.debt_to_income = float(data["dti"])
        self.delinq_2yrs = int(data["delinq_2yrs"])
        self.inq_last_6mths = int(data["inq_last_6mths"])

        self.mths_since_last_delinq = int(self.__set_if_present(data["mths_since_last_delinq"]))
        self.mths_since_last_record = int(self.__set_if_present(data["mths_since_last_record"]))

        self.open_credit_lines = int(data["open_acc"])
        self.public_records = int(data["pub_rec"])
        self.revolving_balance = float(data["revol_bal"])
        self.revolving_util = float(self.__set_if_present(data["revol_util"][0:-1]))
        self.total_accounts = int(data["total_acc"])

        self.initial_list_status = data["initial_list_status"]

        self.outstanding_principal = float(data["out_prncp"])
        self.outstanding_principal_investors = float(data["out_prncp_inv"])
        self.total_payment = float(data["total_pymnt"])
        self.total_payment_investors = float(data["total_pymnt_inv"])
        self.total_received_principal = float(data["total_rec_prncp"])
        self.total_received_interest = float(data["total_rec_int"])
        self.total_received_late_fees = float(data["total_rec_late_fee"])
        self.recoveries = float(data["recoveries"])
        self.collection_recovery_fee = float(data["collection_recovery_fee"])
        self.last_payment_amount = float(data["last_pymnt_amnt"])
        self.collections_12_mths = int(self.__set_if_present(data["collections_12_mths_ex_med"]))

        self.mths_since_last_major_derog = int(self.__set_if_present(data["mths_since_last_major_derog"]))

        self.policy_code = int(data["policy_code"])

        data.pop("id")
        self.json = { self.id: data }

    def __convert_lc_date(self, date):
        if not date:
            return None
        else:
            return datetime.strptime(date, "%b-%Y")

    def __set_if_present(self, value):
        if not value:
            return 0
        else:
            return value

    # Possible formats for length are:
    #   < 1 year
    #   x year(s)
    #   10+ years
    # We want all of these to just return a number
    # Less than 1 year will become 0
    def __parse_length(self, length):
        if length.find("<"):
            return 0
        elif length.find("+"):
            return 10
        else:
            return length.split(" ")[0]

    def __repr__(self):
        return '<id {}>'.format(self.id)
