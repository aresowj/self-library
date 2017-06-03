import random
import string
import os

from subprocess import Popen, PIPE, STDOUT, check_call, run


operations = ['add', 'check', 'del', 'find']


def next_operation():
    return operations[random.randint(0, len(operations)-1)]


def random_string():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(3, 20)))


def generate_inputs():
    inputs = []
    buckets = random.randint(5, 10)
    lines = random.randint(3, 10)
    inputs.append(str(buckets))
    inputs.append(str(lines))
    stored = []

    for i in range(lines):
        next_opt = next_operation()
        if next_opt in {'add', 'find'}:
            next_opt += ' %s' % random_string()
        elif next_opt == 'check':
            next_opt += ' %s' % str(random.randint(0, buckets-1))
        elif next_opt == 'del':
            if random.randint(0,10) > 5:
                # Del stored
                if stored:
                    next_opt += ' %s' % stored.pop(random.randint(0, len(stored)-1))
                else:
                    next_opt = 'add %s' % random_string()
            else:
                next_opt += ' %s' % random_string()
                
        inputs.append(next_opt)

    return inputs

def get_results(file_name, inputs):
    read, write = os.pipe()
    os.write(write, '\n'.join(inputs).encode())
    os.close(write)
    out = run(['python', file_name], stdin=read, stdout=PIPE)

    return out.stdout

if __name__ == '__main__':
    count = 0
    
    while count <= 50:
        inputs = generate_inputs()
        result1 = get_results(r'C:\Users\kagami\Desktop\Data_Structures\Programming-Assignment-3-My-Solution\hash_chains_naive.py', inputs)
        result2 = get_results(r'C:\Users\kagami\Desktop\Data_Structures\Programming-Assignment-3-My-Solution\hash_chains.py', inputs)

        if result1 != result2:
            print('\n'.join(inputs))
            print("=============")
            print(result1)
            print("=============")
            print(result2)


        count += 1
