from flask import Flask, render_template, request, redirect, url_for, session, make_response
from dao.orm import *
from datetime import date
import json
from flask_bootstrap import Bootstrap
from dao.db import PostgresDb
from forms.forms import *
from dao.orm.entities import *
import numpy as np
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.sql.expression import func
from pearson import *
from classification import *

app = Flask(__name__)
app.secret_key = 'development key'
app.debug = True
db = PostgresDb()
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    user_obj = {}
    allUsers = db.sqlalchemy_session.query(User).all()
    current_user = session.get('username')
    admin = False
    current_user = session.get('username')
    if (current_user == 'admin'):
        admin = True
    for user in allUsers:
        if (user.Username == current_user):
            user_obj = user
    return render_template('index.html', current_user = current_user, user_obj = user_obj, admin = admin)
@app.route('/personal_messages', methods = ['GET', 'POST'])
def personal_messages():
    allUsers = db.sqlalchemy_session.query(User).all()
    current_user = session.get('username')
    if (current_user == 'admin'):
        admin = True
        return render_template('personal_messages.html', meow = 'mepw', allUsers=allUsers, current_user = current_user, admin = admin)
    return render_template('personal_messages.html', allMessageallUserss=allUsers, current_user=current_user)


@app.route('/all_users', methods = ['GET', 'POST'])
def all_users():
    allUsers = db.sqlalchemy_session.query(User).all()
    current_user = session.get('username')
    if (current_user == 'admin'):
        admin = True
    return render_template('all_users.html', allUsers=allUsers, current_user = current_user, admin = admin)
@app.route('/all_messages_admin', methods = ['GET', 'POST'])
def all_messages_admin():
    allMessages = db.sqlalchemy_session.query(Message).all()
    current_user = session.get('username')
    if (current_user == 'admin'):
        admin = True
    return render_template('all_mesages_admin.html', allMessages=allMessages, current_user = current_user, admin = admin)
@app.route('/delete_message')
def delete_message():
    id = request.args.get('name')
    message = db.sqlalchemy_session.query(User).filter(Message.MessageID == id).first()
    db.sqlalchemy_session.delete(message)
    db.sqlalchemy_session.commit()

    return redirect(url_for('all_messages_admin'))
@app.route('/delete_user')
def delete_user():
    username = request.args.get('name')
    user = db.sqlalchemy_session.query(User).filter(User.Username == username).first()
    db.sqlalchemy_session.delete(user)
    db.sqlalchemy_session.commit()

    return redirect(url_for('all_users'))
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    error = "whhat"
    error_username = 'YOU CANT DUBLICATE USERNAMES.' \
            ' TRY ANOTHER USERNAME'
    error_company = 'THERE IS NO SUCH A COMPANY' \
            ' TRY ANOTHER COMPANY'
    error_department = 'THERE IS NO SUCH A DEPARTMENT' \
            ' TRY ANOTHER DEPARTMENT'
    current_user = session.get('username')
    form = UserForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('signup.html', form=form)
        else:
            new_user = User(Username = form.Username.data,
                            Password =form.Password.data,
                            Company=form.Company.data,
                            Department=form.Department.data)
        db = PostgresDb()
        user_check = db.sqlalchemy_session.query(User).filter(User.Username == form.Username.data).all()
        company_check = db.sqlalchemy_session.query(Company).filter(Company.Company == form.Company.data).all()
        department_check = db.sqlalchemy_session.query(Department).filter(Department.Department == form.Department.data).all()

        if (user_check):
            return render_template('signup.html', form=form, error=error_username)
        if not (company_check):
            return render_template('signup.html', form=form, error=error_company)
        if not (department_check):
            return render_template('signup.html', form=form, error=error_department)
        db.sqlalchemy_session.add(new_user)
        db.sqlalchemy_session.commit()
        allUsers = db.sqlalchemy_session.query(User).all()
        session['username'] = new_user.Username
        current_user = session.get('username')
        for user in allUsers:
            if (user.Username == current_user):
                user_obj = user
        return render_template('index.html', current_user = current_user, user_obj = user_obj)
    return render_template('signup.html', form = form)
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    error = 'THERE IS NO ACCOUNT WITH THAT USERNAME '
    admin = False
    if form.validate_on_submit():
        user = db.sqlalchemy_session.query(User).filter_by(Username = form.username.data).first()
        password = db.sqlalchemy_session.query(User).filter_by(Password = form.password.data).first()
        if( user and password):
                session['username'] = user.Username
                current_user = session.get('username')
                if (form.username.data == 'admin' and form.password.data == 'adminadmin'):
                    admin = True
                    return redirect(url_for('index'))
                return redirect(url_for('index'))
        return render_template('login.html', form=form, error = error)
    return render_template('login.html', form = form)
