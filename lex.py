import ply.lex as lex
import sys

tokens = [
  'TERMINAL',
  'NON_TERMINAL',
  'EPS',
  'START',
  'ARROW',
  'END',
  'OR'
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

t_EPS = r'ε'
t_ARROW = r'→'
t_END = r','
t_OR = r'\|'
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

  with open(sys.argv[1], "r") as file_open:
    with open(sys.argv[1] + ".out", "w") as file_out:
      #print(file_open)
      for line in file_open.readlines():
        lexer.input(line)
        while True:
          tok = lexer.token()
          if not tok:
            break
          file_out.write(str(tok))
          file_out.write('\n')

if __name__ == "__main__":
    main()