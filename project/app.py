import logging
from flask import Flask, render_template, Response, request, session, redirect, url_for, flash, stream_with_context
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import cv2
import squat
import legRaise
import BirdDog
import DumbbellCurl
import KneeTouch
from threading import Thread, Event
from datetime import datetime
import pytz
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import json
import time

# Flask application setup and configuration
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False
app.config['ENV'] = 'production'

# Logging configuration
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Set Flask and werkzeug log levels
werkzeug_log = logging.getLogger('werkzeug')
werkzeug_log.setLevel(logging.ERROR)

flask_log = logging.getLogger('flask.app')
flask_log.setLevel(logging.ERROR)

# Disable all logs
loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
for logger in loggers:
    logger.setLevel(logging.ERROR)
    logger.propagate = False

# Email server configuration
app.config['MAIL_SERVER'] = 'smtp.elasticemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'demo81440@gmail.com'
app.config['MAIL_PASSWORD'] = 'B6F9FDC29EA82B8B1249FAEF76BEEA6B616C'
app.config['MAIL_DEFAULT_SENDER'] = 'demo81440@gmail.com'

mail = Mail(app)
db = SQLAlchemy(app)
s = URLSafeTimedSerializer(app.secret_key)

# Istanbul time zone
ISTANBUL_TZ = pytz.timezone('Europe/Istanbul')

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ))

class UserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attribute_name = db.Column(db.String(50), nullable=False)
    old_value = db.Column(db.String(150), nullable=False)
    new_value = db.Column(db.String(150), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ))

class ExerciseType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_type_id = db.Column(db.Integer, db.ForeignKey('exercise_type.id'), nullable=False)
    repetitions = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ))
    duration = db.Column(db.Integer)
    exercise_type = db.relationship('ExerciseType', backref=db.backref('exercises', lazy=True))

class Session(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)

class SessionExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)

class WeightHeightUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ))

class PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ))

class EmailLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=lambda: datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ))

class UserSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    login_time = db.Column(db.DateTime, nullable=False)
    logout_time = db.Column(db.DateTime)

# Global variables and camera functions
exercise_counts = {
    'squat': 0,
    'legraise': 0,
    'birddog': 0,
    'dumbbellcurl': 0,
    'kneetouch': 0
}
was_below_threshold = False
camera_threads = {}
camera_stop_events = {}

exercise_modules = {
    'squat': squat,
    'legraise': legRaise,
    'birddog': BirdDog,
    'dumbbellcurl': DumbbellCurl,
    'kneetouch': KneeTouch
}

def start_camera_thread(selected_exercise):
    stop_event = Event()
    camera_stop_events[selected_exercise] = stop_event
    thread = Thread(target=generate_frames, args=(selected_exercise, stop_event))
    camera_threads[selected_exercise] = thread
    thread.start()

def stop_camera_thread(selected_exercise):
    if selected_exercise in camera_stop_events:
        camera_stop_events[selected_exercise].set()
        camera_threads[selected_exercise].join()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['logged_in'] = True
            session['user_id'] = user.id
            new_session = Session(user_id=user.id, start_time=datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ))
            db.session.add(new_session)
            db.session.commit()
            return redirect(url_for('select_exercises'))
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        user_session = Session.query.filter_by(user_id=user_id).order_by(Session.session_id.desc()).first()
        if user_session and user_session.end_time is None:
            user_session.end_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ)
            db.session.commit()
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        gender = request.form['gender']
        height = request.form['height']
        weight = request.form['weight']
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
        password = request.form['password']

        new_user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            gender=gender,
            height=height,
            weight=weight,
            dob=dob,
            password=password,
            created_at=datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ)
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html') 

