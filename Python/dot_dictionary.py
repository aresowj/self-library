class DotDictionary(dict):
    """A dictionary that can user dot operator to
    access the member attributes
    """
    def __init__(self, d):
        super(DotDictionary, self).__init__()
        self.__dict__ = d

    def __getattr__(self, item):
        return self.get(item)
