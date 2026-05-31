import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

DATA_FILE = "courses.json"


class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str


def load_courses():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_courses(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/courses")
def get_courses():
    try:
        return load_courses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/courses")
def add_course(course: Course):
    try:
        data = load_courses()
        new_course = course.model_dump()
        data.append(new_course)
        save_courses(data)
        return {
            "status": "success",
            "message": "New course successfully registered.",
            "data": new_course
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
