from enum import Enum


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
    def __init__(self, product_descriptions, transaction_date, last_factory_id: str,
                 current_factory_id=None):
        self.id = "generated id"
        self.product_descriptions = product_descriptions
        self.transaction_date = transaction_date
        self.last_factory_id = last_factory_id
        self.current_factory_id = current_factory_id
