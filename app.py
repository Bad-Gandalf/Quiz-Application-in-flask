# coding: utf-8
import os
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from flask import Flask, session, render_template, url_for, redirect, request, flash

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.no_of_chance = 4

questions = { "1" : { "question" : "Which city is the capital of Iran?","options": ["Dhaka","Kabul","Tehran","Istambul"], "answer" : "Tehran"},
              "2" : { "question" : "What is the human bodys biggest organ?", "options": ['The cerebrum','Epidermis','Ribs','The skin'],"answer" : "The skin"},
              "3" : { "question" : "Electric current is typically measured in what units?","options": ['joule','Ampere','Watt','Ohm'], "answer" : "Ampere" },
	      "4" : { "question" : "Who was known as Iron man of India?","options": ["Govind Ballabh Pant","Jawaharlal Nehru","Subhash Chandra Bose","Sardar Vallabhbhai Patel"], "answer" : "Sardar Vallabhbhai Patel" },
              "5" : {"question" : "What is the smallest planet in the Solar System?", "options": ["Mercury","Mars","Jupitar","Neptune"],"answer":"Mercury"},
              "6": {'question': "What is the name of the largest ocean on earth?", "options": ["Atlantic","Pacafic", "Indian Ocean","Meditanarian"], "answer": "Pacafic" } ,
              "7": {'question': "What country has the second largest population in the world?", "options": ["Indonasia","America", "India","China"], "answer": "India" },
              "8": {'question': "Zurich is the largest city in what country?", "options": ["France","Spain", "Scotland","Switzerland"], "answer": "Switzerland" }, 
              "9": {'question': "What is the next prime number after 7?", "options": ["13","9", "17","11"], "answer": "11"},
              "10": {'question': "At what temperature is Fahrenheit equal to Centigrade?", "options": ["0 degrees ","-40 degrees", "213 degrees","-213 degrees"], "answer": "-40 degrees"} }


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == "POST":
    if "question" in session:
	    entered_answer = request.form.get('answer', '')
	    if questions.get(session["question"],False):
		    if entered_answer != questions[session["question"]]["answer"]:
			app.no_of_chance -= 1
			flash("Oops..Wrong Answer. Try again", "error")
		    
		    else:
		      if app.no_of_chance == 4:
			mark = 4
		      elif app.no_of_chance == 3:
			mark = 2
		      else:
			mark = 1
		      session["mark"] += mark
		      app.no_of_chance = 4
		      session["question"] = str(int(session["question"])+1)
		      if session["question"] in questions:
			redirect(url_for('index'))
		      else:
			return render_template("score.html", score = session["mark"])
	    else:
		return render_template("score.html", score = session["mark"])
  
  if "question" not in session:
    session["question"] = "1"
    session["mark"] = 0

  elif session["question"] not in questions:
    return render_template("score.html")
  return render_template("quiz.html",
                         question=questions[session["question"]]["question"],
                         question_number=session["question"],
			 options=questions[session["question"]]["options"],
                         score = session["mark"]
                         )

if __name__ == '__main__':
	app.run(debug=True)
