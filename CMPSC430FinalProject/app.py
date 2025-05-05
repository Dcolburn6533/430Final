from flask import Flask, request, redirect, url_for, render_template
from supabase import create_client, Client

app = Flask(__name__)

SUPABASE_URL = "https://fpckroyafrysbwilntie.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZwY2tyb3lhZnJ5c2J3aWxudGllIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NjA0MzQwMiwiZXhwIjoyMDYxNjE5NDAyfQ.7ldcNW1nCKWTg3hni3yOuzRskPt4IX9fdnq-ISVlhp8"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_Customer(first_name, last_name, dob, address, phone_number, email):
    try:
        data = {
            "firstname": first_name,
            "lastname": last_name,
            "dob": dob,
            "house_address": address,
            "phone_number": phone_number,
            "email": email
        }
        result = supabase.table("customer").insert(data).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def edit_Customer(customer_id, new_first_name=None, new_last_name=None, new_dob=None, new_address=None, new_phone_num=None, new_email=None):
    try:
        update_data = {}
        if new_first_name is not None:
            update_data["firstname"] = new_first_name
        if new_last_name is not None:
            update_data["lastname"] = new_last_name
        if new_dob is not None:
            update_data["dob"] = new_dob
        if new_address is not None:
            update_data["house_address"] = new_address
        if new_phone_num is not None:
            update_data["phone_number"] = new_phone_num
        if new_email is not None:
            update_data["email"] = new_email
        result = supabase.table("customer").update(update_data).eq("customer_id", customer_id).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def remove_Customer(customer_id):
    try:
        result = supabase.table("customer").delete().eq("customer_id", customer_id).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def browse_Customers():
    try:
        result = supabase.table("customer").select("*").execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def browse_CustomersFiltered(search_value=None, search_column="all"):
    try:
        query = supabase.table("customer").select("*")
        if search_value:
            s = f"%{search_value}%"
            if search_column != "all":
                query = query.ilike(search_column, s)
            else:
                query = query.or_(
                    "firstname.ilike.{s},lastname.ilike.{s},dob.ilike.{s},house_address.ilike.{s},phone_number.ilike.{s},email.ilike.{s}".format(s=s)
                )
        result = query.execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}


def add_StudentLoan(disbursement_date, repay_start_date, loan_type, loan_term,
                    repay_end_date, monthly_payment, grace_period, customer_id):
    try:
        data = {
            "disbursement_date": disbursement_date,
            "repay_start_date": repay_start_date,
            "loan_type": loan_type,
            "loan_term": loan_term,
            "repay_end_date": repay_end_date,
            "monthly_payment": monthly_payment,
            "grace_period": grace_period,
            "customer_id": customer_id
        }
        result = supabase.table("studentloan").insert(data).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def edit_StudentLoan(loan_id, update_data):
    try:
        result = supabase.table("studentloan").update(update_data).eq("loan_id", loan_id).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def remove_StudentLoan(loan_id):
    try:
        result = supabase.table("studentloan").delete().eq("loan_id", loan_id).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def browse_StudentLoanFiltered(search_value=None, search_column="all"):
    try:
        query = supabase.table("studentloan").select("*, customer(firstname,lastname)")
        if search_value:
            s = f"%{search_value}%"
            if search_column != "all":
                query = query.ilike(search_column, s)
            else:
                query = query.or_(
                    "loan_id.ilike.{s},disbursement_date.ilike.{s},repay_start_date.ilike.{s},loan_type.ilike.{s},loan_term.ilike.{s},repay_end_date.ilike.{s},monthly_payment.ilike.{s},grace_period.ilike.{s},customer_id.ilike.{s},customer.firstname.ilike.{s},customer.lastname.ilike.{s}".format(s=s)
                )
        result = query.execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}


