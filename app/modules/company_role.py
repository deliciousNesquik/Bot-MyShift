class CompanyRole:
    def __init__(self):
        self.data: dict = {}

    async def set_role(self, user_id: int = None, user_role: int = None):
        self.data[user_id] = user_role

    async def get_role(self, user_id: int = None):
        return self.data.get(user_id, None)

    async def del_choose(self, user_id: int = None):
        pass


company_role = CompanyRole()
