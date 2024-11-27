class Product:
    def __init__(self, product_id, name, price, manufacturing_time, expiration_from_manufacturing):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.manufacturing_time = manufacturing_time
        self.expiration_from_manufacturing = expiration_from_manufacturing

    def __repr__(self):
        return (f"Product(product_id={self.product_id}, name='{self.name}', price={self.price}, "
                f"manufacturing_time={self.manufacturing_time}, expiration_from_manufacturing={self.expiration_from_manufacturing})")

    # Getters and Setters
    def get_product_id(self):
        return self.product_id

    def set_product_id(self, product_id):
        self.product_id = product_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price

    def get_manufacturing_time(self):
        return self.manufacturing_time

    def set_manufacturing_time(self, manufacturing_time):
        self.manufacturing_time = manufacturing_time

    def get_expiration_from_manufacturing(self):
        return self.expiration_from_manufacturing

    def set_expiration_from_manufacturing(self, expiration_from_manufacturing):
        self.expiration_from_manufacturing = expiration_from_manufacturing