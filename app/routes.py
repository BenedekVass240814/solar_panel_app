from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User
from . import db
import os
import uuid
from werkzeug.utils import secure_filename
from .ml_model.model import classify_image  # Import model function

# Blueprint for main routes
main_bp = Blueprint('main', __name__)

# Home route
@main_bp.route('/')
def home():
    return render_template('index.html')

# Login route
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Authenticate the user
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id  # Store user ID in session
            session["username"] = email[:email.index("@")]
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

# Register route
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')

        if password == repeat_password:
            if User.query.filter_by(email=email).first():
                flash('Email already exists', 'danger')
            else:
                new_user = User(email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('main.login'))
        else:
            flash('Passwords do not match', 'danger')
    
    return render_template('register.html')

# Profile route
@main_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('You must be logged in to access the profile page.', 'warning')
        return redirect(url_for('main.login'))

    user = User.query.get(session['user_id'])
    
    user_history = [
        {'action': h.action, 'image_path': h.image_path}
        for h in user.history
        ]

    return render_template('profile.html', user=user, user_history=user_history)

# Logout route
@main_bp.route('/logout')
def logout():
    session.clear()  # Clear session on logout
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

# Ensure uploads folder exists
UPLOAD_FOLDER = "app/static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Classification Route (Handles File Upload)
@main_bp.route("/classify", methods=["GET", "POST"])
def classify():
    if request.method == "POST":
        if "image" not in request.files:
            flash("No file uploaded!", "danger")
            return redirect(url_for("main.classify"))

        file = request.files["image"]

        if file.filename == "":
            flash("No selected file!", "danger")
            return redirect(url_for("main.classify"))

        if file:
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"  # Prevent name conflicts
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(file_path)

            # Classify the uploaded image
            predicted_class, conf = classify_image(file_path)

            # Define label mapping (adjust based on your model)
            label_map = ['Bird-drop', 'Clean', 'Dusty', 'Electrical-damage', 'Physical_damage', 'Snow-Covered']
            result_label = f"{label_map[predicted_class]} Confidence: {conf * 100:1.2f}%"

            image_path = f'uploads/{unique_filename}'  # Relative path to store in DB
            web_image_path = url_for('static', filename=image_path)  # Path used in the template

            # Save classification to user's history if logged in
            if 'user_id' in session:
                from .models import UserHistory
                new_history = UserHistory(
                    user_id=session['user_id'],
                    action=result_label,
                    image_path=image_path
                )
                db.session.add(new_history)
                db.session.commit()

            return render_template("classify.html", result=result_label, image_path=web_image_path)

    return render_template("classify.html")

@main_bp.route('/about')
def about():
    return render_template('about.html')  # Ensure about.html exists in the templates folder

@main_bp.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    # Get the feedback and classification result
    feedback = request.form.get("feedback")
    classification_result = request.form.get("classification_result")

    if feedback:
        # Store feedback in the session (this can be replaced with database if needed)
        session['feedback'] = {
            'result': classification_result,
            'feedback': feedback
        }
        flash(f"Thank you for your feedback! You marked this as {feedback}.", 'success')

    return redirect(url_for("main.classify"))
