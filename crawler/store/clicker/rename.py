from random import randint
from time import sleep
from typing import Any

from icecream import ic
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from temp.magnit.backoff import before_execution
import asyncio
import abc


class BaseClicker(abc.ABC):
    START_URL = "https://tvoy.magnit.ru/"
    MAGNUM_URL = "https://magnum.magnit.ru/view_doc.html"

    def __init__(self, login: str, password: str, course: str, min_sec: int = 3, max_sec: int = 6):
        self.login = login
        self.password = password
        self.course = course
        self.min_sec = min_sec
        self.max_sec = max_sec
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.page_load_strategy = "none"
        # self.driver = webdriver.Chrome(options=options)
        self.driver = webdriver.Chrome()

    @abc.abstractmethod
    def init_course(self):
        ...

    def start_course(self):
        self.driver.get(self.START_URL)
        self._sleep()
        self._click_greetings_button()
        self._click_login_button()
        self.init_course()

    def set_value_input(self, x_path, value):
        input_field = self.driver.find_element(by=By.XPATH, value=x_path)
        input_field.send_keys(value)
        self._sleep()

    def click_button(self, x_path) -> WebElement:
        button = self.driver.find_element(by=By.XPATH, value=x_path)
        button.click()
        self._sleep()
        return button

    @before_execution(logger=logger)
    def _click_greetings_button(self):
        x_path = '//*[@id="root"]/div[1]/div/div/div[1]/button'
        self.click_button(x_path)

    @before_execution(logger=logger)
    def _click_login_button(self):
        self.set_value_input('//*[@id="username"]', self.login)
        self.set_value_input('//*[@id="password"]', self.password)
        self.click_button('//*[@id="submit-btn"]')

    def _sleep(self):
        sleep(randint(self.min_sec, self.max_sec))

    @staticmethod
    def create_link(url: str, params: dict[str, Any]):
        return url + "?" + "&".join([f"{k}={v}" for k, v in params.items()])


class ProtectiveDrivingCourse(BaseClicker):
    COURSE_PARAMS = {
        "mode": "course",
        "doc_id": "6929760816126312392",
        "object_id": "6961398061758971672"
    }

    def init_course(self):
        self.click_rating_protective_driving_button()
        self.click_begin_rating_protective_driving_button()
        self.click_resume_rating_protective_driving_button()
        self.click_start_rating_protective_driving_button()
        self.get_question()

    @before_execution(logger=logger)
    def click_rating_protective_driving_button(self):
        url = self.create_link(self.MAGNUM_URL, self.COURSE_PARAMS)
        self.driver.get(url)
        self._sleep()

    @before_execution(logger=logger)
    def click_begin_rating_protective_driving_button(self):
        x_path = '//*[@id="buttons_area"]/button[1]'
        self.click_button(x_path)

    @before_execution(logger=logger)
    def click_resume_rating_protective_driving_button(self):
        x_path = '//*[@id="buttons_area"]/button'
        self.click_button(x_path)

    @before_execution(logger=logger)
    def click_start_rating_protective_driving_button(self):
        x_path = '//*[@id="buttons_area"]/button[2]'
        self.click_button(x_path)

    @before_execution(logger=logger, total_timeout=10)
    def click_start_rating_protective_driving_button(self):
        self.driver.switch_to.window(self.driver.window_handles[1])
        x_path = '/html/body/div[1]/div[1]/div/div[2]/div[2]/div[1]/ul/li[2]/div[1]'
        self.click_button(x_path)

    @before_execution(logger=logger, total_timeout=5)
    def get_question(self):
        frame_id = "cp_course_container"
        wait = WebDriverWait(self.driver, 10)
        frame = wait.until(EC.frame_to_be_available_and_switch_to_it(frame_id))

        class_name = "wtq-question"
        e = self.driver.find_elements(by=By.CLASS_NAME, value=class_name)
        for question in e:
            if text := question.find_element(by=By.CLASS_NAME, value="wtq-q-question-text").text:
                ic(text)
                items = question.find_elements(by=By.CLASS_NAME, value="wtq-item-table") or []
                for index, item in enumerate(items):
                    t = item.find_element(by=By.CLASS_NAME, value="wtq-item-text-cell-main").text
                    ic(t)

                    # if index == r:
                    # # if t == "Зевота":
                    #     item.click()
                    #     ic("click")
                    #     question.find_element(by=By.CLASS_NAME, value="wtq-btn-text").click()
                    #     break
                    # else:
                    #     ic("asdasdasdasd")
                items[randint(1, 3)].find_element(By.CLASS_NAME, value="wt-radio-spot-outer").click()
                ic("click")
                "wtq-footer-cell-main"
                "/html/body/div[1]/div[2]/div[2]/div[24]/div[4]/table/tbody/tr/td[2]/button[1]"

                if i := question.find_element(by=By.CLASS_NAME, value="wtq-footer-cell-main"):
                    button = i.find_elements(by=By.TAG_NAME, value='button')
                    if button:
                        ic("click next question")
                        button[0].click()
                    else:
                        ic("no next question, button")
                else:
                    ic("no next question, branch")
                    break
                sleep(2)


def main():
    username = "sergievskiy_an"
    password = "QQQQqqqq5555"
    magnum = ProtectiveDrivingCourse(username, password, "sdka;skd;aksd;alksd")
    try:
        magnum.start_course()
    except Exception as ex:
        ic(ex)
        logger.exception(ex)
    finally:
        magnum.driver.quit()


if __name__ == "__main__":
    asyncio.run(asyncio.to_thread(main))
# """/qtiplayer3/presentation.htm?path=/webtutor/test_ATP_zashitnoe_vozhdenie/1/&aicc_sid=7342589899979036765&aicc_url=%2Fhandler%2Ehtml&width=750&height=530&fit=2&lang=ru&send=q&display=item&rubric=none&map=1&navmap=1&navstrict=1&navprog=1&timing=1&nextbind=1&reslock=0&break=0&displayresscore=1&feedback=0&failed=0&displaymax=1"""
# class ="wtq-question" wtq-elem="question" wtq-view="item" data-ident="6961385648709519131" style="visibility: visible; left: 0px;" >
# """
# import asyncio
# import concurrent.futures
# import time
#
# def sync_func(x):
#     time.sleep(1)  # Это блокирующая операция
#     return x * x
#
# async def main():
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         future = executor.submit(sync_func, 2)
#         result = await loop.run_in_executor(None, future.result)
#         print(f"Результат: {result}")
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# """
#
# #
# # @dataclass
# # class Course:
# #     rating_protective_driving_: str = "https://magnum.magnit.ru/view_doc.html?mode=course&doc_id=6929760816126312392&object_id=6961398061758971672"
# #     # "https://magnum.magnit.ru/view_doc.html?mode=course&doc_id=6929760816126312392&object_id=6961398061758971672"
