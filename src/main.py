"""The main app file that contains the instantiation of the beer game app and all the endpoints of the app"""

from flask import Flask, g, render_template,request,redirect,session,make_response, flash
import os
import bcrypt
from flask_mysqldb import MySQL
import MySQLdb
import json
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
app.secret_key=os.urandom(24)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'se_project'

mysql = MySQL(app)


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt


db.init_app(app)
from models import *
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    """Homepage"""
    return render_template('index.html')

@app.route('/instructor_login')
def instructor_login():
    if g.instructor:
        return redirect("/instructor_dashboard")

    """Login as instructor frontend"""
    return render_template('instructor_login.html')    

@app.route('/instructor_register')
def instructor_register():
    """Register an instructor frontend"""
    return render_template('instructor_register.html')    

@app.route('/student_login')
def student_login():
    if g.student:
        return redirect("/choose_roles")

    """Login as instructor frontend"""
    return render_template('student_login.html')   

@app.route('/choose_roles')
def choose_roles():
    """Homepage for choosing roles"""
    return render_template('choose_roles.html') 

@app.route('/student_register')
def student_about():
    """Register an instructor frontend"""
    return render_template('student_register.html')    

@app.route('/game_instructions')
def game_instructions():
    """Frontend for the instructions of the game"""
    return render_template('game_instructions.html')

@app.route('/instructor')
def instructor():
    """Homepage for the instructor"""
    return render_template('instructor.html')

@app.route('/instructor_dashboard')
def instructor_dashboard():

    """ If the instructor is not logged in, redirect to login """
    if not g.instructor:
        return redirect("/instructor_login")

    instructor = Instructor.query.filter_by(email=session['instructor_email']).first()
    session['instructor_name'] = instructor.name

    games = Game.query.filter_by(instructor_id = instructor.id).all()

    """Dashboard for the instructor"""
    return render_template('instructor_dashboard.html', games = games)

@app.route('/student_dashboard')
def student_dashboard():
    if not g.student:
        return redirect("/student_login")

    student = Student.query.filter_by(email=session['student_email']).first()
    session['student_name'] = student.username
    games = Game.query.all()
    """Dashboard for the student"""
    return render_template('student_dashboard.html', games=games)

@app.route('/game_creation')
def game_creation():
    """Game creation frontend"""
    return render_template('game_creation.html')

@app.route('/game_screen/<game_id>', methods=['GET', 'POST'])
def game_screen(game_id):
    """Frontend for the Game Screen"""
    if not g.student:
        return redirect("/student_login")
    cur = mysql.connection.cursor()
    if request.method == "POST":
        try:
            cur.execute("UPDATE Student S SET S.game_id = %s WHERE S.username=%s", (request.form['game_id'], request.form['student_name']))
            mysql.connection.commit()
            cur.close()
        except MySQLdb.Error:
            return redirect('/game_screen/'+request.form['game-id'])

    cur = mysql.connection.cursor() 
    session['student_game_id'] = game_id
    games = Game.query.all()
    gameSession = Game.query.filter_by(id=game_id).first()
    week_number = gameSession.rounds_complete
    inventory = gameSession.starting_inventory
    demandPattern = Demand.query.filter_by(id=game_id).first()
    demandPattern2 = DemandPattern.query.filter_by(game_id=game_id).first()
    back_order = 0
    units_shipped = 0
    if demandPattern2 is not None:
        back_order = demandPattern2.back_order
        units_shipped = demandPattern.demand
        if back_order is None:
            back_order = 0
    orderPattern = Order.query.filter_by(id=game_id).first()
    order_made = 0
    if orderPattern is not None:
        order_made = orderPattern.order_amount
        if order_made is None:
            order_made = 0
    ending_inventory = inventory - units_shipped
    demand = cur.execute("SELECT demand FROM Demand D WHERE D.id=%s", (game_id))
    input_screen_1 = [week_number, demand, back_order]
    input_screen_1.append(input_screen_1[1] + input_screen_1[2])
    input_screen_1.append(inventory)
    input_screen_1.append(order_made)
    input_screen_1.append((input_screen_1[4] + input_screen_1[5]))
    input_screen_1.append(units_shipped)
    input_screen_1.append(ending_inventory)

    cur.execute("SELECT demand  FROM demand_pattern D WHERE D.game_id = %s", (game_id))
    demand_pattern = cur.fetchall()
    cur.execute("SELECT order_amount FROM order_pattern O WHERE O.game_id = %s", (game_id))
    order_pattern = cur.fetchall()
    input_screen_2_demand = []
    input_screen_2_order = []
    input_screen_2_demand.extend([demand_pattern[i][0] for i in range(len(demand_pattern[:10]))])
    input_screen_2_order.extend([order_pattern[i][0] for i in range(len(order_pattern[:10]))])
    input_screen_3 = []
    input_screen_4 = []
    return render_template('game_screen.html', games=games, input_screen_1=input_screen_1,
                            input_screen_2_demand=input_screen_2_demand, input_screen_2_order=input_screen_2_order,
                            input_screen_3=input_screen_3,
                            input_screen_4=input_screen_4)

