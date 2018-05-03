from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.secret_key = 'development key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'usstates.sqlite')

db = SQLAlchemy(app)

class State(db.Model):
    __tablename__ = "states"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable = False)

class StateForm(FlaskForm):
    state = StringField('State', validators=[Required()])
    submit = SubmitField("submit")

def web_json_to_python_object(url):
    import json
    from urllib.request import urlopen

    with urlopen(url) as response:
        data = response.read() 
        return json.loads(data)


data = web_json_to_python_object("https://gist.githubusercontent.com/mshafrir/2646763/raw/8303e1d831e89cb8af24a11f2fa77353c317e408/states_titlecase.json")
db.create_all()
for item in data:
    state = State(name=item["name"])
    db.session.add(state)
    db.session.commit() 
@app.route('/')
def index():
    return "index Page"

@app.route("/states", methods=["GET", "POST"])
def states():
    form = StateForm()
    if form.validate_on_submit():
        pass #save on the database
    return render_template("states.html", form=form)
    


@app.route('/statelist')
def state_list():
    search_string = request.args.get("search_string")
    if search_string:
        states = State.query.filter(State.name.like(search_string + "%")).all()
        #countries = Country.query.filter(Country.name.contains(search_string))
        if states:
            result = '<ul id="state-list">'
            for state in states:
                result += '<li onClick="selectState(' + '\''+state.name + '\'' + ')">' + state.name + '</li>'
            result += '</ul>'
            response = jsonify(result)
            return response
    if search_string == "":
        response = jsonify("")
        return response



if __name__ == "__main__":
    app.run(debug=True)

