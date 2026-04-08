# 🎾 Priyanka's Tennis Academy — Website

A fully functional Flask web application rebuilding Priyanka's Tennis Academy website with a SQLite database backend.

---

## 📁 Project Structure

```
priyanka_tennis/
├── app.py                    ← Flask app + all routes + SQLAlchemy models
├── requirements.txt          ← Python dependencies
├── start_environment.bat     ← Windows: set up virtual environment
├── start_program.bat         ← Windows: launch the website
├── start_environment.sh      ← Mac/Linux: set up virtual environment
├── start_program.sh          ← Mac/Linux: launch the website
├── README.md                 ← This file
├── instance/
│   └── tennis_academy.db     ← SQLite database (auto-created on first run)
├── static/
│   ├── css/style.css         ← All site styling
│   ├── js/main.js            ← JavaScript (nav, tabs, animations)
│   ├── images/               ← Place your photos here
│   └── videos/               ← Place your videos here
└── templates/
    ├── base.html             ← Shared layout (nav + footer)
    ├── book_a_lesson.html    ← Homepage / booking form
    ├── new_students.html     ← New students info
    ├── private_tennis_lessons.html
    ├── group_clinics.html
    ├── progress_reports.html ← Student progress lookup
    ├── lookup_progress.html  ← Progress report results
    ├── awards_ceremony.html
    ├── usta_tournaments.html
    ├── contact.html
    ├── about.html
    ├── design_x_tennis.html
    └── admin.html            ← Admin dashboard
```

---

## 🗄️ Database Tables

| Table             | Purpose                                      |
|-------------------|----------------------------------------------|
| `Booking`         | Lesson reservation requests from the site    |
| `Student`         | Enrolled student roster                      |
| `ProgressReport`  | Per-student skill ratings (7 categories)     |
| `ContactMessage`  | Messages submitted via the contact form      |
| `AwardsCeremony`  | Award records for each ceremony              |
| `Tournament`      | NorCal USTA tournament schedule entries      |

---

## 🍎 Mac Launch Instructions (Step by Step)

### Prerequisites

You need **Python 3.10 or later** installed on your Mac.

**Check if Python is already installed:**
```bash
python3 --version
```

**If not installed, install via Homebrew:**
```bash
# First install Homebrew if you don't have it:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install Python:
brew install python
```

---

### Step 1 — Unzip the Project

1. Locate the file `priyanka_tennis.zip` in your Downloads folder (or wherever you saved it)
2. Double-click it to unzip — a folder called `priyanka_tennis` will appear
3. Move the folder wherever you'd like to keep it (e.g. your Desktop or Documents)

---

### Step 2 — Open Terminal

1. Press **Command (⌘) + Space** to open Spotlight Search
2. Type `Terminal` and press **Enter**
3. The Terminal app will open

---

### Step 3 — Navigate to the Project Folder

In Terminal, type the `cd` command followed by the path to the project folder.

**If the folder is on your Desktop:**
```bash
cd ~/Desktop/priyanka_tennis
```

**If it's in Documents:**
```bash
cd ~/Documents/priyanka_tennis
```

**Tip:** You can also drag the folder onto the Terminal window after typing `cd ` (with a space) — it will auto-fill the path.

Verify you're in the right place:
```bash
ls
```
You should see files like `app.py`, `requirements.txt`, `start_environment.sh`, etc.

---

### Step 4 — Make the Shell Scripts Executable

Run this once to give Terminal permission to execute the scripts:
```bash
chmod +x start_environment.sh start_program.sh
```

---

### Step 5 — Set Up the Virtual Environment

Run the environment setup script:
```bash
bash start_environment.sh
```

This will:
- Create a Python virtual environment called `venv`
- Install all required packages (Flask, SQLAlchemy, etc.)

Wait for it to finish. You'll see: **"Environment ready! Run start_program.sh next."**

---

### Step 6 — Launch the Website

Run the program start script:
```bash
bash start_program.sh
```

You'll see:
```
 Website:  http://127.0.0.1:5000
 Admin:    http://127.0.0.1:5000/admin
```

---

### Step 7 — Open the Website in Your Browser

1. Open **Safari**, **Chrome**, or any browser
2. In the address bar, type: `http://127.0.0.1:5000`
3. Press **Enter**

🎾 **The Priyanka's Tennis Academy website is now running!**

---

### Step 8 — Explore the Admin Dashboard

Go to: `http://127.0.0.1:5000/admin`

From the admin dashboard you can:
- View and update **booking requests** (Pending → Confirmed → Cancelled)
- Add and manage **students**
- Read and mark **contact messages**
- Add **awards** to the Awards Ceremony page
- Add **tournament listings** to the USTA Tournaments page
- Create **progress reports** for enrolled students

---

### Step 9 — Stop the Server

When you're done, go back to Terminal and press:
```
CTRL + C
```

---

### Restarting Later

After the initial setup, you only need Step 6 onwards:
```bash
cd ~/Desktop/priyanka_tennis
bash start_program.sh
```

---

## 🌐 Pages & URLs

| Page                    | URL                              |
|-------------------------|----------------------------------|
| Book a Lesson           | http://127.0.0.1:5000/           |
| New Students            | http://127.0.0.1:5000/new-students |
| Private Tennis Lessons  | http://127.0.0.1:5000/private-tennis-lessons |
| Group Clinics           | http://127.0.0.1:5000/group-clinics |
| Progress Reports        | http://127.0.0.1:5000/progress-reports |
| Awards Ceremony         | http://127.0.0.1:5000/awards-ceremony |
| NorCal USTA Tournaments | http://127.0.0.1:5000/usta-tournament-information |
| Contact                 | http://127.0.0.1:5000/contact |
| About                   | http://127.0.0.1:5000/about |
| Design x Tennis         | http://127.0.0.1:5000/design-x-tennis |
| **Admin Dashboard**     | **http://127.0.0.1:5000/admin** |

---

## 📸 Adding Photos & Videos

1. Place **image files** (`.jpg`, `.png`, `.gif`, `.webp`) into `static/images/`
2. Place **video files** (`.mp4`, `.mov`) into `static/videos/`
3. Reference them in templates using:
   ```html
   <img src="{{ url_for('static', filename='images/your-photo.jpg') }}" alt="..." />
   <video src="{{ url_for('static', filename='videos/your-video.mp4') }}" autoplay muted loop></video>
   ```

---

## 🛠️ Troubleshooting

**"python3: command not found"**
→ Install Python from https://python.org/downloads or via Homebrew.

**"No module named flask"**
→ Run `bash start_environment.sh` again to reinstall dependencies.

**Port 5000 already in use**
→ Either stop the other process, or edit `app.py` last line to use a different port:
```python
app.run(debug=True, port=5001)
```

**Database errors**
→ Delete `instance/tennis_academy.db` and restart — it will be recreated automatically.

---

## 📞 Support

📍 Saratoga Country Club, Saratoga, CA  
📞 (408) 356-1967  
🌐 https://priyankastennisacademy.myportfolio.com
