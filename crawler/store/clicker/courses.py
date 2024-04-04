from dataclasses import dataclass
from enum import Enum
from typing import Type, Union

from store.clicker.help import temp_db

TRAINING_TYPE = Union[
    Type["RatingCourseType"],
    Type["DriverCourseType"],
    Type["DispatcherCourseType"],
    Type["MentorCourseType"],
]


class CourseType(Enum):
    eco_full = "Эко вождение полный формат"
    # эко вождение малый формат
    eco_small = "Эко вождение малый формат"
    # защитное вождение
    protective_driving = "Защитное вождение"
    # итоговый тест водителя экспедитора С ПД
    final_test_c_pd = "Итоговый тест водителя экспедитора С ПД"
    # итоговый тест водителя экспедитора E ПД
    final_test_e_pd = "Итоговый тест водителя экспедитора E ПД"
    # итоговый тест водителя экспедитора E ТД
    final_test_e_td = "Итоговый тест водителя экспедитора E ТД"
    # итоговый тест водителя диспетчера
    final_test_dispatcher = "Итоговый тест водителя диспетчера"
    # итоговый тест водителя наставника
    final_test_mentor = "Итоговый тест водителя наставника"


# обучение по рейтингу
@dataclass
class RatingCourseType:
    doc_id = 6929760816126312392
    # эко вождение полный формат
    eco_full = 6924645368353934140
    # эко вождение малый формат
    eco_small = 6924643920544605730
    # защитное вождение
    protective_driving = 6961398061758971672


# обучение по водителя новичка (малый, полный, ТД)
@dataclass
class DriverCourseType:
    doc_id = 6929760465124534937
    # эко вождение полный формат
    eco_full = 6962058253449045800
    # эко вождение малый формат
    eco_small = 6962057914491621733
    # защитное вождение
    protective_driving = 6961397254143690746
    # итоговый тест водителя экспедитора С ПД
    final_test_c_pd = 6924580342161351460
    # итоговый тест водителя экспедитора E ПД
    final_test_e_pd = 6924577233538150324
    # итоговый тест водителя экспедитора E ТД
    final_test_e_td = 6924579316631872065


# обучение по диспетчеру новичка
@dataclass
class DispatcherCourseType:
    doc_id = 6929760181765629593
    # эко вождение полный формат
    eco_full = 6962058253449045800
    # эко вождение малый формат
    eco_small = 6962057914491621733
    # защитное вождение
    protective_driving = 6961397254143690746
    # итоговый тест водителя диспетчера
    final_test_dispatcher = 6924590130235968967


# обучение наставника
@dataclass
class MentorCourseType:
    doc_id = 6929761152024067205
    # эко вождение полный формат
    eco_full = 6962058253449045800
    # эко вождение малый формат
    eco_small = 6962057914491621733
    # защитное вождение
    protective_driving = 6961397254143690746
    # итоговый тест водителя наставника
    final_test_mentor = 6924653197752958377


class TrainingCourse:

    def __init__(self, training_type: TRAINING_TYPE, course: CourseType):
        self.mode = "course"
        self.training_type = training_type
        self.course = course

    def get_questions(self) -> dict[str, str]:
        return temp_db.get(self.course.name, {})

    def get_params(self) -> dict:
        return {
            "mode": self.mode,
            "doc_id": self.training_type.doc_id,
            "object_id": getattr(self.training_type, self.course.name),
        }

