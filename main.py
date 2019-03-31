import decimal

PRIORITY = [['*', '/'], ['+', '-']]

print_internals = True

def tokenize(raw):
    raw = raw.replace(" ", "")

    tokens = []
    previous_is_digit = None
    for symbol in raw:
        current_is_digit = symbol.isdigit()

        if previous_is_digit != current_is_digit:
            tokens.append([])
        
        tokens[-1].append(symbol)
        
        previous_is_digit = current_is_digit
    
    tokens = ["".join(token) for token in tokens]
    return tokens

def prioritize(tree, index):
    return tree[:(index - 1)] + [tree[(index - 1):(index + 2)]] + tree[(index + 2):]

def is_operator(token):
    for group in PRIORITY:
        if token in group:
            return True
    
    return False

def get_op_index(op):
    for i, x in enumerate(PRIORITY):
        if op in x:
            return i

def treeify(tokens):
    tree = tokens
    # [1, '+', 3, '*', 5, '-', 123, '/', 7, '/', 7]
    # [1, '+', [3, '*', 5], '-', 123, '/', 7, '/', 7]
    # [[1, '+', [3, '*', 5]], '-', 123, '/', 7, '/', 7]
    # [[1, '+', [3, '*', 5]], '-', [123, '/', 7], '/', 7]
    # [[1, '+', [3, '*', 5]], '-', [[123, '/', 7], '/', 7]]

    i = 2
    while True:
        if len(tree) == 3:
            break

        if not is_operator(tree[i]):
            left = tree[i - 1]
            right = tree[i + 1]

            li = get_op_index(left)
            ri = get_op_index(right)
            
            tree = prioritize(tree, i + (1 if ri < li else -1))

    return tree

def evaluate(tree):
    left = tree[0]
    right = tree[2]
    op = tree[1]
    
    left = evaluate(left) if isinstance(left, list) else decimal.Decimal(left)
    right = evaluate(right) if isinstance(right, list) else decimal.Decimal(right)
    
    if op == '*':
        return left * right
    elif op == '/':
        return left / right
    elif op == '+':
        return left + right
    elif op == '-':
        return left - right
    
    raise Exception('Unknown operator')

def ep(x):
    print(repr(x))

def calc(raw):
    tokens = tokenize(raw)
    tree = treeify(tokens)
    evaluation = evaluate(tree)
    
    if print_internals:
        ep(raw)
        ep(tokens)
        ep(tree)
    
    return evaluation

def main():
    while True:
        raw = input()
        if raw == 'q':
            break
        print(calc(raw))

main()