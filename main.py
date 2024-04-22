# crud/main.py
from fastapi import FastAPI, Request, Depends, Form, status, HTTPException
from fastapi.templating import Jinja2Templates
import models
from database import engine, sessionlocal
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    plants = db.query(models.Plant).order_by(models.Plant.id.desc())
    return templates.TemplateResponse("index.html", {"request": request, "plants": plants})

@app.post("/add")
async def add(request: Request, plant_name: str = Form(...), plant_scientific_name: str = Form(...), plant_type: str = Form(...),
                    ideal_temperature: int = Form(...), ideal_umidity: int = Form(...), db: Session = Depends(get_db)):
    print(plant_name)
    print(plant_scientific_name)
    print(plant_type)
    print(ideal_temperature)
    print(ideal_umidity)
    plants = models.Plant( plant_name=plant_name
                         , plant_scientific_name=plant_scientific_name
                         , plant_type=plant_type
                         , ideal_temperature=ideal_temperature
                         , ideal_umidity=ideal_umidity)
    db.add(plants)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)



@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})


@app.get("/edit/{id}")
async def edit(request: Request, id: int, db: Session = Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "plant": plant})


@app.post("/update/{id}")
async def update(request: Request, id: int, plant_name: str = Form(...), plant_scientific_name: str = Form(...), plant_type: str = Form(...),
                    ideal_temperature: int = Form(...), ideal_umidity: int = Form(...), db: Session = Depends(get_db)):
    plants = db.query(models.Plant).filter(models.Plant.id == id).first()
    if plants:
        plants.plant_name = plant_name
        plants.plant_scientific_name = plant_scientific_name
        plants.plant_type = plant_type
        plants.ideal_temperature = ideal_temperature
        plants.ideal_umidity = ideal_umidity
        db.commit()
        return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
    else:
        return HTTPException(status_code=404, detail="Plant not found")

@app.get("/delete/{id}")
async def delete(request: Request, id: int, db: Session = Depends(get_db)):
    plants = db.query(models.Plant).filter(models.Plant.id == id).first()
    db.delete(plants)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
