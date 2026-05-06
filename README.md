# UDL Times — Web Project

A daily puzzle and gaming platform inspired by The New York Times Games, built with Django and the corporate colors of the **Universitat de Lleida (UdL)**.

Play Connections, Wordle, and Framed — track your stats, climb the leaderboards, and enjoy a fully responsive experience on any device.
> Note: All game content (words, categories, movie frames, etc.) is based on fictional or university-related data created specifically for this project. It does not reflect real events, people, or official UdL information. 

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.

### 1. Clone the repository

```bash
git clone https://github.com/Nicki-28/udlTimes_Web_Project.git
cd udlTimes_Web_Project
```

### 2. Build and run the containers

```bash
docker-compose up --build
```

The application will be available at **http://localhost:8000**

### 3. Load mock data

After the containers are up, open a **new terminal window** and run:

```bash
docker compose exec web uv run python manage.py seed_mock_data
```

This creates mock Wordle, Connections, Framed, users, and stats data for local testing.

---

## Features

- **Connections** — group words by hidden categories
- **Wordle** — guess the daily 5-letter word
- **Framed** — identify the movie from its frames
- **Statistics system** — track your personal performance over time
- **Leaderboards** — compete for the top spots against other players
- **Responsive design** — optimized for mobile, tablet, and desktop

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Django |
| Frontend | HTML5, CSS3, Vanilla JavaScript, Tailwind CSS |
| Templating | Django Templates (Jinja2-style) |
| Database | PostgreSQL (via Docker) |
| Containerization | Docker + Docker Compose |
| Dependencies | `uv` / `pyproject.toml` |

---

## Project Structure

```
udlTimes_Web_Project/
├── static/                        # CSS, JS, images, fonts
├── templates/                     # HTML templates (Django template engine)
├── udlTimes_Web_Project/          # Django project settings & URLs
├── udltimes/                      # Main Django app (models, views, urls)
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── uv.lock
```

---

## About

This project was developed as part of a university web project at the **[Universitat de Lleida (UdL)](https://www.udl.cat/)**.
