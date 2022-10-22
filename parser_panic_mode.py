import ply.yacc as yacc
import sys
from lex import tokens

start_var = ""

file = ''
help_file = ''
file_out = ''
current_line = 1


def change_line_in_help_file(num, new_line):
    a_file = open(help_file, "r")
    list_of_lines = a_file.readlines()
    if num == len(list_of_lines) - 1:
        list_of_lines[num] = new_line
    else:
        list_of_lines[num] = new_line + '\n'
    a_file = open(help_file, "w")
    a_file.writelines(list_of_lines)
    a_file.close()


def p_rule(p):
    """rule : NON_TERMINAL ARROW tokens END
    | START ARROW tokens END"""
    p[0] = (p[1], p[3])


def p_tokens_token(p):
    """ tokens : token
    | tokens token """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1] += [p[2]]
        p[0] = p[1]


def p_token_non_terminal(p):
    """token : NON_TERMINAL"""
    p[0] = p[1]


def p_token_terminal(p):
    """token : TERMINAL"""
    p[0] = p[1]


def p_token_eps(p):
    """token : EPS"""
    p[0] = p[1]


def p_token_start(p):
    """token : START"""
    global start_var
    start_var = p[1]
    p[0] = p[1]


def p_error(p):
    f = open(file_out, "a")

    if p is None:
        f.write("Unexpected EOF" + '\n')
    else:
        f.write(f"Unexpected {p.type}({p.value}) :{p.lineno}" + '\n')
    f.close()
    exit(123)


def p_error_without_end(p):
    """rule : NON_TERMINAL ARROW tokens
    | START ARROW tokens"""
    f = open(file_out, "a")
    f.write(f"Expected `,` :" + str(current_line) + '\n')
    f.close()
    correct_line = ''
    correct_line += '`' + p[1] + '`'
    correct_line += ' ' + p[2] + ' '
    for el in p[3]:
        correct_line += '"' + el + '"'
    correct_line += ','
    change_line_in_help_file(current_line - 1, correct_line)


def p_error_not_non_terminal(p):
    """rule : tokens ARROW tokens END"""
    f = open(file_out, "a")
    f.write(f"You should use one non_terminal before arrow :" + str(current_line) + '\n')
    f.close()
    correct_line = ''
    correct_line += '`E`'
    correct_line += ' ' + p[2] + ' '
    for el in p[3]:
        correct_line += '"' + el + '"'
    correct_line += ','
    change_line_in_help_file(current_line - 1, correct_line)


def p_error_not_non_terminal_end(p):
    """rule : tokens ARROW tokens"""
    f = open(file_out, "a")
    f.write(f"You should use one non_terminal before arrow :" + str(current_line) + '\n')
    f.close()
    correct_line = ''
    correct_line += '`E`'
    correct_line += ' ' + p[2] + ' '
    for el in p[3]:
        correct_line += '"' + el + '"'
    change_line_in_help_file(current_line - 1, correct_line)



def p_error_without_rule(p):
    """ rule :
    | tokens
    | tokens END
    | tokens ARROW END
    | tokens ARROW
    | ARROW tokens END
    | ARROW tokens
    | NON_TERMINAL ARROW
    | START ARROW
    | END
    | ARROW
    """
    f = open(file_out, "a")
    f.write(f"Expected rule :" + str(current_line) + '\n')
    f.close()
    correct_line = '`E` = "e",'
    change_line_in_help_file(current_line - 1, correct_line)


parser = yacc.yacc()


def definition_help_file(f):
    global help_file
    help_file = f + "file.help"
    with open(file, 'r') as fr, open(help_file, 'w') as fw:
        for line in fr:
            fw.write(line)


def main():
    # первым аргументом -- какую грамматику рассматриваем,
    # вторым -- директория, куда сохранить вспомогательный файл для анализа

    global file
    file = sys.argv[1]
    global file_out
    file_out = sys.argv[1] + '.out'

    definition_help_file(sys.argv[2])

    f = open(help_file, "r")

    f_out = open(file_out, 'w').close()

    global current_line
    for line in f.readlines():
        a_file = open(help_file, "r")
        list_of_lines = a_file.readlines()
        new_line = list_of_lines[current_line - 1]
        i = parser.parse(new_line)
        while i is None:
            a_file = open(help_file, "r")
            list_of_lines = a_file.readlines()
            new_line = list_of_lines[current_line - 1]
            i = parser.parse(new_line)
        current_line += 1


if __name__ == "__main__":
    main()
