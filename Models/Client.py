class Client:
    def __init__(self, client_id, name):
        self.client_id = client_id
        self.name = name

    def __repr__(self):
        return f"Client(client_id={self.client_id}, name='{self.name}')"

    # Getters and Setters
    def get_client_id(self):
        return self.client_id

    def set_client_id(self, client_id):
        self.client_id = client_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name