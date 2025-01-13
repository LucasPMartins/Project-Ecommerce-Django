import re

def check_cpf(input_cpf:str) -> bool:
    cpf = re.sub(
        r'[^0-9]',
        '',
        input_cpf
    )

    nine_digits = cpf[:9]
    count = 10

    result_d1 = 0
    for digit in nine_digits:
        result_d1 += int(digit) * count
        count -= 1
    digit_1 = (result_d1 * 10) % 11
    digit_1 = digit_1 if digit_1 <= 9 else 0

    ten_digits = nine_digits + str(digit_1)
    count = 11

    result_d2 = 0
    for digit in ten_digits:
        result_d2 += int(digit) * count
        count -= 1
    digit_2 = (result_d2 * 10) % 11
    digit_2 = digit_2 if digit_2 <= 9 else 0

    new_cpf = f'{nine_digits}{digit_1}{digit_2}'

    if cpf == new_cpf:
        return True
    
    return False