def add_AutoLoan(VIN, make, model, years, loan_amount, interest_rate, amount_paid, number_of_payments, end_date, customer_id):
    try:
        data = {
            "vin": VIN,
            "make": make,
            "model": model,
            "years": years,
            "loan_amount": loan_amount,
            "interest_rate": interest_rate,
            "amount_paid": amount_paid,
            "number_of_payments": number_of_payments,
            "end_date": end_date,
            "customer_id": customer_id
        }
        result = supabase.table("autoloan").insert(data).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def edit_AutoLoan(loan_id, update_data):
    if "VIN" in update_data:
        update_data["vin"] = update_data.pop("VIN")
    try:
        result = supabase.table("autoloan").update(update_data).eq("loan_id", loan_id).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def remove_AutoLoan(loan_id):
    try:
        result = supabase.table("autoloan").delete().eq("loan_id", loan_id).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def browse_AutoLoanFiltered(search_value=None, search_column="all"):
    try:
        query = supabase.table("autoloan").select("*, customer(firstname,lastname)")
        if search_value:
            s = f"%{search_value}%"
            if search_column != "all":
                query = query.ilike(search_column, s)
            else:
                query = query.or_(
                    "loan_id.ilike.{s},vin.ilike.{s},make.ilike.{s},model.ilike.{s},years.ilike.{s},loan_amount.ilike.{s},interest_rate.ilike.{s},amount_paid.ilike.{s},number_of_payments.ilike.{s},end_date.ilike.{s},customer_id.ilike.{s},customer.firstname.ilike.{s},customer.lastname.ilike.{s}".format(s=s)
                )
        result = query.execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}


def add_PersonalLoan(loan_purpose, loan_amount, start_date, interest_rate, amount_paid, number_of_payments, end_date, customer_id):
    try:
        data = {
            "loan_purpose": loan_purpose,
            "loan_amount": loan_amount,
            "start_date": start_date,
            "interest_rate": interest_rate,
            "amount_paid": amount_paid,
            "number_of_payments": number_of_payments,
            "end_date": end_date,
            "customer_id": customer_id
        }
        result = supabase.table("personalloan").insert(data).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def edit_PersonalLoan(loan_id, update_data):
    try:
        result = supabase.table("personalloan").update(update_data).eq("loan_id", loan_id).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def remove_PersonalLoan(loan_id):
    try:
        result = supabase.table("personalloan").delete().eq("loan_id", loan_id).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def browse_PersonalLoanFiltered(search_value=None, search_column="all"):
    try:
        query = supabase.table("personalloan").select("*, customer(firstname,lastname)")
        if search_value:
            s = f"%{search_value}%"
            if search_column != "all":
                query = query.ilike(search_column, s)
            else:
                query = query.or_(
                    "loan_id.ilike.{s},loan_purpose.ilike.{s},loan_amount.ilike.{s},start_date.ilike.{s},interest_rate.ilike.{s},amount_paid.ilike.{s},number_of_payments.ilike.{s},end_date.ilike.{s},customer_id.ilike.{s},customer.firstname.ilike.{s},customer.lastname.ilike.{s}".format(s=s)
                )
        result = query.execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}


def add_MortgageLoan(house_address, start_date, loan_amount, number_of_payments, interest_rate, amount_paid, end_date, customer_id):
    try:
        data = {
            "house_address": house_address,
            "start_date": start_date,
            "loan_amount": loan_amount,
            "number_of_payments": number_of_payments,
            "interest_rate": interest_rate,
            "amount_paid": amount_paid,
            "end_date": end_date,
            "customer_id": customer_id
        }
        result = supabase.table("mortgage").insert(data).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def edit_MortgageLoan(mortgage_id, update_data):
    try:
        result = supabase.table("mortgage").update(update_data).eq("mortgage_id", mortgage_id).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def remove_MortgageLoan(mortgage_id):
    try:
        result = supabase.table("mortgage").delete().eq("mortgage_id", mortgage_id).execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

def browse_MortgageLoanFiltered(search_value=None, search_column="all"):
    try:
        query = supabase.table("mortgage").select("*, customer(firstname,lastname)")
        if search_value:
            s = f"%{search_value}%"
            if search_column != "all":
                query = query.ilike(search_column, s)
            else:
                query = query.or_(
                    "mortgage_id.ilike.{s},house_address.ilike.{s},start_date.ilike.{s},loan_amount.ilike.{s},number_of_payments.ilike.{s},interest_rate.ilike.{s},amount_paid.ilike.{s},end_date.ilike.{s},customer_id.ilike.{s},customer.firstname.ilike.{s},customer.lastname.ilike.{s}".format(s=s)
                )
        result = query.execute()
        return result.data
    except Exception as e:
        return {"error": str(e)}

