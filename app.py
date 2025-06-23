from cgitb import text
from django.template import engines
from flask import Flask, flash, json, jsonify, render_template, redirect, request, session, url_for
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
import numpy as np
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import func
from models import Responden, db, Users
import joblib


app = Flask(__name__, template_folder='template', static_folder='static')
app.config['SECRET_KEY'] = 'gaya_belajar'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/gaya-belajar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index/')
def home():
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('index'))

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Login successful!', 'success')
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))  # Redirect to admin_dashboard for admin users
            else:
                return redirect(url_for('dashboard'))  # Redirect to dashboard for non-admin users
        else:
            flash('Login failed. Check your credentials.', 'danger')
            return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/test/', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        name = request.form['name']
        npm = request.form['npm']
        if name and npm:  
            session['name'] = name
            session['npm'] = npm
            return redirect('/form')  
        else:
            return "Form submission error: Name and NPM are required."
    return render_template('test.html')

@app.route('/form/', methods=['GET'])
def form():
    try:
        with open('questions.json', 'r') as f:
            questions = json.load(f)
    except FileNotFoundError:
        questions = []  # Jika file tidak ditemukan, berikan daftar kosong

    return render_template('form.html', questions=questions)


# Fungsi prediksi
def prediksi(X_test, prior, likelihood):
    y_pred = []
    for sampel in X_test:
        posteriors = {}
        for cls, prior_cls in prior.items():
            posterior = prior_cls
            for fitur_index in range(len(sampel)):
                nilai_fitur = sampel[fitur_index]
                if nilai_fitur in likelihood[cls][fitur_index]:
                    posterior *= likelihood[cls][fitur_index][nilai_fitur]
                else:
                    posterior *= 1e-6  # nilai smoothing kecil
            posteriors[cls] = posterior
        y_pred.append(max(posteriors, key=posteriors.get))
    return np.array(y_pred)

# Memuat model untuk dimensi
model_input = joblib.load('models/model_input.joblib')
model_processing = joblib.load('models/model_processing.joblib')
model_perception = joblib.load('models/model_perception.joblib')
model_understanding = joblib.load('models/model_understanding.joblib')

@app.route('/submit', methods=['POST'])
def submit_form():
    responses = []
    for key in request.form.keys():
        if key.startswith('responses_'):
            responses.append(int(request.form.get(key)))

    # Pastikan responses tidak kosong
    if not responses:
        return "No responses provided", 400

    # Konversi responses ke bentuk list of lists
    responses_list = [responses]

    try:
        # Predict learning styles
        pred_input = prediksi(responses_list, model_input['prior'], model_input['likelihood'])[0]
        pred_processing = prediksi(responses_list, model_processing['prior'], model_processing['likelihood'])[0]
        pred_perception = prediksi(responses_list, model_perception['prior'], model_perception['likelihood'])[0]
        pred_understanding = prediksi(responses_list, model_understanding['prior'], model_understanding['likelihood'])[0]
        
        name = session.get('name')
        npm = session.get('npm')

        # Simpan hasil prediksi ke dalam database
        new_user = Responden(name=name, npm=npm, responses=str(responses),
                             Input=pred_input,
                             Processing=pred_processing,
                             Perception=pred_perception,
                             Understanding=pred_understanding)

        db.session.add(new_user)
        db.session.commit()

        # Definisikan penjelasan dan saran berdasarkan prediksi
        explanations = {
            'Input': {
                'Visual': 'Anda lebih suka belajar dengan gambar dan diagram.',
                'Verbal': 'Anda lebih suka belajar dengan kata-kata tertulis dan lisan.'
            },
            'Processing': {
                'Aktif': 'Anda lebih suka belajar dengan berdiskusi dan bekerja dalam kelompok.',
                'Reflektif': 'Anda lebih suka belajar dengan merenung dan berpikir sendiri.'
            },
            'Perception': {
                'Sensitif': 'Anda lebih suka belajar dengan fakta dan contoh konkret.',
                'Intuitif': 'Anda lebih suka belajar dengan konsep dan teori abstrak.'
            },
            'Understanding': {
                'Sekuensial': 'Anda lebih suka belajar dengan cara teratur dan bertahap.',
                'Global': 'Anda lebih suka belajar dengan melihat gambaran besar terlebih dahulu.'
            }
        }

        suggestions = {
            'Input': {
                'Visual': 'Gunakan diagram, grafik, dan gambar untuk memahami materi.',
                'Verbal': 'Cobalah membaca buku teks dan mendengarkan ceramah untuk belajar.'
            },
            'Processing': {
                'Aktif': 'Cobalah bergabung dalam kelompok belajar dan berpartisipasi aktif dalam diskusi.',
                'Reflektif': 'Luangkan waktu untuk merenung dan mencatat poin-poin penting setelah belajar.'
            },
            'Perception': {
                'Sensitif': 'Cobalah belajar dengan menggunakan contoh konkret dan aplikasi nyata.',
                'Intuitif': 'Luangkan waktu untuk memahami konsep dan teori yang mendasari materi.'
            },
            'Understanding': {
                'Sekuensial': 'Belajarlah secara teratur dan ikuti langkah-langkah bertahap.',
                'Global': 'Cobalah memahami gambaran besar dari materi sebelum mendalami detail.'
            }
        }

        return render_template('results.html', result={
            'name': name,
            'npm': npm,
            'Input': pred_input,
            'Processing': pred_processing,
            'Perception': pred_perception,
            'Understanding': pred_understanding,
            'explanations': explanations,
            'suggestions': suggestions
        })

    except ValueError as e:
        print("ValueError:", e)
        return str(e)
       
