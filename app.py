from flask import (Flask, render_template, request, redirect,
                   url_for, flash, Response, session)
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
import re as _re

try:
    import requests as _req
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

# ── .env loader ──────────────────────────────────────────────
def load_env(path='.env'):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, _, v = line.partition('=')
                    os.environ.setdefault(k.strip(), v.strip())

load_env()

app = Flask(__name__)
app.config['SECRET_KEY']               = os.environ.get('SECRET_KEY', 'pta-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI']  = os.environ.get('DATABASE_URL', 'sqlite:///tennis_academy.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ── Lesson price map ─────────────────────────────────────────
LESSON_PRICES = {
    'junior-11':    80.00,
    'adult-11':     90.00,
    'semi-private': 60.00,
    'group-junior': 35.00,
    'group-youth':  30.00,
}

LESSON_LABELS = {
    'junior-11':    'Junior 1:1',
    'adult-11':     'Adult 1:1',
    'semi-private': 'Semi-Private 2:1',
    'group-junior': 'Junior Group Clinic',
    'group-youth':  'Youth Group Clinic',
}

@app.context_processor
def inject_globals():
    return {
        'now':        datetime.utcnow(),
        'today':      date.today().isoformat(),
        'ten_to_8_id': os.environ.get('TEN_TO_8_BOOKING_ID', 'wqixcxvilwcwdsyfpp'),
        'LESSON_LABELS': LESSON_LABELS,
    }

# ════════════════════════════════════════════════════════
#  MODELS
# ════════════════════════════════════════════════════════

class Booking(db.Model):
    id             = db.Column(db.Integer,     primary_key=True)
    first_name     = db.Column(db.String(60),  nullable=False)
    last_name      = db.Column(db.String(60),  nullable=False)
    email          = db.Column(db.String(120), nullable=False)
    phone          = db.Column(db.String(30),  nullable=False)
    lesson_type    = db.Column(db.String(50),  nullable=False)
    court          = db.Column(db.String(30),  default='Court 1')
    duration       = db.Column(db.String(20),  default='1 hour')
    preferred_date = db.Column(db.String(20),  nullable=False)
    preferred_time = db.Column(db.String(20),  nullable=False)
    skill_level    = db.Column(db.String(30),  default='Beginner')
    notes          = db.Column(db.Text)
    price          = db.Column(db.Float,       default=0.0)
    status         = db.Column(db.String(20),  default='Confirmed')
    created_at     = db.Column(db.DateTime,    default=datetime.utcnow)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def day_of_week(self):
        try:
            return datetime.strptime(self.preferred_date, '%Y-%m-%d').strftime('%A')
        except Exception:
            return ''

    @property
    def display_date(self):
        try:
            return datetime.strptime(self.preferred_date, '%Y-%m-%d').strftime('%b %d, %Y')
        except Exception:
            return self.preferred_date

    @property
    def lesson_label(self):
        return LESSON_LABELS.get(self.lesson_type, self.lesson_type)


class Student(db.Model):
    id            = db.Column(db.Integer,     primary_key=True)
    name          = db.Column(db.String(120), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    phone         = db.Column(db.String(30))
    age           = db.Column(db.Integer)
    skill_level   = db.Column(db.String(30))
    lesson_type   = db.Column(db.String(50))
    enrolled_date = db.Column(db.DateTime, default=datetime.utcnow)


class ProgressReport(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    student_id  = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    student     = db.relationship('Student', backref='reports')
    report_date = db.Column(db.String(20), nullable=False)
    forehand    = db.Column(db.Integer, default=5)
    backhand    = db.Column(db.Integer, default=5)
    serve       = db.Column(db.Integer, default=5)
    volley      = db.Column(db.Integer, default=5)
    footwork    = db.Column(db.Integer, default=5)
    strategy    = db.Column(db.Integer, default=5)
    consistency = db.Column(db.Integer, default=5)
    notes       = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)


class ContactMessage(db.Model):
    id         = db.Column(db.Integer,     primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(120), nullable=False)
    phone      = db.Column(db.String(30))
    subject    = db.Column(db.String(200))
    message    = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read    = db.Column(db.Boolean,  default=False)


class AwardsCeremony(db.Model):
    id            = db.Column(db.Integer,     primary_key=True)
    student_name  = db.Column(db.String(120), nullable=False)
    award_title   = db.Column(db.String(200), nullable=False)
    ceremony_date = db.Column(db.String(20),  nullable=False)
    description   = db.Column(db.Text)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)


class Tournament(db.Model):
    id                    = db.Column(db.Integer,     primary_key=True)
    name                  = db.Column(db.String(200), nullable=False)
    location              = db.Column(db.String(200))
    date                  = db.Column(db.String(20))
    level                 = db.Column(db.String(50))
    age_group             = db.Column(db.String(50))
    registration_deadline = db.Column(db.String(20))
    usta_link             = db.Column(db.String(500))
    notes                 = db.Column(db.Text)
    created_at            = db.Column(db.DateTime, default=datetime.utcnow)


# ════════════════════════════════════════════════════════
#  MULTI-STEP BOOKING
# ════════════════════════════════════════════════════════

@app.route('/')
def index():
    return redirect(url_for('book_a_lesson'))


@app.route('/book-a-lesson', methods=['GET', 'POST'])
def book_a_lesson():
    if request.method == 'GET':
        return render_template('book_a_lesson.html', step=1, form_data={})

    step      = int(request.form.get('step', 1))
    form_data = {k: v for k, v in request.form.items() if k != 'step'}

    # Step 1 → 2
    if step == 1:
        missing = []
        if not form_data.get('lesson_type'):    missing.append('a lesson type')
        if not form_data.get('preferred_date'): missing.append('a date')
        if not form_data.get('preferred_time'): missing.append('a time slot')
        if missing:
            flash(f'Please select {" and ".join(missing)}.', 'warning')
            return render_template('book_a_lesson.html', step=1, form_data=form_data)
        return render_template('book_a_lesson.html', step=2, form_data=form_data)

    # Step 2 → 3
    elif step == 2:
        missing = []
        if not form_data.get('first_name'): missing.append('your first name')
        if not form_data.get('last_name'):  missing.append('your last name')
        if not form_data.get('email'):      missing.append('your email')
        if not form_data.get('phone'):      missing.append('your phone number')
        if missing:
            flash(f'Please provide {" and ".join(missing)}.', 'warning')
            return render_template('book_a_lesson.html', step=2, form_data=form_data)
        return render_template('book_a_lesson.html', step=3, form_data=form_data)

    # Step 3 → Save + Success
    elif step == 3:
        lesson_type = form_data.get('lesson_type', 'adult-11')
        price       = LESSON_PRICES.get(lesson_type, 0.0)
        booking = Booking(
            first_name     = form_data.get('first_name', ''),
            last_name      = form_data.get('last_name', ''),
            email          = form_data.get('email', ''),
            phone          = form_data.get('phone', ''),
            lesson_type    = lesson_type,
            court          = form_data.get('court', 'Court 1'),
            duration       = form_data.get('duration', '1 hour'),
            preferred_date = form_data.get('preferred_date', ''),
            preferred_time = form_data.get('preferred_time', ''),
            skill_level    = form_data.get('skill_level', 'Beginner'),
            notes          = form_data.get('notes', ''),
            price          = price,
            status         = 'Confirmed',
        )
        db.session.add(booking)
        db.session.commit()
        return render_template('book_a_lesson.html',
                               step=4,
                               booking_id=booking.id,
                               confirmation=booking,
                               form_data=form_data)

    return redirect(url_for('book_a_lesson'))


# ════════════════════════════════════════════════════════
#  PUBLIC PAGES
# ════════════════════════════════════════════════════════

@app.route('/new-students')
def new_students():
    return render_template('new_students.html')

@app.route('/private-tennis-lessons')
def private_tennis_lessons():
    return render_template('private_tennis_lessons.html')

@app.route('/group-clinics')
def group_clinics():
    return render_template('group_clinics.html')

@app.route('/progress-reports', methods=['GET', 'POST'])
def progress_reports():
    if request.method == 'POST':
        db.session.add(ProgressReport(
            student_id  = request.form['student_id'],
            report_date = request.form['report_date'],
            forehand    = int(request.form.get('forehand',    5)),
            backhand    = int(request.form.get('backhand',    5)),
            serve       = int(request.form.get('serve',       5)),
            volley      = int(request.form.get('volley',      5)),
            footwork    = int(request.form.get('footwork',    5)),
            strategy    = int(request.form.get('strategy',    5)),
            consistency = int(request.form.get('consistency', 5)),
            notes       = request.form.get('notes', '')
        ))
        db.session.commit()
        flash('Progress report saved!', 'success')
        return redirect(url_for('admin'))
    students = Student.query.all()
    return render_template('progress_reports.html', students=students)


@app.route('/progress-reports/lookup', methods=['GET', 'POST'])
def lookup_progress():
    reports, student_name = [], ''
    if request.method == 'POST':
        email   = request.form.get('email', '')
        student = Student.query.filter_by(email=email).first()
        if student:
            reports      = ProgressReport.query.filter_by(student_id=student.id) \
                               .order_by(ProgressReport.created_at.desc()).all()
            student_name = student.name
        else:
            flash('No student found with that email.', 'warning')
    return render_template('lookup_progress.html', reports=reports, student_name=student_name)


@app.route('/awards-ceremony')
def awards_ceremony():
    awards = AwardsCeremony.query.order_by(AwardsCeremony.ceremony_date.desc()).all()
    return render_template('awards_ceremony.html', awards=awards)


@app.route('/usta-tournament-information')
def usta_tournaments():
    tournaments = Tournament.query.order_by(Tournament.date).all()
    return render_template('usta_tournaments.html', tournaments=tournaments)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        db.session.add(ContactMessage(
            name    = request.form['name'],
            email   = request.form['email'],
            phone   = request.form.get('phone', ''),
            subject = request.form.get('subject', ''),
            message = request.form['message']
        ))
        db.session.commit()
        flash('Message sent! Coach Priyanka will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/design-x-tennis')
def design_x_tennis():
    return render_template('design_x_tennis.html')


# ════════════════════════════════════════════════════════
#  10to8 SERVER-SIDE PROXY  (bypasses X-Frame-Options)
# ════════════════════════════════════════════════════════

@app.route('/booking-proxy')
def booking_proxy():
    bid        = os.environ.get('TEN_TO_8_BOOKING_ID', 'wqixcxvilwcwdsyfpp')
    target_url = f'https://{bid}.10to8.com'
    if not REQUESTS_OK:
        return Response(
            f'<p style="padding:32px;font-family:sans-serif;">Install requests: '
            f'<code>pip install requests</code> — or '
            f'<a href="{target_url}" target="_top">open directly</a></p>',
            content_type='text/html')
    try:
        hdrs = {'User-Agent': 'Mozilla/5.0', 'Accept': 'text/html'}
        resp = _req.get(target_url, headers=hdrs, timeout=12, allow_redirects=True)
        html = resp.text
        html = html.replace('<head>', f'<head><base href="{target_url}/" target="_top">', 1)
        html = _re.sub(r'(href|src)="/((?!/))',
                       lambda m: f'{m.group(1)}="{target_url}/{m.group(2)}', html)
        html = _re.sub(r'<meta[^>]*x-frame-options[^>]*>', '', html, flags=_re.IGNORECASE)
        html = html.replace('<a ', '<a target="_top" ')
        return Response(html, content_type='text/html; charset=utf-8')
    except Exception as exc:
        return Response(
            f'<p style="padding:40px;font-family:sans-serif;">Could not load calendar. '
            f'<a href="{target_url}" target="_top" style="color:#2BB5AC;">Open directly →</a>'
            f'<br><small style="color:#aaa;">{exc}</small></p>',
            content_type='text/html')


# ════════════════════════════════════════════════════════
#  ADMIN — bookings with filters + cancel / delete
# ════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════
#  ADMIN AUTHENTICATION
# ════════════════════════════════════════════════════════

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'tennis2024')

