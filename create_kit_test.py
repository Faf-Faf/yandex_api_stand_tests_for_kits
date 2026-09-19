import sender_stand_request
import data
import copy 

# Функция для изменения значения в параметре kit_body в теле запроса 
def get_kit_body(kit_name):
    # Копируется словарь с телом запроса из файла data
    current_body = copy.deepcopy(data.kit_body)
    # Изменение значения в поле name
    current_body["name"] = kit_name
    # Возвращается новый словарь с нужным значением kit_body
    return current_body

def create_user_and_get_token():
    # создаём пользователя, чтобы получить токен для набора
    user_response = sender_stand_request.post_new_user(data.user_body)
    return user_response.json()["authToken"]

def positive_assert(kit_name):
    #Формируем тело запроса
    kit_body = get_kit_body(kit_name)
    auth_token = create_user_and_get_token()

    #Создаём набор
    kit_response = sender_stand_request.post_new_kit(kit_body, auth_token)
    #Проверяем код ответа именно на запрос создания набора
    #Мы проверяем, что набор создался прежде чем проверять, что он появился в списке наборов
    assert kit_response.status_code == 201

    #Сохраняем тело ответа один раз
    created_kit = kit_response.json()
    assert created_kit["id"] != ""
    assert created_kit["name"] == kit_name

# Функция негативной проверки, когда в ответе ошибка про символы
def negative_assert_symbol(kit_name):
    # В переменную kit_body сохраняется обновлённое тело запроса
    kit_body = get_kit_body(kit_name)
    auth_token = create_user_and_get_token()

    # В переменную response сохраняется результат 
    response = sender_stand_request.post_new_kit(kit_body, auth_token)

    # Проверяется, что код ответа равен 400
    assert response.status_code == 400

    # Проверяется, что в теле ответа атрибут "code" равен 400
    assert response.json()["code"] == 400

# Функция для негативной проверки, когда в ответе ошибка: "Не все необходимые параметры были переданы"
def negative_assert_no_name(kit_body):
    auth_token = create_user_and_get_token()

    # В переменную response сохраняется результат 
    response = sender_stand_request.post_new_kit(kit_body, auth_token)

    # Проверяется, что код ответа равен 400
    assert response.status_code == 400

    # Проверяется, что в теле ответа атрибут "code" равен 400
    assert response.json()["code"] == 400
    # Проверяется текст в теле ответа в атрибуте "message"
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

# Тест 13. Успешное создание набора. Параметр name состоит из 1 символа
def test_create_kit_1_letter_in_name_get_success_response():
    positive_assert("a")

# Тест 14. Успешное создание набора. Параметр name состоит из 511 символов
def test_create_kit_511_letter_in_name_get_success_response():
    positive_assert("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
    "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdab" \
    "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
    "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")

# Тест 15. Ошибка. Параметр name состоит из 512 символов
def test_create_kit_512_letter_in_name_get_error_response():
    negative_assert_symbol("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc" \
    "dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdab" \
    "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcda" \
    "bcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" \
    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")

# Тест 16. Успешное создание набора. Параметр name состоит из английских букв
def test_create_kit_english_letter_in_name_get_success_response():
    positive_assert("QWErty")

# Тест 17. Успешное создание набора. Параметр name состоит из русских букв
def test_create_kit_russian_letter_in_name_get_success_response():
    positive_assert("Мария")

# Тест 18. Успешное создание набора. Параметр name состоит из строки спецсимволов
def test_create_kit_has_special_symbol_in_name_get_success_response():
    positive_assert("\"№%@\",")

# Тест 19. Успешное создание набора. Параметр name состоит из слов с пробелами
def test_create_kit_has_space_in_name_get_success_response():
    positive_assert("Человек и КО")

# Тест 20. Успешное создание набора. Параметр name состоит из строки цифр
def test_create_kit_has_number_in_name_get_success_response():
    positive_assert("123")

# Тест 21. Ошибка. В запросе нет параметра name
def test_create_kit_no_name_get_error_response():
    # Копируется словарь с телом запроса из файла data в переменную kit_body
    kit_body = copy.deepcopy(data.kit_body)
    # Удаление параметра name из запроса
    kit_body.pop("name")
    # Проверка полученного ответа
    negative_assert_no_name(kit_body)

# Тест 22. Ошибка. Параметр состоит из пустой строки
def test_create_kit_empty_name_get_error_response():
    # В переменную kit_body сохраняется обновлённое тело запроса
    kit_body = get_kit_body("")
    # Проверка полученного ответа
    negative_assert_no_name(kit_body)

# Тест 23. Ошибка. Тип параметра name: число
def test_create_kit_number_type_name_get_error_response():
    # В переменную kit_body сохраняется обновлённое тело запроса
    kit_body = get_kit_body(12)
    auth_token = create_user_and_get_token()

    # В переменную kit_response сохраняется результат запроса на создание набора:
    response = sender_stand_request.post_new_kit(kit_body, auth_token)

    # Проверка кода ответа
    assert response.status_code == 400