@app.route('/logout')
def logout():
    session.pop('username', None)
    current_user = session.get('username')
    return render_template('index.html', current_user = current_user)
@app.route('/user', methods = ['GET'])
def index_user():
    allUsers = db.sqlalchemy_session.query(User).all()
    return render_template('user.html', allUsers = allUsers)


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    form = UserForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('user_form.html', form=form, form_name="New user",
                                   action="new_user")
        else:
            user_obj = User(
                Username=form.Username.data,
                Password = form.Password.data,
                Company = form.Company.data

            )
            db = PostgresDb()
            a = db.sqlalchemy_session.query(Company).filter(Company.Company == form.Company.data).all()
            b = db.sqlalchemy_session.query(User).filter(User.Username == form.Username.data).all()

            if not a:
                return redirect(url_for('index_user'))
            if b:
                return redirect(url_for('index_user'))

            db.sqlalchemy_session.add(user_obj)
            db.sqlalchemy_session.commit()

    return render_template('user_form.html', form=form, form_name="New user", action="new_user")

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    form = UserForm()
    if request.method == 'GET':
        name = request.args.get('name')
        db = PostgresDb()
        user = db.sqlalchemy_session.query(User).filter(
        User.Username == name).one()

        a = db.sqlalchemy_session.query(Company).filter(Company.Company == user.Company).all()

        if not a:
            return render_template('user_form.html', form=form, form_name="Edit user", action="edit_user")

        form.Username.data = user.Username
        form.Password.data = user.Password
        form.Company.data = user.Company
        form.old_name.data = user.Username
        return render_template('user_form.html', form=form, form_name="Edit user", action="edit_user")
        
    else:

        if not form.validate():
            return render_template('user_form.html', form=form, form_name="Edit user",
                                    action="edit_user")
        else:
            db = PostgresDb()
            a = db.sqlalchemy_session.query(Company).filter(Company.Company == form.Company.data).all()

            if not a:
                return render_template('user_form.html', form=form, form_name="Edit user",
                                    action="edit_user")

            user = db.sqlalchemy_session.query(User).filter(User.Username == form.old_name.data ).one()
    
            user.Username = form.Username.data
            user.Password = form.Password.data
            user.Company = form.Company.data
            

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_user'))

@app.route('/messages_department', methods = ['GET'])
def messages_department():
    allUsers = db.sqlalchemy_session.query(User).all()
    allMesages = db.sqlalchemy_session.query(Message).all()
    current_user = session.get('username')

    user_array = []
    messages_array = []
    user_department_array=[]
    for user in allUsers:
        if (user.Username == current_user):
            user_obj = user
    needed_department = user_obj.Department
    print('dep', needed_department)
    for user in allUsers:
         if(user.Company == user_obj.Company):
             user_array.append(user)
    for user in user_array:
        if(user.Department == needed_department):
            user_department_array.append(user)
    for message in allMesages:
        for i in ((user_department_array)):
            if(message.MessageSender == i.Username):
                messages_array.append(message)

    return render_template('messages.html',user_obj = user_obj, user_array=user_array, allMesages = messages_array, current_user = current_user)

@app.route('/messages', methods = ['GET'])
def index_message():
    allUsers = db.sqlalchemy_session.query(User).all()
    allMesages = db.sqlalchemy_session.query(Message).all()
    current_user = session.get('username')
    user_array = []
    messages_array = []

    for user in allUsers:
        if (user.Username == current_user):
            user_obj = user
    for user in allUsers:
         if(user.Company == user_obj.Company):
             user_array.append(user)
    for message in allMesages:
        for i in ((user_array)):
            if(message.MessageSender == i.Username):
                messages_array.append(message)

    return render_template('company_messages.html', user_array=user_array, allMesages = messages_array, current_user = current_user, user_obj= user_obj)

