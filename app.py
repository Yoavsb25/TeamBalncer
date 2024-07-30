from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from models.user import User, db  # Import User model and db instance from models
from models.soccermatch import SoccerMatch, Team, Player
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Secret key for session management

# Configure the SQLAlchemy part of the app instance
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yoavsborovsky/PycharmProjects/TeamMakerWebb/instance/app.db'  # Path to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize SQLAlchemy with the app
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Set the login view endpoint

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Initialize SoccerMatch instance
soccer_match = SoccerMatch()


@app.route('/')
def index():
    return render_template('index.html')  # Render the homepage


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Load user by ID


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']

        # Check if username already exists
        if User.find_by_username(username):
            flash('Username already exists. Please choose a different one', 'error')
        # Check if passwords match
        elif verify_password != password:
            flash('Passwords do not match. Please try again', 'error')
        # Check if email already exists
        elif User.find_by_email(email):
            flash('Email address already exists. Please choose a different one', 'error')
        # Validate email format
        elif '@' not in email:
            flash('Email address is invalid. Please try again', 'error')
        else:
            new_user = User(username=username, password=password, email=email)
            db.session.add(new_user)  # Add new user to the database
            db.session.commit()
            flash('Account created successfully. You can now log in', 'success')
            return redirect(url_for('login'))  # Redirect to login page
    return render_template('signup.html')  # Render the signup page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.find_by_username(username)

        # Check if user exists and password is correct
        if user and user.verify_password(password):
            login_user(user)  # Log in the user
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))  # Redirect to homepage
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')  # Render the login page


@app.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('index'))  # Redirect to homepage


@app.route('/create_teams', methods=['GET', 'POST'])
def create_teams():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_team':
            team_name = request.form['team_name']
            team_color = request.form['team_color']
            try:
                soccer_match.add_team(team_name, team_color)  # Add new team
            except ValueError as e:
                flash(str(e), 'error')  # Handle errors
    return render_template('create_teams.html',
                           teams=soccer_match.teams)  # Render the create teams page with current teams


@app.route('/remove_team', methods=['POST'])
def remove_team():
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        removed = soccer_match.remove_team(team_name)  # Remove team
        if removed:
            flash(f'Team {team_name} has been successfully removed', 'success')
        else:
            flash(f'Team {team_name} not found', 'error')
    return redirect(url_for('create_teams'))  # Redirect to create teams page


@app.route('/teams/count', methods=['GET'])
def teams_count():
    teams_count = len(soccer_match.teams)  # Get the number of teams
    return str(teams_count)  # Return the count as a string


@app.route('/create_players', methods=['GET', 'POST'])
def create_players():
    if request.method == 'POST':
        player_name = request.form['player_name']
        player_skill = float(request.form['player_skill'])
        try:
            soccer_match.add_player(player_name, player_skill)  # Add new player
            flash(f'Player {player_name} was added successfully', 'success')
        except ValueError as e:
            flash(str(e), 'error')  # Handle errors
        return redirect(url_for('create_players'))  # Redirect to create players page
    return render_template('create_players.html',
                           players=soccer_match.players)  # Render the create players page with current players


@app.route('/remove_player', methods=['POST'])
def remove_player():
    if request.method == 'POST':
        player_name = request.form['player_name']
        try:
            soccer_match.remove_player(player_name)  # Remove player
            flash(f'Player {player_name} removed successfully', 'success')
        except ValueError as e:
            flash(str(e), 'error')  # Handle errors
        return redirect(url_for('create_players'))  # Redirect to create players page
    return redirect(url_for('create_players'))  # Redirect to create players page if method is not POST


@app.route('/players/count', methods=['GET'])
def players_count():
    player_count = len(soccer_match.players)  # Get the number of players
    return str(player_count)  # Return the count as a string


@app.route('/results', methods=['GET', 'POST'])
def results():
    try:
        soccer_match.initialize_teams()  # Initialize teams
        soccer_match.balance_teams()  # Balance teams
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'balance_teams':
                soccer_match.balance_teams()  # Balance teams again if requested
                flash('Teams balanced successfully', 'success')
                return redirect(url_for('results'))  # Redirect to results page
    except ValueError as e:
        flash(str(e), 'error')  # Handle errors
        return redirect(url_for('create_players'))  # Redirect to create players page on error
    return render_template('results.html', teams=soccer_match.teams)  # Render the results page with current teams


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables within the application context
    app.run(debug=True)  # Run the application in debug mode
