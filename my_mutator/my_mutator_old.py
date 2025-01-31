import random
import string

commands = ['insert', 'meta', 'replace']
meta = b'-\^$(.#*[|<,;{'
#syms = string.printable
#syms = syms.encode()

def init(seed):
    random.seed(seed)

def deinit():
    pass

def fuzz(buf, add_buf, max_size):
    pattern = buf
    if pattern:
        cmd = random.choices(commands, weights=[2, 3, 1], k=1)[0]
    else:
        cmd = random.choices(commands[:2], weights=[2, 3], k=1)[0]
    match(cmd):
        case 'insert':
            new = random.randint(0, 255).to_bytes() * random.randint(1, 20)
            pos = random.randint(0, len(pattern))
            pattern = pattern[:pos] + new + pattern[pos:]
        case 'meta':
            new = random.choice(meta)
            pos = random.randint(0, len(pattern))
            pattern.insert(pos, new)
            if new in b'[(<{':
                pos = random.randint(pos + 1, len(pattern))
                if new == b'['[0]:
                    new = b']'[0]
                elif new == b'('[0]:
                    new = b')'[0]
                elif new == b'<'[0]:
                    new = b'>'[0]
                else:
                    new = b'}'[0]
                pattern.insert(pos, new)
        case 'replace':
            pos = random.randint(0, len(pattern) - 1)
            pattern = pattern.replace(pattern[pos].to_bytes(), random.randint(0, 255).to_bytes())
    return pattern[:max_size]