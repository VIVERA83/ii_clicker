from clicker.backoff import before_execution


class BaseParser:

    async def click_button(self, x_path) -> WebElement:
        button = self.driver.find_element(by=By.XPATH, value=x_path)
        button.click()
        await self.sleep()
        return button