# Select exercises route
@app.route('/select_exercises', methods=['GET', 'POST'])
def select_exercises():
    global exercise_counts
    if request.method == 'POST':
        selected_exercises = request.form.getlist('exercise')
        session['selected_exercises'] = selected_exercises
        for exercise in selected_exercises:
            if exercise not in camera_stop_events:
                camera_stop_events[exercise] = Event()
        exercise_counts = {exercise: 0 for exercise in exercise_counts}
        return redirect(url_for('exercise_page'))

    exercises = ["squat", "legraise", "birddog", "dumbbellcurl", "kneetouch"]
    exercise_images = {
        "squat": "images/squatexercise.png",
        "legraise": "images/legraiseexercise.png",
        "birddog": "images/birddogexercise.png",
        "dumbbellcurl": "images/dumbellcurlexercise.png",
        "kneetouch": "images/kneetouchexercise.png"
    }
    exercise_descriptions = {
        "squat": "Squat strengthens the legs, hips, and back muscles. Feet are shoulder-width apart, body leans back, and knees bend. It improves balance and supports calorie burning.",
        "legraise": "Leg Raise works the abdominal and hip muscles. Lying on the ground, lift your legs up straight while keeping your back on the floor. It strengthens core muscles and improves flexibility.",
        "birddog": "BirdDog works the back and abdominal muscles. Hands and knees are on the ground, one arm and the opposite leg are raised straight. It strengthens core muscles and balanced movements.",
        "dumbbellcurl": "Dumbbell Curl strengthens arm muscles. Dumbbells are held with palms facing up while standing, and arms are bent. It works the biceps muscles.",
        "kneetouch": "Knee Touch works the abdominal and hip muscles. While lying on the ground, hands are raised towards the knees. It strengthens core muscles and improves flexibility."
    }
    return render_template('select_exercises.html', exercises=exercises, exercise_images=exercise_images, exercise_descriptions=exercise_descriptions)

# Exercise page route
@app.route('/exercise')
def exercise_page():
    if 'selected_exercises' not in session:
        return redirect(url_for('select_exercises'))
    selected_exercises = session['selected_exercises']
    exercise_titles = [exercise.capitalize() for exercise in selected_exercises]
    exercise_images = {
        "squat": "images/squatexercise.png",
        "legraise": "images/legraiseexercise.png",
        "birddog": "images/birddogexercise.png",
        "dumbbellcurl": "images/dumbellcurlexercise.png",
        "kneetouch": "images/kneetouchexercise.png"
    }
    selected_exercise_images = {exercise.lower(): exercise_images[exercise.lower()] for exercise in selected_exercises}
    return render_template('exercise.html', exercise_titles=exercise_titles, exercise_images=selected_exercise_images, exercise_counts=exercise_counts)

