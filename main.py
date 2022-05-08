import lexer
import sys

#sys.stdin.reconfigure(encoding='utf-8')
text = sys.stdin.read()

result, error = lexer.run(text)

for i in range(len(result)):
    print(result[i])
if error: print(error.as_string())