@app.route('/updateDB', methods=['GET', 'POST'])
def updateDB():
    """ Updates the database with the submitted values by the player each round """
    if request.method == 'POST':
        quantity = request.form['quantity']
        game_id = request.form['game_id']
        gameSession = Game.query.filter_by(id=game_id).first()
        week_number = gameSession.rounds_complete
        gameSession.rounds_complete += 1
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO demand_pattern(game_id, demand, week_number) VALUES(%s, %s, %s)", (game_id, quantity, week_number))
        cur.execute("INSERT INTO order_pattern(game_id, order_amount, week_number) VALUES(%s, %s, %s)", (game_id, quantity, week_number))        
        mysql.connection.commit()
        cur.close()
        demandSession = Demand.query.filter_by(id=game_id).first()
        demandSession.demand = quantity

        demandSession.week_number += 1
        orderSession = Order.query.filter_by(id=game_id).first()
        orderSession.order_amount = quantity
        orderSession.week_number += 1
        db.session.commit()
    return redirect(request.referrer)


@app.route('/create_instructor', methods=['GET', 'POST'])
def create_instructor():
    """Create a instructor via query string parameters."""
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if name and email and password:
        existing_instructor = Instructor.query.filter(
            Instructor.email == email
        ).first()
        if existing_instructor:
            flash (f'{email} already exists!')
            return redirect("/instructor_login")
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_instructor = Instructor(
            name=name,
            email=email,
            password=hashed,
        )
        db.session.add(new_instructor)
        db.session.commit()
        flash ('Account successfully created! Please login')
        return redirect("/instructor_login")
    else:
        flash ('Missing details')
        return redirect("/instructor_register")

@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
    """Create a instructor via query string parameters."""
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if username and email and password:
        existing_student = Student.query.filter(
            Student.email == email
        ).first()
        if existing_student:
            flash (f'{email} already exists!')
            return redirect("/student_login")
        new_student = Student(
            username=username,
            email=email,
            password=password,
        )
        db.session.add(new_student)
        db.session.commit()
        flash ('Account successfully created! Please login')
        return redirect("/student_login")
    else:
        flash ('Missing details')
        return redirect("/student_register")

@app.before_request
def before_request():
    g.instructor = None
    g.student = None

    if 'instructor_email' in session:
        user = [x for x in Instructor.query if x.email == session['instructor_email']]
        g.instructor = user

    if 'student_email' in session:
        user = [x for x in Student.query if x.email == session['student_email']]
        g.student = user

@app.route('/instructor_login_check', methods=['GET', 'POST'])
def instructor_login_check():
    """Password check for instructor backend"""
    email = request.form.get('email')
    user_password = request.form.get('password')
    if email and user_password:
        existing_instructor = Instructor.query.filter(Instructor.email == email).first()
        if existing_instructor:
            if (bcrypt.checkpw(user_password.encode('utf-8'), existing_instructor.password.encode('utf-8'))):
                session['instructor_email'] = email
                return redirect("/instructor_dashboard")
            else:
                flash('Wrong password')
                return redirect("/instructor_login")
        else:
            flash('Wrong credentials')
            return redirect("/instructor_login")
    else:
        flash("Missing details")
        return redirect("/instructor_login")

@app.route('/instructor_logout')
def instructor_logout():
    """Instructor logout"""
    session.pop('instructor_email', None)
    return redirect("/")

