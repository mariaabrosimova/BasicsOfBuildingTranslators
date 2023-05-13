from pythonds.basic.stack import Stack
import sys
flag_unary = False
def is_number(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def reverse_polish_notation(infix):
    with_enter = ''
    fl_shift = True  # операнд
    flag = False
    if infix[0] == '-':
        # flag = True
        fl_shift = False
        # print(len(infix), infix)
        infix = "#" + infix[1:]
        # print(len(infix), infix)
        flag_unary = True

    elif infix[0] == '+':
        infix = infix[1:]
    for i in range(len(infix)):
        if infix[i] != ' ':
            if infix[i] == '.' or flag:
                flag = False
                with_enter += infix[i]
            else:
                # print ("------i", infix[i])
                if infix[i] != '(' and infix[i] != ')':
                    # Проверить что происходит чередование символов
                    if fl_shift:
                        # Надо считать до момент пока не встретили пробел
                        if infix[i].lower() in "abcdefghijklmnopqrstuvwxyz" or is_number(infix[i]):
                            if i != len(infix) - 1:
                                if not is_number(infix[i + 1]) and infix[i + 1] != '.':
                                    fl_shift = False
                        else:
                            raise Exception("Ошибка 1. Некорректный(-ые) операнд(ы)")
                    else:
                        if infix[i] == '+' or infix[i] == '-' or infix[i] == '*' or infix[i] == '/' or infix[
                            i] == '#':  # or infix[i] == '#'
                            fl_shift = True
                        else:
                            raise Exception("Ошибка 2. Некорректный(-ые) оператор(ы) или нет оператора")
                    # if not check_num:
                    # проверим нужно ли добавлять пробел
                    if i != len(infix) - 1 or infix[-1] == ')' or infix[-1] == '(':
                        if (is_number(infix[i + 1]) or infix[i + 1] == '.') and infix[i] != '+' and infix[i] != '*' and \
                                infix[i] != '-' and infix[i] != '/':  # and infix[i] != '#'
                            with_enter += infix[i]
                        else:
                            with_enter += infix[i] + ' '
                    else:
                        with_enter += infix[i] + ' '
                else:
                    with_enter += infix[i] + ' '

    infix = with_enter
    priority_operation = {}
    priority_operation["#"] = 4
    priority_operation["*"] = 3
    priority_operation["/"] = 3
    priority_operation["+"] = 2
    priority_operation["-"] = 2
    priority_operation["("] = 1
    op_stack = Stack()
    postfix_list = []

    token_list = infix.split()
    # print("----token_list", token_list)

    for token in token_list:
        if token.lower() in "abcdefghijklmnopqrstuvwxyz" or is_number(token):
            postfix_list.append(token)
        elif token == '(':
            op_stack.push(token)
        elif token == ')':
            if (not op_stack.isEmpty()):
                top_token = op_stack.pop()
            else:
                raise Exception("Ошибка 3. Лишняя скобка")
            while top_token != '(':
                postfix_list.append(top_token)
                # top_token = op_stack.pop()
                if (not op_stack.isEmpty()):
                    top_token = op_stack.pop()
                else:
                    raise Exception("Ошибка 4. Лишняя скобка")
        else:
            while (not op_stack.isEmpty()) and (priority_operation[op_stack.peek()] >= priority_operation[token]):
                postfix_list.append(op_stack.pop())
            op_stack.push(token)

    while not op_stack.isEmpty():
        postfix_list.append(op_stack.pop())

    if '(' in postfix_list or ')' in postfix_list:
        raise Exception("Ошибка 5. Не хватает открывающей или закрывающей скобки(-ок)")
    return " ".join(postfix_list)


def calculation(operator, operand1, operand2):
    if operator == "#":
        return -operand1
    elif operator == "*":
        return operand1 * operand2
    elif operator == "/":
        return operand1 / operand2
    elif operator == "+":
        return operand1 + operand2
    else:
        return operand1 - operand2


def postfix_calculation(postfix_expr):
    operand_stack = Stack()
    token_list = postfix_expr.split()
    for token in token_list:
        if token.lower() in "abcdefghijklmnopqrstuvwxyz" or is_number(token):
            if token.lower() in "abcdefghijklmnopqrstuvwxyz":
                # работаем с переменными
                num = float(input(token + " = "))
                # print(num, "token.lower() in abcdefghijklmnopqrstuvwxyz")
                operand_stack.push(num)

            else:
                # если работаем с числами
                # print (token, "token")
                operand_stack.push(float(token))
        else:
            if (token == '#'):
                # print ("Унарная операция", token)
                operand2 = 0
                operand1 = operand_stack.pop()
                result = calculation(token, operand1, operand2)
                operand_stack.push(result)
            else:
                # print("Знак операции", token)
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = calculation(token, operand1, operand2)
                operand_stack.push(result)
    # print(operand_stack.pop())
    buf = operand_stack.pop()
    # print(buf)
    return buf


fl = True
while fl:
    try:
        # print("Выражение для 1 варианта: \n", "(r/t/y/u + i*o + p - a + s) + (d - f)*(g + h)*(j + k)")
        # v_1 = reverse_polish_notation("(r/t/y/u + i*o + p - a + s) + (d - f)*(g + h)*(j + k)")
        # print("Постфиксная запись: \n", v_1)
        # res_v1 = postfix_calculation(v_1)
        # print("Вычисление значения для данного выражения: ", res_v1 , "\n")

        infix = input("Введите выражение: ")
        postfix = reverse_polish_notation(infix)
        if not (flag_unary):
            if not postfix and ('+' not in postfix and '-' not in postfix and '*' not in postfix and '/' not in postfix):
                raise Exception ("Ошибка 6. Некорректный ввод")
            print("Постфиксная запись: {}".format(postfix))
        try:
            if not (flag_unary):
                res = postfix_calculation(postfix)
            else:
                res = - postfix_calculation(postfix)
            print("Результат = {}".format(res))
        except ValueError:
            print("Ошибка. Некорректный тип данных, ожидалось число ")
        except ZeroDivisionError:
            print("Ошибка. Попытка деления на 0 ")

    except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])

    print("\n\n")




