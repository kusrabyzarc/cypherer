from functools import wraps

def strict_type(func):
    """
    Возвращает декоратор, который запрещает передачу аргументров неверного типа данных

    :param func: Функция декорирования
    :type func: function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Получаем аннотации типов
        annotations = func.__annotations__
        
        # Проверяем позиционные аргументы
        for arg, (param, expected_type) in zip(args, annotations.items()):
            if param == "return":  # Пропускаем аннотацию возврата
                continue
            if not isinstance(arg, expected_type):
                raise TypeError(f"Аргумент '{param}' должен быть {expected_type}, а не {type(arg)}")
        
        # Проверяем именованные аргументы
        for param, arg in kwargs.items():
            if param in annotations:
                expected_type = annotations[param]
                if not isinstance(arg, expected_type):
                    raise TypeError(f"Аргумент '{param}' должен быть {expected_type}, а не {type(arg)}")
        
        return func(*args, **kwargs)
    return wrapper