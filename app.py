from flask import Flask, render_template, request,session,url_for,redirect
import joblib
import pandas as pd
model=joblib.load('model/model.pkl')
app = Flask(__name__)
app.secret_key = "qiuyeye234uy3rubfeyu"

@app.route("/", methods=["GET", "POST"])
def index():
    form_data = None
    prediction = None
    if request.method == "POST":
            form_data = request.form.to_dict()
            cgpa = float(request.form['cgpa'])
            iq = int(request.form['iq'])
            projects = int(request.form['projects'])
            communication = int(request.form['communication'])

 
            input_df = pd.DataFrame([{
                    'CGPA': cgpa,
                    'IQ': iq,
                    'Projects_Completed': projects,
                    'Communication_Skills': communication
                }])

            result = model.predict(input_df)[0]
            prediction = "Placed" if result == 1 else "Not Placed"
            session["prediction"] = prediction
            session["form_data"] = form_data
            return redirect(url_for("index"))

    prediction = session.pop("prediction", None)
    form_data = session.pop("form_data", None)
    return render_template("index.html", prediction=prediction,form_data=form_data)



if __name__ == '__main__':
    app.run(debug=True)