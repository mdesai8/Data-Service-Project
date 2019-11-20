class Authentication():
    def __init__(self, is_logged_in):
        self.is_logged_in = is_logged_in

    def check_auth(self):
        return self.is_logged_in

    def set_auth(self, logged, uid):
        self.is_logged_in = logged
        self.uid = uid
