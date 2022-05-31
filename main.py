from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from typing import Callable
from sqlalchemy import exc

app = Flask(__name__)
Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable
    Boolean: Callable


db = MySQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.String(250), nullable=False)
    has_wifi = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.String(250), nullable=False)
    can_take_calls = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class CafeForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    map_url = StringField("map_url", validators=[DataRequired(), URL()])
    img_url = StringField("img_url", validators=[DataRequired(), URL()])
    location = StringField("location", validators=[DataRequired()])
    seats = StringField("seats", validators=[DataRequired()])
    has_toilet = StringField("has_toilet", validators=[DataRequired()])
    has_wifi = StringField("has_wifi", validators=[DataRequired()])
    has_sockets = StringField("has_sockets", validators=[DataRequired()])
    can_take_calls = StringField("can_take_calls", validators=[DataRequired()])
    coffee_price = StringField("coffee_price", validators=[DataRequired()])

    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


# @app.route("/add", methods=["GET", "POST"])
# def add_cafe():
#     if request.method == "POST":
#         new_cafe = Cafe(name=request.form["name"],
#                         map_url=request.form["map_url"],
#                         img_url=request.form["img_url"],
#                         location=request.form["location"],
#                         seats=request.form["seats"],
#                         has_toilet=request.form["has_toilet"],
#                         has_wifi=request.form["has_wifi"],
#                         has_sockets=request.form["has_sockets"],
#                         can_take_calls=request.form["can_take_calls"],
#                         coffee_price=request.form["coffee_price"]
#                         )
#         try:
#             db.session.add(new_cafe)
#             db.session.commit()
#         except exc.IntegrityError:
#             db.session.rollback()
#         return redirect(url_for('cafes'))
#     return render_template('add.html')

@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(name=request.form["name"],
                        map_url=request.form["map_url"],
                        img_url=request.form["img_url"],
                        location=request.form["location"],
                        seats=request.form["seats"],
                        has_toilet=request.form["has_toilet"],
                        has_wifi=request.form["has_wifi"],
                        has_sockets=request.form["has_sockets"],
                        can_take_calls=request.form["can_take_calls"],
                        coffee_price=request.form["coffee_price"]
                        )
        try:
            db.session.add(new_cafe)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)

@app.route("/edit-post/<int:cafe_id>", methods=["GET", "POST"])
def edit_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    edit_form = CafeForm(
        name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        seats=cafe.seats,
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        has_sockets=cafe.has_sockets,
        can_take_calls=cafe.can_take_calls,
        coffee_price=cafe.coffee_price
    )
    if edit_form.validate_on_submit():
        cafe.name = edit_form.name.data
        cafe.map_url = edit_form.map_url.data
        cafe.img_url = edit_form.img_url.data
        cafe.location = edit_form.location.data
        cafe.seats = edit_form.seats.data
        cafe.has_toilet = edit_form.has_toilet.data
        cafe.has_sockets = edit_form.has_sockets.data
        cafe.can_take_calls = edit_form.can_take_calls.data
        cafe.coffee_price = edit_form.coffee_price.data

        db.session.commit()
        return redirect(url_for('cafes'))

    return render_template('add.html', form=edit_form, is_edit=True)

@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    post_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('cafes'))


@app.route('/cafes')
def cafes():
    cafes = db.session.query(Cafe).all()
    cafes = [cafe.to_dict() for cafe in cafes]
    header = ["ID", "Name", "Map URL", "Image URL", "Location", "Seats", "Has Toilet", "Has Wifi", "Has Sockets", "Can Take Calls", "Coffee Price"]
    return render_template('cafes.html', cafes=cafes, header=header)


if __name__ == '__main__':
    app.run(debug=True)
