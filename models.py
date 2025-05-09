from settings import Base, Session
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


# Модель для таблиці "Товари"
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    image_filename: Mapped[str] = mapped_column(String(255), nullable=False)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="product")


# Модель для таблиці "Замовлення"
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    product: Mapped["Product"] = relationship("Product", back_populates="orders")


# Ініціалізація бази даних і додавання товарів
def init_db():
    base = Base()
    base.drop_db()
    base.create_db()  # Створюємо таблиці

    with Session() as session:
        products = [
            Product(
                name="Nike Air Max",
                description="Класичні кросівки для бігу",
                price=4300,
                image_filename="nike_air_max.png",
            ),
            Product(
                name="Adidas Ultraboost",
                description="Легкі та комфортні кросівки",
                price=3100,
                image_filename="adidas_ultraboost.png",
            ),
            Product(
                name="Puma RS-X",
                description="Стильні кросівки для міста",
                price=3750.50,
                image_filename="puma_rsx.png",
            ),
        ]
        session.add_all(products)
        session.commit()


if __name__ == "__main__":
    init_db()
