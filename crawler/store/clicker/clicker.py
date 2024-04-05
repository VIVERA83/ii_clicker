import asyncio
from logging import Logger, getLogger
from random import randint

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from store.clicker.backoff import before_execution
from store.clicker.courses import TrainingCourse


class CourseClicker:
    START_URL = "https://tvoy.magnit.ru/"
    MAGNUM_URL = "https://magnum.magnit.ru/view_doc.html"

    def __init__(
        self,
        login: str,
        password: str,
        training_course: TrainingCourse,
        min_sec: int = 3,
        max_sec: int = 6,
        min_sec_answer: int = 15,
        max_sec_answer: int = 20,
        logger: Logger = None,
    ):
        self.loger = logger or getLogger(name=__name__)
        self.login = login
        self.password = password
        self.training_course = training_course
        self.min_sec = min_sec
        self.max_sec = max_sec
        self.min_sec_answer = min_sec_answer
        self.max_sec_answer = max_sec_answer
        self.timeout = 10
        self.questions = {}
        self.driver = webdriver.Chrome(options=self.get_driver_options())

    @staticmethod
    def get_driver_options() -> Options:
        options = webdriver.ChromeOptions()
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--headless=new")
        # options.add_argument("--start-maximized")
        # options.add_argument("--ignore-certificate-errors")
        # options.add_argument("--allow-running-insecure-content")
        user_agent = UserAgent(browsers=["chrome"]).getRandom.get("useragent")
        options.add_argument(f"user-agent={user_agent}")
        return options

    async def start_course(self):
        self.driver.get(self.START_URL)
        await self.sleep()
        await self._click_greetings_button()
        await self._click_login_button()
        await self.init_course()

    async def set_value_input(self, x_path, value):
        input_field = self.driver.find_element(by=By.XPATH, value=x_path)
        input_field.send_keys(value)
        await self.sleep()

    async def click_button(self, x_path) -> WebElement:
        button = self.driver.find_element(by=By.XPATH, value=x_path)
        button.click()
        await self.sleep()
        return button

    @before_execution()
    async def _click_greetings_button(self):
        x_path = '//*[@id="root"]/div[1]/div/div/div[1]/button'
        await self.click_button(x_path)
        self.loger.info("Начальная страница пройдена")

    # @before_execution()
    async def _click_login_button(self):
        await self.set_value_input('//*[@id="username"]', self.login)
        await self.set_value_input('//*[@id="password"]', self.password)
        await self.click_button('//*[@id="submit-btn"]')
        self.loger.info("Авторизация пройдена")

    async def sleep(self, min_sec: int = None, max_sec: int = None):
        min_sec = min_sec or self.min_sec
        max_sec = max_sec or self.max_sec
        await asyncio.sleep(randint(min_sec, max_sec))

    def create_link(self):
        return (
            self.MAGNUM_URL
            + "?"
            + "&".join(
                [f"{k}={v}" for k, v in self.training_course.get_params().items()]
            )
        )

    async def init_course(self):
        self.questions = self.training_course.get_questions()
        await self.go_to_course()
        await self.click_start_course_button()
        await self.click_resume_course_button()
        await self.click_start_test()
        await self.execute_course()

    @before_execution()
    async def go_to_course(self):
        url = self.create_link()
        self.driver.get(url)
        await self.sleep()

    @before_execution()
    async def click_start_course_button(self):
        x_path = '//*[@id="buttons_area"]/button[1]'
        await self.click_button(x_path)

    @before_execution()
    async def click_resume_course_button(self):
        x_path = '//*[@id="buttons_area"]/button'
        await self.click_button(x_path)

    @before_execution(total_timeout=10)
    async def click_start_test(self):
        self.driver.switch_to.window(self.driver.window_handles[1])
        cpx_block_structure = self.driver.find_elements(
            by=By.CLASS_NAME, value="cpx-block-structure"
        )[0]
        cpx_module_name = cpx_block_structure.find_elements(
            by=By.CLASS_NAME, value="cpx-module-name"
        )[-1]
        cpx_module_name.click()
        await self.sleep()

    @before_execution(total_timeout=5)
    async def execute_course(self):
        self.loger.info("Начат курс")
        frame_id = "cp_course_container"
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(ec.frame_to_be_available_and_switch_to_it(frame_id))

        question_elements = self.__get_question_elements()
        await self.__answer_questions(question_elements)
        self.driver.close()
        await self.sleep()
        self.__close_course()
        self.loger.info("Курс пройден")

    def __close_course(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        element = self.driver.find_element(By.ID, "buttons_area")
        element.find_element(By.TAG_NAME, "button").click()

    def __get_question_elements(self) -> list[WebElement]:
        class_name = "wtq-question"
        question_elements = self.driver.find_elements(
            by=By.CLASS_NAME, value=class_name
        )
        return question_elements

    async def __answer_questions(self, question_elements: list[WebElement]):
        for index, question in enumerate(question_elements):
            if question_text := self._get_text_from_element(
                question, "wtq-q-question-text"
            ):
                self.loger.info(f"question {index}: {question_text}")
                await self.sleep(self.min_sec_answer, self.max_sec_answer)

                if correct_answer := self.questions.get(question_text):
                    self.__select_answer(correct_answer, question)
                else:
                    self.__select_random_answer(question)
                self.__click_next_question(question)

    def __click_next_question(self, question):
        try:
            if button_element := self._get_web_elements(
                question, value="wtq-footer-cell-main"
            ):
                if button := self._get_web_elements(
                    button_element[0], "button", By.TAG_NAME
                )[0]:
                    button.click()
        except Exception as e:
            self.loger.error(f"__click_next_question {e}")

    def __select_answer(self, correct_answer, question):
        answer_elements = self._get_web_elements(question, "wtq-item-table")
        for answer in answer_elements:
            answer_text = self._get_text_from_element(answer, "wtq-item-text-cell-main")
            if answer_text == correct_answer:
                self._get_web_elements(answer, "wt-radio-spot-outer")[0].click()
                self.loger.info(f"correct answer: {answer_text}")
                return
        self.__select_random_answer(question)

    def __select_random_answer(self, question: WebElement):
        answer_elements = self._get_web_elements(question, "wtq-item-table")
        count = len(answer_elements) - 1
        self._get_web_elements(
            answer_elements[randint(0, count)], "wt-radio-spot-outer"
        )[0].click()
        self.loger.info(f"random answer")

        # TODO: delete this code after fix api
        for el in answer_elements:
            text = self._get_text_from_element(el, "wtq-item-text-cell-main")
            print(text)
        # TODO stop

    @staticmethod
    def _get_text_from_element(element: WebElement, class_name: str) -> str:
        return element.find_element(by=By.CLASS_NAME, value=class_name).text

    @staticmethod
    def _get_web_elements(
        element: WebElement, value: str, by: str = By.CLASS_NAME
    ) -> list[WebElement]:
        element = element.find_elements(by=by, value=value)
        return element or []
