from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, select, update
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/webapp_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Counter(Base):
    __tablename__ = "counter"
    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, nullable=False)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def increment_count(db: Session = Depends(get_db)):
    result = db.execute(select(Counter).where(Counter.id == 1)).first()
    counter = result[0]
    new_count = counter.count + 1
    db.execute(update(Counter).where(Counter.id == 1).values(count=new_count))
    db.commit()

    return {"count": new_count}

# Запуск сервісу:
# uvicorn main:app --reload
