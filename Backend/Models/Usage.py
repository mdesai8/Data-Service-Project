class Usage():
    def __init__(self, api_calls):
        self.api_calls = api_calls

    def get_usage(self):
        calls = self.api_calls
        return calls

    def inc_usage(self):
        self.api_calls += 1