# ---------- Login & My Loans Routes ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    customers_list = browse_Customers()
    if request.method == 'POST':
        customer_id = request.form.get("customer_id")
        return redirect(url_for('myloans_route', customer_id=customer_id))
    return render_template("login.html", customers=customers_list)

@app.route('/myloans/<string:customer_id>')
def myloans_route(customer_id):
    # Get loans for a specific customer from all tables.
    student_loans = supabase.table("studentloan").select("*").eq("customer_id", customer_id).execute().data
    auto_loans = supabase.table("autoloan").select("*").eq("customer_id", customer_id).execute().data
    personal_loans = supabase.table("personalloan").select("*").eq("customer_id", customer_id).execute().data
    mortgage_loans = supabase.table("mortgage").select("*").eq("customer_id", customer_id).execute().data
    customer = supabase.table("customer").select("*").eq("customer_id", customer_id).execute().data
    if customer:
        customer = customer[0]
    else:
        customer = {}
    return render_template("myloans.html",
                           customer=customer,
                           student_loans=student_loans,
                           auto_loans=auto_loans,
                           personal_loans=personal_loans,
                           mortgage_loans=mortgage_loans)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/customers')
def customers_route():
    search_value = request.args.get("search_value")
    search_column = request.args.get("search_column", "all")
    data = browse_CustomersFiltered(search_value, search_column)
    return render_template("customers.html", customers=data, search_value=search_value, search_column=search_column)

@app.route('/customer/add', methods=['GET', 'POST'])
def add_customer_route():
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        dob = request.form.get("dob")
        address = request.form.get("address")
        phone_number = request.form.get("phone_number")
        email = request.form.get("email")
        add_Customer(first_name, last_name, dob, address, phone_number, email)
        return redirect(url_for('customers_route'))
    return render_template("add_customer.html")

@app.route('/customer/edit/<string:customer_id>', methods=['GET', 'POST'])
def edit_customer_route(customer_id):
    customers_data = browse_Customers()
    customer_record = None
    for customer in customers_data:
        if customer.get("customer_id") == customer_id:
            customer_record = customer
            break
    if request.method == 'POST':
        new_first_name = request.form.get("first_name")
        new_last_name = request.form.get("last_name")
        new_dob = request.form.get("dob")
        new_address = request.form.get("address")
        new_phone_num = request.form.get("phone_number")
        new_email = request.form.get("email")
        edit_Customer(customer_id, new_first_name, new_last_name, new_dob, new_address, new_phone_num, new_email)
        return redirect(url_for('customers_route'))
    return render_template("edit_customer.html", customer=customer_record)

@app.route('/customer/delete/<string:customer_id>')
def delete_customer_route(customer_id):
    remove_Customer(customer_id)
    return redirect(url_for('customers_route'))

@app.route('/studentloans')
def studentloans_route():
    search_value = request.args.get("search_value")
    search_column = request.args.get("search_column", "all")
    data = browse_StudentLoanFiltered(search_value, search_column)
    customers_list = browse_Customers()
    return render_template("studentloans.html", studentloans=data, search_value=search_value, search_column=search_column)

@app.route('/studentloan/add', methods=['GET', 'POST'])
def add_studentloan_route():
    customers_list = browse_Customers()
    if request.method == 'POST':
        disbursement_date = request.form.get("disbursement_date")
        repay_start_date = request.form.get("repay_start_date")
        loan_type = request.form.get("loan_type")
        loan_term = request.form.get("loan_term")
        repay_end_date = request.form.get("repay_end_date")
        monthly_payment = float(request.form.get("monthly_payment"))
        grace_period = request.form.get("grace_period")
        customer_id = request.form.get("customer_id")
        add_StudentLoan(disbursement_date, repay_start_date, loan_type, loan_term,
                        repay_end_date, monthly_payment, grace_period, customer_id)
        return redirect(url_for('studentloans_route'))
    return render_template("add_studentloan.html", customers=customers_list)

