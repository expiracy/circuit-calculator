class Current:
    def __init__(self, id=-1, value=None):
        self.id = id
        self.value = value

    def __str__(self):
        return f"ID: {self.id}, Value: {self.value}"
