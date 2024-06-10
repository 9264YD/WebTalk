from flask import Flask, render_template, request, session, redirect, url_for,jsonify
from .forms import LoginForm,RegistrationForm
from .models import User,ChatData,db,QAData,GroupData
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user is None:
            return render_template('login.html', form=form)
        session['username'] = form.username.data
        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            return render_template('register.html', form=form, error='Username already exists')

        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/result', methods=['POST'])
def result():
    question = request.form['username']
    result = None

    if question == "I still don't understand.":
        latest_question = ChatData.query.order_by(ChatData.id.desc()).first()
        if latest_question:
            question = latest_question.question
        new_ishelp_value = '2'  
        qa_data = QAData.query.filter_by(question=question).first()
        if qa_data:
            qa_data.ishelp = new_ishelp_value
            db.session.commit()
        result = "The question has been submitted to the help page"
    else:
        chat_data = QAData.query.filter_by(question=question).first()
        if chat_data:
            result = chat_data.answer
        else:
            result = "I don't understand what you mean"

    usersname = session['username']
    chat_data = ChatData(question=question, answer=result, usersname=usersname)
    db.session.add(chat_data)
    db.session.commit()

    return jsonify({'result': result})


@app.route('/chat')
def chat():
    if 'username' in session:
        now_username = session['username']
        messages = ChatData.query.filter(ChatData.usersname == now_username).all()
        messages = [[message.id, message.question, message.answer] for message in messages]
        return render_template('chat.html', messages=messages)
    else:
        return redirect(url_for('index'))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    username = session['username']
    if username == 'admin':
        question = request.form.get('question')
        answer = request.form.get('answer')
        print(answer)

        db.session.query(QAData).filter(QAData.question == question).update({"answer": answer})
        db.session.commit()

        return redirect(url_for('help'))
    else:
        return redirect(url_for('help'))
    
@app.route('/help')
def help():
    if 'username' in session:
        secondrows = QAData.query.filter(QAData.ishelp == '2').all()
        firstrows = QAData.query.filter(QAData.ishelp == '1').all()
        messages = [[row.question, row.answer] for row in secondrows]

        if firstrows:
            firstrow = firstrows[0]
            daijie_question_list = [firstrow.question, 'Please enter the correct answer to this question below']
            messages.append(daijie_question_list)

        return render_template('help.html', messages=messages)
    else:
        return redirect(url_for('index'))

@app.route('/meet', methods=['POST'])
def meet():
    gossip = request.form['username']
    username = session['username']
    group_data = GroupData(gossip=gossip, username=username)
    db.session.add(group_data)
    db.session.commit()

    result = 'User ' + str(username) + ':' + str(gossip)
    return jsonify({'result': result})

@app.route('/group')
def group():
    if 'username' in session:
        rows = GroupData.query.all()
        messages = []
        if rows:
            messages = [['User ' + str(row.username) + ':' + str(row.gossip)] for row in rows]

        return render_template('group.html', messages=messages)
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'username' in session:
        if request.method == 'POST':
            if request.form['password'] != '':
                User.query.filter(User.username == session['username']).update({"password": request.form['password']})
                db.session.commit()
                session.pop('username', None)
                return redirect(url_for('index'))
        return render_template('Account.html', username=session['username'])
    else:
        return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    if 'username' in session:
        now_username = session['username']
        messages = ChatData.query.filter(ChatData.usersname == now_username).all()
        messages = [[message.id, message.question, message.answer] for message in messages]
        return render_template("search.html", messages=messages)
    else:
        return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_data():
    Questionid = request.form['Questionid']
    ChatData.query.filter(ChatData.id == Questionid).delete()
    db.session.commit()
    return redirect(url_for('search'))