@app.route('/student_login_check', methods=['GET', 'POST'])
def student_login_check():
    """Password check for student/player backend"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        existing_player = Student.query.filter(
            Student.email == email
        ).filter(
            Student.password == password
        ).first()
        if existing_player:
            session['student_email'] = email
            return redirect("/choose_roles")
        else:
            flash('Wrong credentials')
            return redirect("/student_login")
    else:
        flash("Missing details")
        return redirect("/student_login")

@app.route('/student_logout')
def student_logout():
    """Student logout"""
    session.pop('student_email', None)
    return redirect("/")

@app.route('/create_game', methods=['GET', 'POST'])
def create_game():
    """Create individual games backend"""
    email = request.form.get('email')
    user_password = request.form.get('password')
    institute = request.form.get('institute')
    games = request.form.get('games', type=int)

    if email and user_password and institute and games:
        existing_instructor = Instructor.query.filter(
            Instructor.email == email
        ).first()
        if existing_instructor:
            if (bcrypt.checkpw(user_password.encode('utf-8'), existing_instructor.password.encode('utf-8'))):
                games = int(games)
                for i in range(games):
                    new_game = Game(
                        session_length=10,
                        distributor_present=True,
                        wholesaler_present=True,
                        holding_cost=4,
                        backlog_cost=8,
                        session_id=1,
                        instructor=existing_instructor,
                        active=True,
                        info_sharing=True,
                        info_delay=2,
                        rounds_complete=1,
                        is_default_game=False,
                        starting_inventory=10,
                        instructor_id=existing_instructor.id,
                        )
                    demand_pattern = Demand(
                        week_number = 1,
                        demand = 0,
                        )
                    order_pattern_model = Order(
                        order_amount = 0,
                        week_number = 1,
                    )
                    db.session.add(new_game)
                    db.session.add(demand_pattern)
                    db.session.add(order_pattern_model)
                    db.session.commit()
                    response = "Created games with IDs: " + f'{new_game.id},'
                return redirect("/instructor_dashboard")
            else:
                flash("Wrong password")
        else:
            flash("Wrong credentials")
        return redirect("/game_creation")
    else:
        flash("Missing details")
        return redirect("/game_creation")

@app.route('/update_game/<game_id>', methods=['GET', 'POST'])
def update_game(game_id):
    """Update game method"""
    instructor = Instructor.query.filter_by(email=session['instructor_email']).first()
    session['instructor_name'] = instructor.name
    game = Game.query.filter_by(id = game_id, instructor_id = instructor.id).first()
    return render_template('update_game_screen.html', game = game)

@app.route('/update_specific_game', methods=['GET', 'POST'])
def update_specific_game():
    """Update specific game method"""
    instructor = Instructor.query.filter_by(email=session['instructor_email']).first()
    session['instructor_name'] = instructor.name
    game_id = request.form.get('game_id')
    game = Game.query.filter_by(id = game_id, instructor_id = instructor.id).first()
    # if game exists
    if game:
        holding_cost = request.form.get('holding_cost')
        backlog_cost = request.form.get('backlog_cost')
        instructor = Instructor.query.filter_by(email=session['instructor_email']).first()
        session['instructor_name'] = instructor.name
        game = Game.query.filter_by(id = game_id, instructor_id = instructor.id).first()
        game.holding_cost = holding_cost
        game.backlog_cost = backlog_cost
        db.session.commit()
        return redirect("/instructor_dashboard")

@app.route('/reset_game/<game_id>', methods=['GET', 'POST'])
def reset_game(game_id):
    """Reset a specific game"""
    instructor = Instructor.query.filter_by(email=session['instructor_email']).first()
    session['instructor_name'] = instructor.name
    game = Game.query.filter_by(id = game_id, instructor_id = instructor.id).first()
    if game :
        game.holding_cost = 0
        game.backlog_cost = 0
    db.session.commit()
    return redirect("/instructor_dashboard")

@app.route('/reset_games')
def reset_games():
    """Reset all games"""
    instructor = Instructor.query.filter_by(email=session['instructor_email']).first()
    session['instructor_name'] = instructor.name
    # reset attributes to 0 for games owned by instructor
    db.engine.execute ('update Game set holding_cost=0, backlog_cost=0 where id>0 and instructor_id=' + str(instructor.id))
    return redirect("/instructor_dashboard")

@app.route('/delete_game/<game_id>', methods=['GET', 'POST', 'DELETE'])
def delete_game(game_id):
    """Delete a specific game"""
    try:
        instructor = Instructor.query.filter_by(email=session['instructor_email']).first()
        session['instructor_name'] = instructor.name
        db.session.delete(Game.query.filter_by(id=game_id, instructor_id=instructor.id).first())
        db.session.commit()
        response = "Deleted game"
        return redirect("/instructor_dashboard")
    except:
        flash("No games to delete")
        return redirect("/instructor_dashboard")

# if __name__=="__main__":
print("here!!")
with app.app_context():
    db.create_all(app=app)
    db.session.commit()
    app.run(debug=True)