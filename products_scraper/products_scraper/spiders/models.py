from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    fecha = Column(Date)
    imagen = Column(String)
    nombre = Column(String)
    distribuidor = Column(String)
    codigo=Column(String)
    precio = Column(Float)

# Reemplaza los siguientes valores con los de tu configuración de MySQL
DATABASE_URL ="postgresql+psycopg2://mypinga:2xauq08ifk8XXs0Hpl8ijHKsGSNpb2W1@dpg-cgjacvgrjeniuke5lqvg-a.frankfurt-postgres.render.com/products_box5"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)