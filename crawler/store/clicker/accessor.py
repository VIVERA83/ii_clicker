from base.base_accessor import BaseAccessor


class ClickerAccessor(BaseAccessor):
    cources = {}

    async def start_protective_driving_course(self):

        self.logger.info("Start protective driving course")
