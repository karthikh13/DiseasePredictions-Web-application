from flask import Flask, render_template, request, flash
import os
import pickle

app = Flask(__name__)
app.secret_key = "secret key"

# ---------- Load Models ----------
working_dir = os.path.dirname(os.path.abspath(__file__))

model_paths = {
    "diabetes": 'saved_models/diabetes_model.sav',
    "heart": 'saved_models/heart_disease_model.sav',
    "parkinsons": 'saved_models/parkinsons_model.sav'
}

models = {}

for name, path in model_paths.items():
    try:
        models[name] = pickle.load(open(os.path.join(working_dir, path), 'rb'))
    except Exception as e:
        print(f"Error loading {name} model: {e}")

# ---------- Routes ----------

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/parkinsons', methods=['POST'])
def predict_parkinsons():
    fields = [
        'fo', 'fhi', 'flo', 'jitter_percent', 'jitter_abs', 'rap', 'ppq',
        'ddp', 'shimmer', 'shimmer_db', 'apq3', 'apq5', 'apq', 'dda',
        'nhr', 'hnr', 'rpde', 'dfa', 'spread1', 'spread2', 'd2', 'ppe'
    ]
    try:
        user_input = [float(request.form[field]) for field in fields]
        prediction = models["parkinsons"].predict([user_input])[0]

        if prediction == 1:
            flash("The person has Parkinson's disease", 'warning')
        else:
            flash("The person does not have Parkinson's disease", 'success')

    except Exception as e:
        flash(f"Error processing input: {e}", 'warning')

    return render_template('parkinsons.html')


@app.route('/heart', methods=['POST'])
def predict_heart():
    fields = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ]
    try:
        user_input = [float(request.form[field]) for field in fields]
        prediction = models["heart"].predict([user_input])[0]

        if prediction == 1:
            flash("The person is having heart disease", 'warning')
        else:
            flash("The person does not have any heart disease", 'success')

    except Exception as e:
        flash(f"Error processing input: {e}", 'warning')

    return render_template('heart.html')


@app.route('/diabetes', methods=['POST'])
def predict_diabetes():
    fields = [
        'pregnancies', 'glucose', 'bloodPressure', 'skinThickness',
        'insulin', 'bmi', 'diabetesPedigreeFunction', 'age'
    ]
    try:
        user_input = [float(request.form[field]) for field in fields]
        prediction = models["diabetes"].predict([user_input])[0]

        if prediction == 1:
            flash("The person is diabetic", 'warning')
        else:
            flash("The person is not diabetic", 'success')

    except Exception as e:
        flash(f"Error processing input: {e}", 'warning')

    return render_template('diabetes.html')


# ---------- Navigation Pages ----------

@app.route('/heart_page')
def heart_page():
    return render_template('heart.html')


@app.route('/diabetes_page')
def diabetes_page():
    return render_template('diabetes.html')


@app.route('/parkinsons_page')
def parkinsons_page():
    return render_template('parkinsons.html')


# ---------- Run App ----------
if __name__ == '__main__':
    app.run(debug=True)
