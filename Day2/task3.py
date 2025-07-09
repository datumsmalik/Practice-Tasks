import logging


logging.basicConfig(
    filename='app.log',   
    level=logging.INFO,

    format='%(asctime)s - %(levelname)s - %(message)s'
)

def divide(a, b):
    try:
        result = a / b
        logging.info(f"Division successful: {a} / {b} = {result}")
        return result


    except ZeroDivisionError:
        logging.error("Tried to divide by zero!")
        return None


    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None



print(divide(10, 2))  


print(divide(5, 0))   

print(divide(8, 'BBBBB')) 
