import ply.lex as lex
import sys

tokens = [
    'TERMINAL',
    'NON_TERMINAL',
    'EPS',
    'START',
    'ARROW',
    'END',
]


def t_NON_TERMINAL(t):
    r'(`((\\|.)*?[^\\])`)|(`(\\)+`)'
    t.value = t.value[1:-1].replace("\`", "`")
    return t


def t_TERMINAL(t):
    r'("((\\|.)*?[^\\])")|("(\\)+")'
    t.value = t.value[1:-1].replace('\\"', '"')
    return t


def t_START(t):
    r'(<((\\|.)*?[^\\])>)|(<(\\)+>)'
    t.value = t.value[1:-1].replace("\<", "<").replace("\>", ">")
    return t


t_EPS = r'e'
t_ARROW = r'='
t_END = r','
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def main():
    lexer = lex.lex()
    filename = sys.argv[1]
    with open(filename, "r") as file_open:
        with open(filename + ".out", "w") as file_out:
            lexer.input("".join(file_open.readlines()))
            while True:
                tok = lexer.token()
                if not tok:
                    break
                file_out.write(str(tok))
                file_out.write('\n')


if __name__ == "__main__":
    main()
