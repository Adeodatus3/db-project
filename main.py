from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Books(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True, type_=Integer, name="id", unique=True)
  title: Mapped[str] = mapped_column(unique=True, nullable=False, type_=String, name="title")
  author: Mapped[str] = mapped_column(nullable=False,type_=String, name="author")
  rating: Mapped[float] = mapped_column(nullable=False, type_=Float, name="rating")



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-library-collection.db"

db.init_app(app)


# with app.app_context():
#   # db.create_all()
#
#   book_of_matthew = Books(id=1, title="Matthew's Good News", author="Matthew the Apostle", rating=11)
#
#   db.session.add(book_of_matthew)
#   db.session.commit()
#
#
#
# with app.app_context():
#     result = db.session.execute(db.select(Books).order_by(Books.title))
#     all_books = result.scalars().all()
#     print(all_books[0].title)

# all_books = []

@app.route('/', methods=["GET", "POST"])
def home():
    with app.app_context():
        result = db.session.execute(db.select(Books).order_by(Books.title))
        all_books = result.scalars().all()


    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add(id, delete=False):

    if request.method == "POST":
        name = request.form["Name"]
        author = request.form["Author"]
        rating = request.form["Rating"]

        new_book = Books(title=name, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()

        return redirect('/')


    return render_template("add.html")


@app.route('/edit/id=<id>', methods=["GET", "POST"])
def edit(id):
    with app.app_context():
        book = db.session.execute(db.select(Books).where(Books.id == id)).scalar()
        print(request.method)
        if request.method == "POST":
            new_rating = float(request.form["name"])
            book.rating=new_rating
            db.session.commit()
            print(book.rating)
            return redirect("/")

        #     print(new_rating)
        return render_template("edit.html",id=id, book=book)


def test():
    print("Hello")


if __name__ == "__main__":

    app.run(debug=True, port=5001)