# Camera frame generation function
def generate_frames(selected_exercise, stop_event):
    global exercise_counts, was_below_threshold

    try:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            logging.error("Unable to open camera.")
            return

        module = exercise_modules[selected_exercise]

        with module.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while not stop_event.is_set():
                success, frame = cap.read()
                if not success:
                    logging.error("Unable to receive frame from camera.")
                    break
                else:
                    logging.debug("Received frame from camera.")
                    frame, exercise_counts[selected_exercise], was_below_threshold = module.process_frame(
                        frame, pose, exercise_counts[selected_exercise], was_below_threshold)

                    cv2.putText(frame, f'{selected_exercise.capitalize()} Count: {exercise_counts[selected_exercise]}',
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    ret, buffer = cv2.imencode('.jpg', frame)
                    if not ret:
                        logging.error("Unable to encode frame.")
                        continue
                    frame = buffer.tobytes()
                    logging.debug("Encoded frame and sending.")
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        cap.release()
    except Exception as e:
        logging.error(f"Error generating frames: {e}")

# Video feed route
@app.route('/video_feed/<selected_exercise>')
def video_feed(selected_exercise):
    try:
        if selected_exercise not in camera_threads or not camera_threads[selected_exercise].is_alive():
            start_camera_thread(selected_exercise)
        return Response(generate_frames(selected_exercise, camera_stop_events[selected_exercise]), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        logging.error(f"Error generating video feed: {e}")
        return "An error occurred. Please try again.", 500

# Toggle camera route
@app.route('/toggle_camera/<selected_exercise>')
def toggle_camera(selected_exercise):
    if selected_exercise in camera_threads and camera_threads[selected_exercise].is_alive():
        stop_camera_thread(selected_exercise)
    else:
        start_camera_thread(selected_exercise)
    return redirect(url_for('exercise_page'))

# End exercise route
@app.route('/end_exercise')
def end_exercise():
    global exercise_counts
    exercise_titles = session.get('selected_exercises', [])
    user_id = session.get('user_id')
    for exercise in exercise_titles:
        exercise_type = ExerciseType.query.filter_by(name=exercise.lower()).first()
        repetitions = exercise_counts[exercise.lower()]
        new_exercise = Exercise(user_id=user_id, exercise_type_id=exercise_type.id, repetitions=repetitions, timestamp=datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ))
        db.session.add(new_exercise)
    db.session.commit()
    exercise_counts_to_display = {exercise: {'count': exercise_counts[exercise.lower()], 'name': exercise} for exercise in exercise_titles}
    return render_template('end_exercise.html', exercise_counts=exercise_counts_to_display)

# History route
@app.route('/history')
def history():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('login'))

    # Get date parameter from URL, use today's date if not provided
    date = request.args.get('date')
    if not date:
        date = datetime.now(ISTANBUL_TZ).strftime('%Y-%m-%d')

    selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    start_of_day = datetime.combine(selected_date, datetime.min.time()).replace(tzinfo=ISTANBUL_TZ)
    end_of_day = datetime.combine(selected_date, datetime.max.time()).replace(tzinfo=ISTANBUL_TZ)
    user_exercises = Exercise.query.filter_by(user_id=user_id).filter(Exercise.timestamp.between(start_of_day, end_of_day)).order_by(Exercise.timestamp.desc()).all()

    bmi = round(user.weight / ((user.height / 100) ** 2), 1)

    # Group exercises by time range
    grouped_exercises = {}
    for exercise in user_exercises:
        exercise_date = exercise.timestamp.astimezone(ISTANBUL_TZ).strftime('%Y-%m-%d %H:%M')
        if exercise_date not in grouped_exercises:
            grouped_exercises[exercise_date] = []
        grouped_exercises[exercise_date].append(exercise)

    no_data_message = None
    if not user_exercises:
        no_data_message = "No data available for the selected date."

    return render_template('history.html', user=user, grouped_exercises=grouped_exercises, bmi=bmi, date=date, no_data_message=no_data_message, ISTANBUL_TZ=ISTANBUL_TZ)

# Delete exercise route
@app.route('/delete_exercise/<int:exercise_id>', methods=['POST'])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    db.session.delete(exercise)
    db.session.commit()
    return redirect(url_for('history'))

# Settings route
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('login'))

    success_message = None
    feedback_success = False

    if request.method == 'POST':
        if 'email' in request.form:
            if user.firstname != request.form['firstname']:
                firstname_history = UserHistory(user_id=user_id, attribute_name='firstname', old_value=user.firstname, new_value=request.form['firstname'])
                db.session.add(firstname_history)
                user.firstname = request.form['firstname']
            
            if user.lastname != request.form['lastname']:
                lastname_history = UserHistory(user_id=user_id, attribute_name='lastname', old_value=user.lastname, new_value=request.form['lastname'])
                db.session.add(lastname_history)
                user.lastname = request.form['lastname']
            
            if user.email != request.form['email']:
                email_history = UserHistory(user_id=user_id, attribute_name='email', old_value=user.email, new_value=request.form['email'])
                db.session.add(email_history)
                user.email = request.form['email']
            
            if user.gender != request.form['gender']:
                gender_history = UserHistory(user_id=user_id, attribute_name='gender', old_value=user.gender, new_value=request.form['gender'])
                db.session.add(gender_history)
                user.gender = request.form['gender']
            
            if user.height != int(request.form['height']):
                height_history = UserHistory(user_id=user_id, attribute_name='height', old_value=str(user.height), new_value=request.form['height'])
                db.session.add(height_history)
                user.height = request.form['height']
            
            if user.weight != int(request.form['weight']):
                weight_history = UserHistory(user_id=user_id, attribute_name='weight', old_value=str(user.weight), new_value=request.form['weight'])
                db.session.add(weight_history)
                user.weight = request.form['weight']
            
            dob_new = datetime.strptime(request.form['dob'], '%Y-%m-%d')
            if user.dob != dob_new:
                dob_history = UserHistory(user_id=user_id, attribute_name='dob', old_value=user.dob.strftime('%Y-%m-%d'), new_value=request.form['dob'])
                db.session.add(dob_history)
                user.dob = dob_new
            
            if user.password != request.form['password']:
                password_history = UserHistory(user_id=user_id, attribute_name='password', old_value=user.password, new_value=request.form['password'])
                db.session.add(password_history)
                user.password = request.form['password']

            db.session.commit()

            bmi = round(user.weight / ((user.height / 100) ** 2), 1)
            weight_height_update = WeightHeightUpdate(user_id=user_id, height=user.height, weight=user.weight, bmi=bmi, updated_at=datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ))
            db.session.add(weight_height_update)
            db.session.commit()
            
            success_message = 'Settings updated successfully!'
        elif 'message' in request.form:
            message = request.form['message']
            feedback = Feedback(user_id=user.id, message=message, created_at=datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ))
            db.session.add(feedback)
            db.session.commit()

            msg = Message("Feedback from " + user.firstname + " " + user.lastname + " (PTWA)", recipients=['demo81440@gmail.com'])
            msg.body = f"Message from {user.firstname} {user.lastname} ({user.email}):\n\n{message}\n\nSent by PTWA"
            mail.send(msg)

            feedback_success = True

    return render_template('settings.html', user=user, success_message=success_message, feedback_success=feedback_success)

