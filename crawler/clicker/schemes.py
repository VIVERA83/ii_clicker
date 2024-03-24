from pydantic import BaseModel


class CourseSchema(BaseModel):
    login: str
    password: str
    course: str
