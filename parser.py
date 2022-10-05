import ply.yacc as yacc
import sys
from lex import tokens

start_var = ""
terminals = set()
non_terminals = set()
rules_list = []


def p_rule(p):
    "rule : tokens ARROW tokens END"
    p[0] = (p[1], p[3])
    rules_list.append(p[0])


def p_tokens_token(p):
    """ tokens : token
    | tokens token """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1] += [p[2]]
        p[0] = p[1]


def p_token_terminal(p):
    'token : TERMINAL'
    p[0] = p[1]
    terminals.add(p[0])


def p_token_non_terminal(p):
    'token : NON_TERMINAL'
    p[0] = p[1]
    non_terminals.add(p[0])


def p_token_eps(p):
    'token : EPS'
    p[0] = p[1]


def p_token_start(p):
    'token : START'
    global start_var
    start_var = p[1]
    p[0] = p[1]


def p_error(p):
    if p is None:
        print("Unexpected EOF")
    else:
        print(f"Syntax error: Unexpected {p.type}({p.value}) on line {p.lineno}")
    exit(123)


def normal_form():
    norm = True
    for r in rules_list:
        if len(r[0]) > 1 or len(r[1]) > 2:
            norm = False
        if r[0][0] in terminals:
            norm = False
        if r[0][0] == 'e':
            norm = False
        if len(r[1]) == 1:
            if r[1][0] in non_terminals:
                norm = False
        else:
            if r[1][0] in terminals or r[1][1] in terminals:
                norm = False
    return norm


def main():
    parser = yacc.yacc()
    with open(sys.argv[1], "r") as file_open:
        with open(sys.argv[1] + '.out', "w") as file_out:
            for line in file_open.readlines():
                parser.parse(line)
            non_terminals.add(start_var)
            out = "start:" + start_var + '\n'
            out += "terminals: "
            for i in terminals:
                out += i
                out += ' '
            out += "\nnon-terminals: "
            for i in non_terminals:
                out += str(i)
                out += ' '
            out += "\nrules:\n"
            for rule in rules_list:
                for i in rule[0]:
                    out += i
                out += '='
                for j in rule[1]:
                    out += j
                out += '\n'
            if normal_form():
                out += "Normal Form"
            else:
                out += "Not normal formal"
            file_out.write(out)


if __name__ == "__main__":
    main()
