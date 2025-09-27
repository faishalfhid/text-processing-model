from flask import Flask, render_template, request
import pickle

# Load vectorizer dan model
model_path = "./models"
vectorizer = pickle.load(open(model_path + "/vectorizer_2.pkl", "rb"))
nb_model = pickle.load(open(model_path + "/naive_bayes_2.pkl", "rb"))
svm_model = pickle.load(open(model_path + "/svm_2.pkl", "rb"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction_nb, prediction_svm = None, None
    if request.method == "POST":
        message = request.form["message"]
        data = vectorizer.transform([message])

        prediction_nb = nb_model.predict(data)[0]
        prediction_svm = svm_model.predict(data)[0]

    return render_template("index.html", 
                           prediction_nb=prediction_nb, 
                           prediction_svm=prediction_svm)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
