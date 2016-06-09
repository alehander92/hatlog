class Env:
    def __init__(self, values=None, parent=None):
        self.values = values or {}
        self.parent = parent

    def __getitem__(self, label):
        current = self
        while current is not None:
            if label in current.values:
                return current.values[label]
            current = current.parent

    def __setitem__(self, label, value):
        self.values[label] = value

