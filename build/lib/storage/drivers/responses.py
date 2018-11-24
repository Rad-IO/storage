class FailResponse:
    def __init__(self, reason):
        self.reason = reason


class SuccessResponse:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            super(SuccessResponse, self).__setattr__(k, v)
