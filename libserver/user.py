class User:

    def __init__(self, address):
        self.address = address
        self.name = None
    
    def set_name(self, name: str):
        """Sets a user's name"""
        self.name = name
        