# Forgot password route
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt='email-confirm')
            reset_url = url_for('reset_password', token=token, _external=True)
            msg = Message("Password Reset Request (PTWA)", recipients=[email])
            msg.body = f"Hi {user.firstname},\n\nTo reset your password, please click the link below:\n{reset_url}\n\nIf you did not make this request, please ignore this email.\n\nSent by PTWA"
            mail.send(msg)

            password_reset = PasswordReset(user_id=user.id, token=token, created_at=datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(ISTANBUL_TZ))
            db.session.add(password_reset)
            db.session.commit()

            flash('Password reset email sent!', 'success')
        else:
            flash('Email address not found.', 'error')
    return render_template('forgot_password.html')

# Reset password route
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        user.password = password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)

# Reset route
@app.route('/reset')
def reset():
    global exercise_counts, was_below_threshold, camera_stop_events, camera_threads
    exercise_counts = {exercise: 0 for exercise in exercise_counts}
    was_below_threshold = False
    camera_stop_events = {}
    camera_threads = {}
    return redirect(url_for('index'))

# Update exercise counts route
@app.route('/update_counts')
def update_counts():
    def generate():
        while True:
            for exercise, count in exercise_counts.items():
                data = {'exercise': exercise, 'count': count}
                yield f"data: {json.dumps(data)}\n\n"
            time.sleep(1)

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

# Add exercise types to database
def populate_exercise_types():
    exercise_types = [
        {"name": "squat", "description": "Squat strengthens the legs, hips, and back muscles. Feet are shoulder-width apart, body leans back, and knees bend. It improves balance and supports calorie burning."},
        {"name": "legraise", "description": "Leg Raise works the abdominal and hip muscles. Lying on the ground, lift your legs up straight while keeping your back on the floor. It strengthens core muscles and improves flexibility."},
        {"name": "birddog", "description": "BirdDog works the back and abdominal muscles. Hands and knees are on the ground, one arm and the opposite leg are raised straight. It strengthens core muscles and balanced movements."},
        {"name": "dumbbellcurl", "description": "Dumbbell Curl strengthens arm muscles. Dumbbells are held with palms facing up while standing, and arms are bent. It works the biceps muscles."},
        {"name": "kneetouch", "description": "Knee Touch works the abdominal and hip muscles. While lying on the ground, hands are raised towards the knees. It strengthens core muscles and improves flexibility."}
    ]
    for exercise_type in exercise_types:
        existing_type = ExerciseType.query.filter_by(name=exercise_type["name"]).first()
        if not existing_type:
            new_exercise_type = ExerciseType(name=exercise_type["name"], description=exercise_type["description"])
            db.session.add(new_exercise_type)
    db.session.commit()

# Main application start
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        populate_exercise_types()
    app.run(debug=True, port=8085)
