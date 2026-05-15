
# 🎓 UDL Times — Web Project

A daily puzzle and gaming platform inspired by *The New York Times Games*, built with **Django** and customized with the visual identity of the **Universitat de Lleida (UdL)**.

Enjoy *Connections*, *Wordle*, and *Framed*: track your stats, compete on the leaderboards, and experience a fully responsive design.

> **Note:** All content (words, categories, movies) is based on fictional or university-related data created specifically for this project. It does not reflect official UdL information.

---

## 🚀 Getting Started

### Prerequisites
* [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/) installed.

### 1. Clone the repository
```bash
git clone [https://github.com/Nicki-28/udlTimes_Web_Project.git](https://github.com/Nicki-28/udlTimes_Web_Project.git)
cd udlTimes_Web_Project

```

### 2. Build and run the project

```bash
docker-compose up --build

```

The application will be available at: **http://localhost:8000**

### 3. Load mock data

In a new terminal, run:

```bash
docker compose exec web uv run python manage.py seed_mock_data

```

This will create sample users, statistics, and games for Wordle, Connections, and Framed.

---

## 🛠️ Tech Stack

| Layer | Technology |
| --- | --- |
| **Backend** | Python 3, Django |
| **Frontend** | HTML5, CSS3, Vanilla JS, Tailwind CSS |
| **Database** | PostgreSQL (Dockerized) |
| **E2E Tests** | Behave (BDD), Splinter, Selenium |
| **Dependency Management** | `uv`, `pyproject.toml` |

---

## 🧪 End-to-End (E2E) Testing

We have implemented a robust test suite using **Behave** (Behavior-Driven Development) and **Splinter** to ensure the proper functioning of critical workflows.

### Test Structure

```text
udltimes/
└── features/
    ├── environment.py              # Browser configuration (Headless Chrome)
    ├── *.feature                   # Gherkin language scenarios
    └── steps/
        ├── common_steps.py         # Shared steps (Login, Navigation)
        └── *_wordle.py             # Feature-specific logic

```

### Implementation Levels

1. **Level 1: `.feature` (Gherkin):** Scenario definitions in natural language.
2. **Level 2: `steps/*.py` (Python):** Code that translates the text into browser actions.
3. **Level 3: `environment.py` (Driver):** Technical browser configuration (Chrome Headless, security overrides, etc.).

### Scenario Coverage

| Feature | Scenarios | Points |
| --- | --- | --- |
| **Create Custom Wordle** | Success, no login, empty word, invalid length, unauthorized characters. | 3.0 |
| **Edit Custom Wordle** | Success as author, no login, attempt to edit others, empty validation. | 3.0 |
| **Delete Custom Wordle** | Success as author, no login, attempt to delete others. | 1.5 |

### Running the Tests

To run the tests in your local environment:

```bash
# 1. Ensure the DB is running
docker compose up -d db

# 2. Run Behave (from the project root)
POSTGRES_HOST=localhost python3 manage.py behave --keepdb

```

> **Technical Note:** Because the login modal is handled by JavaScript, the tests use `execute_script` to interact with hidden DOM elements, ensuring smooth test execution.

---

## 📂 Project Structure

```bash
udlTimes_Web_Project/
├── static/                # Assets (CSS, JS, Images)
├── templates/             # HTML Templates (Django Templates)
├── udlTimes_Web_Project/  # Core project configuration
├── udltimes/              # Main application (Models, Views, Features)
├── manage.py              # Django management script
├── Dockerfile             # Container image configuration
└── pyproject.toml         # Dependencies and development tools

```

---

## 📝 Recent Release Notes

* **Behave-Django:** Integrated into `INSTALLED_APPS`.
* **Model Fixes:** Added `max_length` to `FramedConcept` descriptions.
* **Docker Tuning:** Port `5432` exposed to facilitate local testing.
* **Login Fix:** Resolved Selenium interaction issues with Tailwind modals.