@app.route('/results/')
def results():
    return render_template('results.html')


@app.route('/admin_dashboard/')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/manage_user/')
def manage_user():
    # Query pengguna yang bukan admin
    users = Users.query.filter_by(is_admin=False).all()
    
    # Render template dengan mengirimkan daftar pengguna yang sudah difilter
    return render_template('manage_user.html', users=users)

@app.route('/identification_report/')
def identification_report():
    try:
        # Ambil semua data responden dari database
        all_respondents = Responden.query.all()

        # Siapkan data untuk dikirim ke HTML
        report_data = []
        for respondent in all_respondents:
            report_data.append({
                'id': respondent.id,
                'name': respondent.name,
                'npm': respondent.npm,
                'Input': respondent.Input,
                'Perception': respondent.Perception,
                'Processing': respondent.Processing,
                'Understanding': respondent.Understanding
            })

        return render_template('identification_report.html', report_data=report_data)
    
    except Exception as e:
        return str(e)

@app.route('/api/Responden/<int:id>', methods=['DELETE'])
def delete_assessment(id):
    asessment = Responden.query.get_or_404(id)
    db.session.delete(asessment)
    db.session.commit()
    return jsonify(message="User deleted successfully"), 200

@app.route('/dashboard/')
def dashboard():
    try:
        # Ambil semua data responden dari database
        all_respondents = Responden.query.all()

        # Siapkan data untuk dikirim ke HTML
        report_data = []
        for respondent in all_respondents:
            report_data.append({
                'name': respondent.name,
                'npm': respondent.npm,
                'Input': respondent.Input,
                'Perception': respondent.Perception,
                'Processing': respondent.Processing,
                'Understanding': respondent.Understanding
            })

        return render_template('dashboard.html', report_data=report_data)
    
    except Exception as e:
        return str(e)
    
@app.route('/rekap')
def rekap():
    return render_template('rekap.html')

@app.route('/rekapitulasi_admin')
def rekapitulasi_admin():
    return render_template('rekapitulasi.html')

@app.route('/rekapitulasi', methods=['GET'])
def rekapitulasi():
    # Aggregate the counts for each learning style
    results = {
        "Input": {},
        "Processing": {},
        "Perception": {},
        "Understanding": {}
    }
    
    # Query and count occurrences for each dimension
    for dimension in results.keys():
        count = db.session.query(
            getattr(Responden, dimension), func.count().label('count')
        ).group_by(getattr(Responden, dimension)).all()
        
        total_count = sum(row.count for row in count)
        
        for value, count in count:
            results[dimension][value] = {
                "count": count,
                "percentage": (count / total_count) * 100 if total_count > 0 else 0
            }
    
    return jsonify(results)


@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        username = data['username']
        email = data['email']
        password = data['password']

        if not username or not email or not password:
            return jsonify({'message': 'Missing fields'}), 400

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user instance
        new_user = Users(username=username, email=email, password=hashed_password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User added successfully'}), 201

    except KeyError as e:
        return jsonify({'message': f'Missing key: {e}'}), 400
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to add user: {e}")
        return jsonify({'message': 'Failed to add user'}), 500

@app.route('/api/users/<int:id>', methods=['PUT'])
def edit_user(id):
    data = request.get_json()
    user = Users.query.get_or_404(id)
    user.username = data['username']
    user.email = data['email']
    if data['password']:
        user.password = data['password']
    db.session.commit()
    return jsonify(message="User updated successfully"), 200

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(message="User deleted successfully"), 200

    
@app.route('/api/counts', methods=['GET'])
def get_counts():
    student_count = Responden.query.count()
    teacher_count = Users.query.filter_by(is_admin=False).count()
    return jsonify({
        'student_count': student_count,
        'teacher_count': teacher_count
    })



if __name__ == '__main__':
    app.run(debug=True)
