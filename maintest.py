import lexer
import sys

'''while True:
    text = input()
    result, error = lexer.run(text)

    if error: print(error.as_string())
    else: print(result)'''
#sys.stdin.reconfigure(encoding='utf-8')
f = open('.\LP\_t1.txt')
contents = f.read()
result, error = lexer.run(contents)


for i in range(len(result)):
    print(result[i])

if error: print(error.as_string())


'''text = sys.stdin.read()
result, error = lexer.run(text)

if error: print(error.as_string())
else: print(result)'''