@app.route('/studentloan/edit/<string:loan_id>', methods=['GET', 'POST'])
def edit_studentloan_route(loan_id):
    studentloans_data = browse_StudentLoanFiltered()
    customers_list = browse_Customers()
    loan_record = None
    for loan in studentloans_data:
        if loan.get("loan_id") == loan_id:
            loan_record = loan
            break
    if request.method == 'POST':
        update_data = {
            "disbursement_date": request.form.get("disbursement_date"),
            "repay_start_date": request.form.get("repay_start_date"),
            "loan_type": request.form.get("loan_type"),
            "loan_term": request.form.get("loan_term"),
            "repay_end_date": request.form.get("repay_end_date"),
            "monthly_payment": float(request.form.get("monthly_payment")),
            "grace_period": request.form.get("grace_period"),
            "customer_id": request.form.get("customer_id")
        }
        edit_StudentLoan(loan_id, update_data)
        return redirect(url_for('studentloans_route'))
    return render_template("edit_studentloan.html", loan=loan_record, customers=customers_list)

@app.route('/studentloan/delete/<string:loan_id>')
def delete_studentloan_route(loan_id):
    remove_StudentLoan(loan_id)
    return redirect(url_for('studentloans_route'))

@app.route('/autoloans')
def autoloans_route():
    search_value = request.args.get("search_value")
    search_column = request.args.get("search_column", "all")
    data = browse_AutoLoanFiltered(search_value, search_column)
    customers_list = browse_Customers()
    return render_template("autoloans.html", autoloans=data, search_value=search_value, search_column=search_column)

@app.route('/autoloan/add', methods=['GET', 'POST'])
def add_autoloan_route():
    customers_list = browse_Customers()
    if request.method == 'POST':
        VIN = request.form.get("VIN")
        make = request.form.get("make")
        model = request.form.get("model")
        years = int(request.form.get("years"))
        loan_amount = float(request.form.get("loan_amount"))
        interest_rate = float(request.form.get("interest_rate"))
        amount_paid = float(request.form.get("amount_paid"))
        number_of_payments = int(request.form.get("number_of_payments"))
        end_date = request.form.get("end_date")
        customer_id = request.form.get("customer_id")
        add_AutoLoan(VIN, make, model, years, loan_amount, interest_rate, amount_paid, number_of_payments, end_date, customer_id)
        return redirect(url_for('autoloans_route'))
    return render_template("add_autoloan.html", customers=customers_list)

@app.route('/autoloan/edit/<string:loan_id>', methods=['GET', 'POST'])
def edit_autoloan_route(loan_id):
    autoloans_data = browse_AutoLoanFiltered()
    customers_list = browse_Customers()
    loan_record = None
    for loan in autoloans_data:
        if loan.get("loan_id") == loan_id:
            loan_record = loan
            break
    if request.method == 'POST':
        update_data = {
            "VIN": request.form.get("VIN"),
            "make": request.form.get("make"),
            "model": request.form.get("model"),
            "years": int(request.form.get("years")),
            "loan_amount": float(request.form.get("loan_amount")),
            "interest_rate": float(request.form.get("interest_rate")),
            "amount_paid": float(request.form.get("amount_paid")),
            "number_of_payments": int(request.form.get("number_of_payments")),
            "end_date": request.form.get("end_date"),
            "customer_id": request.form.get("customer_id")
        }
        edit_AutoLoan(loan_id, update_data)
        return redirect(url_for('autoloans_route'))
    return render_template("edit_autoloan.html", loan=loan_record, customers=customers_list)

@app.route('/autoloan/delete/<string:loan_id>')
def delete_autoloan_route(loan_id):
    remove_AutoLoan(loan_id)
    return redirect(url_for('autoloans_route'))

@app.route('/personalloans')
def personalloans_route():
    search_value = request.args.get("search_value")
    search_column = request.args.get("search_column", "all")
    data = browse_PersonalLoanFiltered(search_value, search_column)
    customers_list = browse_Customers()
    return render_template("personalloans.html", personalloans=data, search_value=search_value, search_column=search_column)

