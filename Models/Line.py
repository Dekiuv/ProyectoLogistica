class Line:
    def __init__(self, line_id, product, quantity):
        self.line_id = line_id
        self.product = product
        self.quantity = quantity

    def __repr__(self):
        return f"Line(line_id={self.line_id}, product={self.product}, quantity={self.quantity})"

    # Getters and Setters
    def get_line_id(self):
        return self.line_id

    def set_line_id(self, line_id):
        self.line_id = line_id

    def get_product(self):
        return self.product

    def set_product(self, product):
        self.product = product

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity = quantity