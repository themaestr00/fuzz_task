import random
import string

def init(seed):
    random.seed(seed)

def deinit():
    pass

def fuzz(buf, add_buf, max_size):
    args = b'012345678cdehiklnprstvwxyABDGIRS'
    arg, pattern = buf.split(b' ')
    mods = ['arg', 'pattern']
    mod = random.choice(mods)

    if mod == 'arg':
        new = random.choice(args)
        arg = bytearray(b'-')
        arg.append(new)
        if new in b'DIS':
            arg.append(random.choice(b'0123456789'))
        elif new == b'i':
            arg.append(random.choice(b'abcdefghijklmnopqrsuvwxyz0123456789'))
    else:
        commands = ['insert', 'meta', 'replace']
        meta = b'-\^$(.#*[|<,;)]>'
        syms = string.ascii_letters + string.digits + string.punctuation
        syms = syms.encode()
        cmd = random.choice(commands)
        match(cmd):
            case 'insert':
                new = random.choice(syms)
                pos = random.randint(0, len(pattern))
                pattern.insert(pos, new)
            case 'meta':
                new = random.choice(meta)
                pos = random.randint(0, len(pattern))
                pattern.insert(pos, new)
            case 'replace':
                pos = random.randint(0, len(pattern) - 1)
                pattern[pos] = random.choice(syms)
    arg.extend(b' ')
    print(arg + pattern)
    return arg + pattern
