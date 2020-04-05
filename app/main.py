import quart
import quart.flask_patch
import pymongo
import os
from werkzeug.security import check_password_hash
from app import config
from app.resources import login_form, add_form

is_heroku = os.environ.get("IS_HEROKU", False)

if is_heroku:
    mongocli = pymongo.MongoClient(os.environ.get("MONGODB_URI", ""))
else:
    mongocli = pymongo.MongoClient(config.MONGO_CONN, config.MONGO_PORT)
app = quart.Quart(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
mongodb = mongocli.litra


@app.route("/")
async def root():
    return quart.redirect("/index")


@app.route("/index")
async def index():
    answers = mongodb.qa.find(projection=("number", "question"))
    return await quart.render_template("index.html", title="Списать литру", answers=answers)


@app.route("/login", methods=("GET", "POST"))
async def login():
    form = login_form.LoginForm()
    if "logged_in" in quart.session and quart.session["logged_in"]:
        return quart.redirect("/add")
    if form.validate_on_submit():
        if check_password_hash(config.ADD_PASSWD_HASH, form.password.data):
            quart.session["logged_in"] = True
            return quart.redirect("/add")
        else:
            return await quart.render_template("login.html", form=form, title="login")
    else:
        return await quart.render_template("login.html", form=form, title="login")


@app.route("/add", methods=("GET", "POST"))
async def add():
    form = add_form.AddForm()
    if not ("logged_in" in quart.session and quart.session["logged_in"]):
        await quart.abort(403)
    if form.validate_on_submit():
        new_answer = {
            "number": form.number.data,
            "question": form.question.data,
            "answer": form.answer.data
        }
        old_answer = mongodb.qa.find_one({"number": form.number.data})
        if old_answer:
            mongodb.qa.replace_one({"_id": old_answer["_id"]}, new_answer)
        else:
            mongodb.qa.insert_one(new_answer)
        return quart.redirect("/index")
    else:
        return await quart.render_template("add.html", form=form, title="add")


@app.route("/answer/<int:number>")
async def answer(number):
    answer = mongodb.qa.find_one({"number": number})
    return await quart.render_template("answer.html", answer=answer)
