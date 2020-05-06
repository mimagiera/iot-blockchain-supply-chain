from enum import Enum

ID = 0


class ProductType(Enum):
    BRICK = 1
    CONCRETE_MIXER = 2
    CRANE = 3


class ProductDescription:
    def __init__(self, type_of_product, product_schema: str, number_of_parts_to_produce: int):
        self.type_of_product = type_of_product
        self.product_schema = product_schema
        self.number_of_parts_to_produce = number_of_parts_to_produce


class OrderDescription:
    def __init__(self, product_descriptions, transaction_date, current_factory_id: str,
                 destination_factory_id: str):
        self.id = self.generate_id()
        self.product_descriptions = product_descriptions
        self.transaction_date = transaction_date
        self.current_factory_id = current_factory_id
        self.destination_factory_id = destination_factory_id

    @staticmethod
    def generate_id():
        global ID
        ID = ID + 1
        return ID
