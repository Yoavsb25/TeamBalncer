# TeamBalncer

![Python](https://img.shields.io/badge/Python-A78BFA?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-7C3AED?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-A78BFA?style=for-the-badge&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-7C3AED?style=for-the-badge)

> Flask web app that balances soccer teams by skill level using a greedy swap algorithm.

---

## Overview

TeamBalncer is a Flask web application for creating and balancing soccer teams. You define teams and players (each with a numeric skill level), and the app distributes players across teams then iteratively swaps them to minimize the skill gap — until all teams are within a configurable tolerance.

## Features

- User authentication (signup, login, logout)
- Create and remove teams with custom names and colors
- Add and remove players with numeric skill ratings
- Automatic team balancing via greedy swap algorithm
- Results page showing final balanced team composition

## Balancing Algorithm

1. **Initialize** — shuffle all players randomly, then distribute via round-robin across teams
2. **Balance** — iterate up to 1000 times:
   - Find the weakest team (lowest average skill) and strongest team (highest average skill)
   - If skill gap ≤ `epsilon_threshold` (0.1), stop — teams are balanced
   - On the weakest team, identify the weakest player
   - On the strongest team, search for a stronger player within a growing skill window (epsilon 0.5 → 5.0)
   - Among all candidate swaps, pick the one that minimizes the resulting skill gap
   - If the best swap reduces the gap, execute it; otherwise stop (local optimum reached)

## Data Models

| Model | Fields | Description |
|-------|--------|-------------|
| `User` | `username`, `email`, `password` (hashed) | Account with Flask-Login integration |
| `Player` | `name`, `skill_level` (float) | Individual player with numeric skill rating |
| `Team` | `name`, `color`, `players` (list) | Team with helpers: `average_skill()`, `total_skill()`, `find_weakest_player()`, `find_similar_player()` |
| `SoccerMatch` | `teams` (list), `players` (list) | Orchestrates `initialize_teams()` and `balance_teams()` |

## Routes

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Home page |
| GET/POST | `/signup` | Create a new account |
| GET/POST | `/login` | Log in |
| GET | `/logout` | Log out (login required) |
| GET/POST | `/create_teams` | Add and view teams |
| POST | `/remove_team` | Remove a team by name |
| GET | `/teams/count` | Returns current team count (plain text) |
| GET/POST | `/create_players` | Add and view players |
| POST | `/remove_player` | Remove a player by name |
| GET | `/players/count` | Returns current player count (plain text) |
| GET/POST | `/results` | Balance teams and display result |

## Getting Started

**Prerequisites:** Python 3.x, pip

```bash
git clone https://github.com/Yoavsb25/TeamBalncer.git
cd TeamBalncer
pip install -r requirements.txt
flask db upgrade
python app.py
```

Open http://localhost:5000

## Project Structure

```
TeamBalncer/
├── app.py              # Flask app — all routes, login manager, SoccerMatch integration
├── models/
│   ├── user.py         # User model + Flask-Login integration
│   ├── soccermatch.py  # SoccerMatch — initialize_teams(), balance_teams()
│   ├── team.py         # Team model with skill helpers
│   └── player.py       # Player model
├── migrations/         # Flask-Migrate database migrations
├── static/             # CSS and JS assets
├── templates/          # Jinja2 templates (home, login, signup, teams, players, results)
├── instance/           # SQLite database file
└── Procfile            # Heroku deployment config
```

---

[![LinkedIn](https://img.shields.io/badge/Yoav_Sborovsky-LinkedIn-7C3AED?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yoav-sborovsky/)
&nbsp;
Part of [Yoav Sborovsky's GitHub portfolio](https://github.com/Yoavsb25)
