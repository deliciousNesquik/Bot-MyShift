class CompanyChooser:
    def __init__(self):
        self.data: dict = {}

    async def set_choose(self, user_id: int = None, user_choose: int = None):
        self.data[user_id] = user_choose

    async def get_choose(self, user_id: int = None):
        return self.data.get(user_id)

    async def del_choose(self, user_id: int = None):
        pass


company_chooser = CompanyChooser()
