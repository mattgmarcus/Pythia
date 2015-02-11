from app import db

class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer)
    loan_amount = db.Column(db.Integer)
    funded_amount = db.Column(db.Integer)
    funded_amount_investors = db.Column(db.Integer)
    term = db.Column(db.Integer)
    interest_rate = db.Column(db.Float)
    installment = db.Column(db.Float)
    grade = db.Column(db.String) # Possible to store as numbers. But also don't want to be sequential
    sub_grade = db.Column(db.String)
    employee_title = db.Column(db.String)
    employment_length = db.Column(db.Integer)
    home_ownership = db.Column(db.Integer) # Will express each state as a number
    annual_income = db.Column(db.Integer)
    is_income_verified = db.Column(db.Boolean)
    issue_date = db.Column(db.DateTime)
    loan_status = db.Column(db.Integer) # Will express status as a number
    payment_plan = db.Column(db.Boolean)
    url = db.Column(db.String)
    description = db.Column(db.String)
    purpose = db.Column(db.String) # This could also be an integer if there are only a few possible values
    title = db.Column(db.String) # This could also be an integer if there are only a few possible values
    zip_code = db.Column(db.String) # Not integer because last two numbers omitted. Could also just store the first three values in integer
    address_state = db.Column(db.String) # Could label each state 1-50 and do numbers
    debt_to_income = db.Column(db.Float)
    delinq_2yrs = db.Column(db.Integer)
    earliest_credit_line = db.Column(db.DateTime)
    inq_last_6mths = db.Column(db.Integer)
    mths_since_last_delinq = db.Column(db.Integer)
    mth_since_last_record = db.Column(db.Integer)
    open_credit_lines = db.Column(db.Integer)
    public_records = db.Column(db.Integer)
    revolving_balance = db.Column(db.Integer)
    revolving_util = db.Column(db.Float)
    total_accounts = db.Column(db.Integer)
    initial_list_status = db.Column(db.Integer) # W = 0, F = 1
    outstanding_principal = db.Column(db.Float)
    outstanding_principal_investors = db.Column(db.Float)
    total_payment = db.Column(db.Float)
    total_payment_investors = db.Column(db.Float)
    total_received_principal = db.Column(db.Float)
    total_received_interest = db.Column(db.Float)
    total_received_late_fees = db.Column(db.Float)
    recoveries = db.Column(db.Float)
    collection_recovery_fee = db.Column(db.Float)
    last_payment_date = db.Column(db.DateTime)
    last_payment_amount = db.Column(db.Float)
    next_payment_date = db.Column(db.DateTime)
    last_credit_pulled_date = db.Column(db.DateTime)
    collections_12_mths = db.Column(db.Integer)
    mths_since_last_major_derog = db.Column(db.Integer)
    policy_code = db.Column(db.Integer) # 1 = publicly available, 2 = not publicly available

    def __init__(self, data):
        self.id = data["id"]
        self.member_id = data["member_id"]
        self.loan_amount = data["loan_amnt"]
        self.funded_amount = data["funded_amnt"]
        self.funded_amount_investors = data["funded_amnt_inv"]
        self.term = data["term"]
        self.interest_rate = data["int_rate"]
        self.installment = data["installment"]
        self.grade = data["grade"]
        self.sub_grade = data["sub_grade"]
        self.employee_title = data["emp_title"]
        self.employment_length = data["emp_length"]
        self.home_ownership = data["home_ownership"]
        self.annual_income = data["annual_inc"]
        self.is_income_verified = data["is_inc_v"]
        self.issue_date = data["issue_d"]
        self.loan_status = data["loan_status"]
        self.payment_plan = data["pymnt_plan"]
        self.url = data["url"]
        self.description = data["desc"]
        self.purpose = data["purpose"]
        self.title = data["title"]
        self.zip_code = data["zip_code"]
        self.address_state = data["addr_state"]
        self.debt_to_income = data["dti"]
        self.delinq_2yrs = data["delinq_2yrs"]
        self.earliest_credit_line = data["earliest_cr_line"]
        self.inq_last_6mths = data["inq_last_6mths"]
        self.mths_since_last_delinq = data["mths_since_last_delinq"]
        self.mth_since_last_record = data["mths_since_last_record"]
        self.open_credit_lines = data["open_acc"]
        self.public_records = data["pub_rec"]
        self.revolving_balance = data["revol_bal"]
        self.revolving_util = data["revol_util"]
        self.total_accounts = data["total_acc"]
        self.initial_list_status = data["initial_list_status"]
        self.outstanding_principal = data["out_prncp"]
        self.outstanding_principal_investors = data["out_prncp_inv"]
        self.total_payment = data["total_pymnt"]
        self.total_payment_investors = data["total_pymnt_inv"]
        self.total_received_principal = data["total_rec_prncp"]
        self.total_received_interest = data["total_rec_int"]
        self.total_received_late_fees = data["total_rec_late_fee"]
        self.recoveries = data["recoveries"]
        self.collection_recovery_fee = data["collection_recovery_fee"]
        self.last_payment_date = data["last_pymnt_d"]
        self.last_payment_amount = data["last_pymnt_amnt"]
        self.next_payment_date = data["next_pymnt_d"]
        self.last_credit_pulled_date = data["last_credit_pull_d"]
        self.collections_12_mths = data["collections_12_mths_ex_med"]
        self.mths_since_last_major_derog = data["mths_since_last_major_derog"]
        self.policy_code = data["policy_code"]

        self.json = { self.id: data.pop("id") }

    def __repr__(self):
        return '<id {}>'.format(self.id)
