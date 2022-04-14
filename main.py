from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class add_books(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), unique=False, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


# all_books = []

db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(add_books).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = add_books(title=request.form["book_name"], author=request.form["book_author"],
                             rating=request.form["book_rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    if request.method == "GET":
        book_id = request.args.get("id")
        book_selected = add_books.query.get(book_id)
        return render_template("edit.html", book_selected=book_selected)
    else:
        book_id = request.form.get("id")
        updated_rating = request.form.get("new_rating")
        book_to_update = add_books.query.filter_by(id=book_id).first()
        book_to_update.rating = updated_rating
        db.session.commit()
        return redirect(url_for('home'))


@app.route("/delete",methods=["POST","GET"])
def delete_book():
    book_id = request.args.get("id")
    book_selected = add_books.query.get(book_id)
    db.session.delete(book_selected)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