@app.route('/new_message', methods=['GET', 'POST'])
def new_message():
    db = PostgresDb()
    form = MessagesForm()
    current_user = session.get('username')
    allUsers = db.sqlalchemy_session.query(User).all()

    if request.method == 'POST':
        if not form.validate():
            return render_template('message_form.html',current_user = current_user, form=form, form_name="New message", action="new_message")
        else:
            message_obj = Message(
                MessageSender=current_user,
                MessageContent = form.MessageContent.data,
                MessageDate = date.today()
            )

            db.sqlalchemy_session.add(message_obj)
            db.sqlalchemy_session.commit()
            for user in allUsers:
                if (user.Username == current_user):
                    user_obj = user

            return redirect(url_for('index_message'))

    return render_template('message_form.html', current_user=current_user, form=form, form_name="New message", action="new_message")

@app.route('/edit_message', methods=['GET', 'POST'])

def edit_message():
    form = MessagesForm()
    db = PostgresDb()
    if request.method == 'GET':
        message_id = request.args.get('name')
        message = db.sqlalchemy_session.query(Message).filter(Message.MessageID == message_id).one()

        a = db.sqlalchemy_session.query(Message).filter(Message.MessageID == message.MessageID).all()

        if not a:
            return render_template('message_form.html', form=form, form_name="Edit message", action="edit_message")
        form.MessageContent.data = message.MessageContent
        form.old_name.data = message.MessageID
        return render_template('message_form.html', form=form, form_name="Edit message", action="edit_message")
        
    else:
        if not form.validate():

            return render_template('message_form.html', form=form, form_name="Edit message",
                                    action="edit_message")
        else:
            db = PostgresDb()
            a = db.sqlalchemy_session.query(Message).filter(Message.MessageID == form.old_name.data).all()

            if not a:
                return render_template('message_form.html', form=form, form_name="Edit message",
                                    action="edit_message")
            message = db.sqlalchemy_session.query(Message).filter(Message.MessageID == form.old_name.data ).one()
    
            message.MessageContent = form.MessageContent.data
            message.MessageDate = date.today()

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_message'))
   


@app.route('/company', methods = ['GET'])
def index_company():
    allCompanies = db.sqlalchemy_session.query(Company).all()
    return render_template('companies.html', allCompanies = allCompanies)

