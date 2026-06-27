import logging

def create_logger(logger_name:str, log_name:str):

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(logger_name)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)


    if not logger.handlers:
        logger.addHandler(file_handler)
    
    return logger    


    
user_logger = create_logger("user", "user.log")
inventory_logger = create_logger("inventory", "inventory.log")
product_logger = create_logger("product", "product.log")
category_logger = create_logger("category", "category.log")
order_logger = create_logger("order", "order.log")
payment_logger = create_logger("payment", "payment.log")
auth_logger = create_logger("auth", "auth.log")

