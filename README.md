# 🚀 Hangarin - Task Management System

Hangarin is a sleek, modern Task Management application built with **Django**. It features user authentication, real-time progress tracking, task categorization, and priority-based sorting to help users stay organized and celebrate their productivity.



## ✨ Key Features
* **User Authentication:** Secure Signup, Login, and Logout functionality.
* **Dynamic Dashboard:** Personal workspace for every user.
* **Progress Tracking:** Visual progress bar that updates as you complete tasks.
* **Smart Categorization:** Organize tasks by "Activity," "Work," "Study," etc.
* **Priority Levels:** Visual cues for High and Low-priority goals.
* **Search & Filter:** Find tasks quickly using the built-in search bar.
* **Celebration:** Interactive confetti effects when you reach 100% completion!

## 🛠️ Tech Stack
* **Backend:** Python 3.11+, Django 5.x
* **Frontend:** HTML5, CSS3 (Custom Grid/Flexbox), JavaScript
* **Icons:** Google Material Symbols
* **Database:** SQLite (Development)

---

## ⚙️ Installation & Setup

Follow these steps to get the project running locally:

### 1. Clone the Repository
```bash
git clone https://github.com/yuul-b-awlright/hangarin.git
git clone https://github.com/yuul-b-awlright/hangarin.git
cd hangarin
```

### 2. Activate the Virtual Environment
Use the project's virtual environment so Django and dependencies load correctly.

On Windows PowerShell:
```powershell
cd c:\Users\Lenovo\Desktop\gygy\hangarin\hangarin
.\Scripts\Activate.ps1
```

Then run Django with the venv Python:
```powershell
python manage.py runserver
```

If you prefer not to activate the venv, run directly:
```powershell
.\Scripts\python.exe manage.py runserver
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Add OpenWeather API Key
Create a `.env` file in the project root with:
```text
OPENWEATHER_API_KEY=your_real_openweather_api_key_here
```

### 5. Run Migrations
```powershell
python manage.py migrate
```

### 6. Start the Development Server
```powershell
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## 🔧 Notes
* Use the virtual environment provided in `hangarin\Scripts`.
* The application may fail to start if you run `python` from the system-wide Python instead of the project's venv.
* Set a valid OpenWeather API key in `.env` before using the weather dashboard.