@app.route('/new_company', methods=['GET', 'POST'])
def new_company():
    form = CompaniesForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('companies_form.html', form=form, form_name="New company", action="new_company")
        else:
            company_obj = Company(
                 Company=form.Company.data,
            )
            db.sqlalchemy_session.add(company_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_company'))

    return render_template('companies_form.html', form=form, form_name="New company", action="new_company")

@app.route('/edit_company', methods = ['GET'])
def edit_company():
    form = CompaniesForm()

    if request.method == 'GET':

        company = request.args.get('name')
        db = PostgresDb()
        companyobj = db.sqlalchemy_session.query(Company).filter(Company.Company == company).one()

        form.Company.data = companyobj.Company
        form.old_name.data = companyobj.Company
        return render_template('companies_form.html', form=form, form_name="Edit company", action="new_company")

    else:
        if not form.validate():
            return render_template('companies_form.html', form=form, form_name="Edit company",
                                    action="edit_company")
        else:
            db = PostgresDb()

            companyobj = db.sqlalchemy_session.query(Company).filter(Company.Company == form.old_name.data).one()
            companyobj.Company = form.Company.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_company'))
@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    allUsers = db.sqlalchemy_session.query(User).all()
    allDepartments = db.sqlalchemy_session.query(Department).all()

    lenOfName = []
    lenofPass = []
    mean = ''
    for user in allUsers:
        lenOfName.append(len(user.Username))
        lenofPass.append(len(user.Password))
    corellation_number = pearson(lenOfName, lenofPass)
    if (corellation_number > 0.9 and corellation_number < 1):
        mean = 'Very high dependence'
    if (corellation_number > 0.7 and corellation_number < 0.9):
        mean = 'High dependence'
    if (corellation_number > 0.5 and corellation_number < 0.7):
        mean = 'Medium dependence'
    if (corellation_number == 1):
        mean = '100% dependence'
    current_user = session.get('username')
    width = corellation_number * 100
    array_departs = []
    x  = []
    age = request.args.get('age')
    depart = request.args.get('depart')
    allDepartments = db.sqlalchemy_session.query(Department).all()
    for dep in allDepartments:
        array_departs.append(dep.Department)
    index = array_departs.index(depart)
    x.append(int(age))
    x.append(index)
    print('x', x)
    result_pnn = output(x)
    return render_template('statistics.html', result_pnn=result_pnn, width=width, allDepartments  = allDepartments, corellation_number = corellation_number, current_user = current_user)

@app.route('/statistics', methods = ['GET', 'POST'])
def statistics():
    allUsers = db.sqlalchemy_session.query(User).all()
    allDepartments = db.sqlalchemy_session.query(Department).all()

    lenOfName = []
    lenofPass = []
    mean = ''
    for user in allUsers:
        lenOfName.append(len(user.Username))
        lenofPass.append(len(user.Password))
    corellation_number = pearson(lenOfName, lenofPass)
    if (corellation_number>0.9 and corellation_number<1):
        mean = 'Very high dependence'
    if (corellation_number>0.7 and corellation_number<0.9):
        mean = 'High dependence'
    if (corellation_number>0.5 and corellation_number<0.7):
        mean = 'Medium dependence'
    if (corellation_number ==1 ):
        mean = '100% dependence'
    current_user = session.get('username')
    width = corellation_number*100
    return render_template('statistics.html', allDepartments=allDepartments, width=width, corellation_number = corellation_number, mean = mean, allUsers=allUsers, current_user = current_user)
@app.route('/delete_company')
def delete_company():
    allCompanies = db.sqlalchemy_session.query(Company).all()

    name = request.args.get('name')
    thisCompany = db.sqlalchemy_session.query(Company).filter(Company.Company == name).first()
   
    db.sqlalchemy_session.delete(thisCompany)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_company'))



@app.route('/dashboard')
def dashboard_def():

    names = set()
    for numes in db.sqlalchemy_session.query(Message.MessageSender).distinct():
        names.add(numes.MessageSender)
        print("type names", numes.MessageSender)
    names_converted = tuple(names)

    values = []
    for i in names:
        q = db.sqlalchemy_session.query(func.count(Message.MessageSender)).filter(Message.MessageSender == i).one()
        list_of_max = list(q)
        new_index = list_of_max[0]
        values.append(new_index)

    bar = go.Bar(
        x=names_converted,
        y=values,
    )
    scatter = go.Scatter(
        x=names_converted,
        y=values,
    )
    
    # messages = db.sqlalchemy_session.query(Message).order_by(Message.MessageContent)
    # calories = [dish.calories_amount for dish in messages]
    # bar = go.Bar(
    #     x=calories,
    #     y=[dish.dishname for dish in messages]
    # )
    
    # scatter = go.Scatter(
    #     x=calories,
    #     y=[dish.dishname for dish in messages],
    # )
    ids = [0, 1]
    data =[scatter, bar]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphJSON=graphJSON, ids=ids)


@app.route('/shop', methods = ['GET'])
def index_shop():
    messenger_data = db.sqlalchemy_session.query(Messenger).all()
    print(messenger_data)
    return render_template('messenger.html', messengers_data = messenger_data)


# @app.route('/plotly')
# def draw_plot():
#     messenger_names = set()
#     for numes in db.sqlalchemy_session.query(Messenger.Site).distinct():
#         messenger_names.add(numes.Site)
        
#     names_converted = tuple(messenger_names)

#     prices = []
#     for i in messenger_names:
#         query_data = db.sqlalchemy_session.query(Messenger.Price).filter(Messenger.Site == i).one()
#         print('query data', query_data)
#         list_form_of_query_response = list(query_data)
#         print('list_form_of_query_response', list_form_of_query_response)

#         new_index = list_form_of_query_response[0]
#         prices.append(new_index)

#     print(prices)
#     pie_data = go.Pie(
#         labels=names_converted,
#         values=prices,
#     )

#     ids = [0]
#     data =[pie_data]
#     graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

#     return render_template('dashboard.html', graphJSON=graphJSON, ids=ids)

@app.route('/message_room')
def chat():

    return render_template("mail.html", )
    
if __name__ == "__main__":
    app.run()