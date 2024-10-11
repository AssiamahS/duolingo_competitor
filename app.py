from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spanish.db'
db = SQLAlchemy(app)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(150), nullable=False)
    spanish = db.Column(db.String(150), nullable=False)

class WordForm(FlaskForm):
    english = StringField('English', validators=[DataRequired()])
    spanish = StringField('Spanish', validators=[DataRequired()])
    submit = SubmitField('Add Word')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = WordForm()
    if form.validate_on_submit():
        new_word = Word(english=form.english.data, spanish=form.spanish.data)
        db.session.add(new_word)
        db.session.commit()
        return redirect(url_for('index'))
    words = Word.query.all()
    return render_template('index.html', form=form, words=words)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
