from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devops_league.db'
db = SQLAlchemy(app)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    place = db.Column(db.Integer)
    points = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    draws = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    goals_scored = db.Column(db.Integer)
    goals_conceded = db.Column(db.Integer)

# Sample data
teams_data = [
    {"name": "Beitar Jerusalem", "place": 1, "points": 75, "wins": 24, "draws": 3, "losses": 1, "goals_scored": 80, "goals_conceded": 15},
    {"name": "Manchester City", "place": 2, "points": 71, "wins": 23, "draws": 2, "losses": 3, "goals_scored": 85, "goals_conceded": 20},
    {"name": "Barcelona", "place": 3, "points": 65, "wins": 20, "draws": 5, "losses": 3, "goals_scored": 72, "goals_conceded": 29},
    {"name": "PSG", "place": 4, "points": 64, "wins": 21, "draws": 1, "losses": 6, "goals_scored": 70, "goals_conceded": 36},
    {"name": "Bayern", "place": 5, "points": 54, "wins": 15, "draws":9, "losses": 4, "goals_scored": 54, "goals_conceded": 35},
    {"name": "Juventus", "place": 6, "points": 52, "wins": 15, "draws": 7, "losses": 6, "goals_scored": 51, "goals_conceded": 42},
    {"name": "Hapoel tel aviv", "place": 7, "points": 41, "wins": 11, "draws": 8, "losses": 9, "goals_scored": 42, "goals_conceded": 46},
    {"name": "Dortmund", "place": 8, "points": 38, "wins": 10, "draws": 8, "losses": 10, "goals_scored": 41, "goals_conceded": 50},
]

# Create a flag to ensure one-time database setup
db_initialized = False

@app.route('/')
def league_table():
    global db_initialized
    
    if not db_initialized:
        db.create_all()
        for team_data in teams_data:
            team = Team(**team_data)
            db.session.add(team)
        db.session.commit()
        db_initialized = True
    
    teams = Team.query.order_by(Team.place).all()
    return render_template('league_table.html', teams=teams)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
