from flask import Flask, render_template, request, redirect, url_for, flash
from settings import Session, DatabaseConfig
from models import Product, Order
from sqlalchemy import select

app = Flask(__name__)
app.config.from_object(DatabaseConfig)


@app.route("/")
def index():
    return render_template("index.html")


# Сторінка з усіма товарами
@app.route("/products")
def products():
    with Session() as session:
        stmt = select(Product)
        all_products = session.scalars(stmt).fetchall()
        # all_products = session.query(Product).all() # Взяття усіх товарів з БД

    return render_template(
        "products.html", products=all_products
    )  # Передача html-файлу разом з інформацією про товари


# Сторінка замовлення
@app.route("/order/<int:product_id>", methods=["GET", "POST"])
def order(product_id):
    with Session() as session:
        stmt = select(Product).where(Product.id == product_id)
        product = session.scalar(stmt)
        # product = session.query(Product).get(product_id) # Забираємо данні про товар за його id

        if not product:
            return "Товар не знайдено", 404

        if request.method == "POST":
            phone = request.form["phone"]
            email = request.form["email"]

            # Створюємо нове замовлення
            new_order = Order(phone=phone, email=email, product_id=product_id)
            session.add(new_order)
            session.commit()

            flash(f"Шузи: {product.name} замовлено!")
            return redirect(
                url_for("index")
            )  # Повертаємо користувача на головну сторінку

        return render_template(
            "order.html", product=product
        )  # Передаємо данні про товар разом з html-файлом


@app.route("/search", methods=["POST", "GET"])
def search():
    query = request.args.get("search")
    
    if request.method == "POST":
        query = request.form.get("search")
    
    if not query:
        flash("Будь ласка, введіть пошуковий запит.")
        return redirect(url_for("index"))

    with Session() as session:
        stmt = select(Product).where(Product.name.like(f"%{query}%")) # "SELECT * FROM products where name LIKE '%query%'" 
        products: Sequence[Product]|None = session.scalars(stmt).all()
    return render_template("products.html", products=products)


if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True, port=5050)