@app.route('/personalloan/add', methods=['GET', 'POST'])
def add_personalloan_route():
    customers_list = browse_Customers()
    if request.method == 'POST':
        loan_purpose = request.form.get("loan_purpose")
        loan_amount = float(request.form.get("loan_amount"))
        start_date = request.form.get("start_date")
        interest_rate = float(request.form.get("interest_rate"))
        amount_paid = float(request.form.get("amount_paid"))
        number_of_payments = int(request.form.get("number_of_payments"))
        end_date = request.form.get("end_date")
        customer_id = request.form.get("customer_id")
        add_PersonalLoan(loan_purpose, loan_amount, start_date, interest_rate, amount_paid, number_of_payments, end_date, customer_id)
        return redirect(url_for('personalloans_route'))
    return render_template("add_personalloan.html", customers=customers_list)

@app.route('/personalloan/edit/<string:loan_id>', methods=['GET', 'POST'])
def edit_personalloan_route(loan_id):
    personalloans_data = browse_PersonalLoanFiltered()
    customers_list = browse_Customers()
    loan_record = None
    for loan in personalloans_data:
        if loan.get("loan_id") == loan_id:
            loan_record = loan
            break
    if request.method == 'POST':
        update_data = {
            "loan_purpose": request.form.get("loan_purpose"),
            "loan_amount": float(request.form.get("loan_amount")),
            "start_date": request.form.get("start_date"),
            "interest_rate": float(request.form.get("interest_rate")),
            "amount_paid": float(request.form.get("amount_paid")),
            "number_of_payments": int(request.form.get("number_of_payments")),
            "end_date": request.form.get("end_date"),
            "customer_id": request.form.get("customer_id")
        }
        edit_PersonalLoan(loan_id, update_data)
        return redirect(url_for('personalloans_route'))
    return render_template("edit_personalloan.html", loan=loan_record, customers=customers_list)

@app.route('/personalloan/delete/<string:loan_id>')
def delete_personalloan_route(loan_id):
    remove_PersonalLoan(loan_id)
    return redirect(url_for('personalloans_route'))

@app.route('/mortgageloans')
def mortgageloans_route():
    search_value = request.args.get("search_value")
    search_column = request.args.get("search_column", "all")
    data = browse_MortgageLoanFiltered(search_value, search_column)
    customers_list = browse_Customers()
    return render_template("mortgageloans.html", mortgageloans=data, search_value=search_value, search_column=search_column)

@app.route('/mortgageloan/add', methods=['GET', 'POST'])
def add_mortgageloan_route():
    customers_list = browse_Customers()
    if request.method == 'POST':
        house_address = request.form.get("house_address")
        start_date = request.form.get("start_date")
        loan_amount = float(request.form.get("loan_amount"))
        number_of_payments = int(request.form.get("number_of_payments"))
        interest_rate = float(request.form.get("interest_rate"))
        amount_paid = float(request.form.get("amount_paid"))
        end_date = request.form.get("end_date")
        customer_id = request.form.get("customer_id")
        add_MortgageLoan(house_address, start_date, loan_amount, number_of_payments, interest_rate, amount_paid, end_date, customer_id)
        return redirect(url_for('mortgageloans_route'))
    return render_template("add_mortgageloan.html", customers=customers_list)

@app.route('/mortgageloan/edit/<string:mortgage_id>', methods=['GET', 'POST'])
def edit_mortgageloan_route(mortgage_id):
    mortgageloans_data = browse_MortgageLoanFiltered()
    customers_list = browse_Customers()
    loan_record = None
    for loan in mortgageloans_data:
        if loan.get("mortgage_id") == mortgage_id:
            loan_record = loan
            break
    if request.method == 'POST':
        update_data = {
            "house_address": request.form.get("house_address"),
            "start_date": request.form.get("start_date"),
            "loan_amount": float(request.form.get("loan_amount")),
            "number_of_payments": int(request.form.get("number_of_payments")),
            "interest_rate": float(request.form.get("interest_rate")),
            "amount_paid": float(request.form.get("amount_paid")),
            "end_date": request.form.get("end_date"),
            "customer_id": request.form.get("customer_id")
        }
        edit_MortgageLoan(mortgage_id, update_data)
        return redirect(url_for('mortgageloans_route'))
    return render_template("edit_mortgageloan.html", loan=loan_record, customers=customers_list)

@app.route('/mortgageloan/delete/<string:mortgage_id>')
def delete_mortgageloan_route(mortgage_id):
    remove_MortgageLoan(mortgage_id)
    return redirect(url_for('mortgageloans_route'))

if __name__ == '__main__':
    app.run(debug=True)