def admin_required(f):
    """Decorator — redirects to login if not authenticated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the admin dashboard.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # Already logged in → go straight to dashboard
    if session.get('admin_logged_in'):
        return redirect(url_for('admin'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session.permanent = False          # ends when browser closes
            flash('Welcome back, Coach Priyanka! 🎾', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Incorrect password. Please try again.', 'danger')

    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('admin_login'))


@app.route('/admin')
@admin_required
def admin():
    by_date   = request.args.get('by_date',   '')
    by_day    = request.args.get('by_day',    '')
    by_lesson = request.args.get('by_lesson', '')
    by_status = request.args.get('by_status', '')

    q = Booking.query
    if by_date:   q = q.filter(Booking.preferred_date == by_date)
    if by_lesson: q = q.filter(Booking.lesson_type    == by_lesson)
    if by_status: q = q.filter(Booking.status         == by_status)

    bookings = q.order_by(Booking.preferred_date, Booking.preferred_time).all()

    if by_day:
        bookings = [b for b in bookings if b.day_of_week == by_day]

    total_revenue = sum(
        b.price for b in bookings if b.status == 'Confirmed'
    )

    students    = Student.query.order_by(Student.name).all()
    messages    = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    awards      = AwardsCeremony.query.order_by(AwardsCeremony.ceremony_date.desc()).all()
    tournaments = Tournament.query.order_by(Tournament.date).all()

    return render_template('admin.html',
        bookings=bookings,
        total_revenue=total_revenue,
        students=students,
        messages=messages,
        awards=awards,
        tournaments=tournaments,
        filters=dict(by_date=by_date, by_day=by_day,
                     by_lesson=by_lesson, by_status=by_status),
        lesson_types=list(LESSON_PRICES.keys()),
        days=['Monday','Tuesday','Wednesday','Thursday',
              'Friday','Saturday','Sunday'],
    )


@app.route('/admin/booking/<int:id>/cancel', methods=['POST'])
@admin_required
def cancel_booking(id):
    b = Booking.query.get_or_404(id)
    b.status = 'Cancelled'
    db.session.commit()
    flash(f'Booking #{id} ({b.full_name}) has been cancelled.', 'success')
    return redirect(url_for('admin') + _preserve_args())


@app.route('/admin/booking/<int:id>/delete', methods=['POST'])
@admin_required
def delete_booking(id):
    b = Booking.query.get_or_404(id)
    name = b.full_name
    db.session.delete(b)
    db.session.commit()
    flash(f'Booking #{id} ({name}) permanently deleted.', 'success')
    return redirect(url_for('admin') + _preserve_args())


def _preserve_args():
    """Re-apply current query-string filters after redirect."""
    args = {k: v for k, v in request.form.items() if k.startswith('filter_')}
    return ''  # simple version — returns to unfiltered admin


@app.route('/admin/student/add', methods=['POST'])
@admin_required
def add_student():
    db.session.add(Student(
        name        = request.form['name'],
        email       = request.form['email'],
        phone       = request.form.get('phone', ''),
        age         = int(request.form['age']) if request.form.get('age') else None,
        skill_level = request.form.get('skill_level', ''),
        lesson_type = request.form.get('lesson_type', ''),
    ))
    db.session.commit()
    flash('Student added!', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/award/add', methods=['POST'])
@admin_required
def add_award():
    db.session.add(AwardsCeremony(
        student_name  = request.form['student_name'],
        award_title   = request.form['award_title'],
        ceremony_date = request.form['ceremony_date'],
        description   = request.form.get('description', ''),
    ))
    db.session.commit()
    flash('Award added!', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/tournament/add', methods=['POST'])
@admin_required
def add_tournament():
    db.session.add(Tournament(
        name                  = request.form['name'],
        location              = request.form.get('location', ''),
        date                  = request.form.get('date', ''),
        level                 = request.form.get('level', ''),
        age_group             = request.form.get('age_group', ''),
        registration_deadline = request.form.get('registration_deadline', ''),
        usta_link             = request.form.get('usta_link', ''),
        notes                 = request.form.get('notes', ''),
    ))
    db.session.commit()
    flash('Tournament added!', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/message/<int:id>/read', methods=['POST'])
@admin_required
def mark_message_read(id):
    msg = ContactMessage.query.get_or_404(id)
    msg.is_read = True
    db.session.commit()
    return redirect(url_for('admin'))


# ════════════════════════════════════════════════════════
#  SEED DATA
# ════════════════════════════════════════════════════════

def seed_data():
    if Tournament.query.count() == 0:
        db.session.add_all([
            Tournament(name='NorCal Junior Open - Level 5',
                       location='San Jose, CA', date='2025-02-15',
                       level='Level 5', age_group='18 & Under',
                       registration_deadline='2025-02-08',
                       usta_link='https://www.usta.com/en/home/play/youth-tennis/programs/northerncalifornia/junior-competition.html'),
            Tournament(name='Bay Area Closed Championships - Level 3',
                       location='Saratoga, CA', date='2025-03-22',
                       level='Level 3', age_group='18 & Under',
                       registration_deadline='2025-03-15',
                       usta_link='https://www.usta.com/en/home/play/youth-tennis/programs/northerncalifornia/junior-competition.html'),
            Tournament(name='Silicon Valley Invitational - Level 4',
                       location='Cupertino, CA', date='2025-04-10',
                       level='Level 4', age_group='12 & Under / 16 & Under',
                       registration_deadline='2025-04-03',
                       usta_link='https://www.usta.com/en/home/play/youth-tennis/programs/northerncalifornia/junior-competition.html'),
        ])
    if AwardsCeremony.query.count() == 0:
        db.session.add_all([
            AwardsCeremony(student_name='Alex M.',
                           award_title='Most Improved Player – Spring 2024',
                           ceremony_date='2024-06-15',
                           description='Remarkable improvement in serve consistency and footwork.'),
            AwardsCeremony(student_name='Sofia R.',
                           award_title='Outstanding Sportsmanship – Fall 2024',
                           ceremony_date='2024-11-20',
                           description='Demonstrated exceptional respect and positive attitude.'),
            AwardsCeremony(student_name='Ethan L.',
                           award_title='Junior Champion – Summer 2024',
                           ceremony_date='2024-08-10',
                           description='Top performer in the junior group clinic tournament series.'),
        ])
    db.session.commit()


# ════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True, port=5000)
