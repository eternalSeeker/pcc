class FunDecorator:
    def __init__(self):
        self.registry = []

    def __call__(self, m):
        """"This method is called when some method is decorated"""
        self.registry.append(m)  # Add function/method to the registry


generate_outputs = FunDecorator()
