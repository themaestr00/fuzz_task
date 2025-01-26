import random
import string

def init(seed):
    random.seed(seed)

def deinit():
    pass

def fuzz(buf, add_buf, max_size):
    pattern = buf
    commands = ['insert', 'meta', 'replace']
    meta = b'-\^$(.#*[|<,;'
    syms = string.ascii_letters + string.digits + string.punctuation
    syms = syms.encode()
    if len(pattern) > 0:
        cmd = random.choice(commands)
    else:
        cmd = random.choice(commands[:2])
    match(cmd):
        case 'insert':
            new = random.choice(syms)
            pos = random.randint(0, len(pattern))
            pattern.insert(pos, new)
        case 'meta':
            new = random.choice(meta)
            pos = random.randint(0, len(pattern))
            pattern.insert(pos, new)
            if new in b'[(<':
                pos = random.randint(pos + 1, len(pattern))
                if new == b'['[0]:
                    new = b']'[0]
                elif new == b'('[0]:
                    new = b')'[0]
                else:
                    new = b'>'[0]
                pattern.insert(pos, new)
        case 'replace':
            pos = random.randint(0, len(pattern) - 1)
            pattern[pos] = random.choice(syms)
    return pattern
