from base.base_accessor import BaseAccessor
from clicker.schemes import CourseTypeEnum
from store.clicker.courses import (
    CourseType,
    DispatcherCourseType,
    DriverCourseType,
    MentorCourseType,
    RatingCourseType,
    TrainingCourse,
)
from store.clicker.rename import CourseClicker


class ClickerAccessor(BaseAccessor):
    courses = {
        CourseTypeEnum.driver.value: DriverCourseType,
        CourseTypeEnum.dispatcher.value: DispatcherCourseType,
        CourseTypeEnum.mentor.value: MentorCourseType,
        CourseTypeEnum.rating.value: RatingCourseType,
    }

    async def start_clicker(
        self,
        login: str,
        password: str,
        course_type: CourseTypeEnum,
        courses: list[CourseType],
    ):
        type_course = self.courses.get(course_type.value)
        for course in courses:
            clicker = CourseClicker(
                login=login,
                password=password,
                training_course=TrainingCourse(type_course, course),
                min_sec_answer=5,
                max_sec_answer=10,
                logger=self.logger,
            )
            try:
                clicker.start_course()
            except Exception as ex:
                raise Exception(ex.args[0])
            finally:
                clicker.driver.quit()
        self.logger.info("Start protective driving course")
