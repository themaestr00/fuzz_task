import random
import string

args = b'012345678cdehiklnprstvwxyABDGIRS'
meta = b'-\^$(.#*[|<,;{'
mods = ['arg', 'pattern']

def init(seed):
    random.seed(seed)

def deinit():
    pass

def fuzz(buf, add_buf, max_size):
    parse = buf.split(b'\0')
    pattern = parse[-2]
    cur_args = parse[1:-2]
    mod = random.choices(mods, weights=[1, 3], k=1)[0]

    if mod == 'arg':
        commands = ['add', 'rm']
        if cur_args:
            cmd = random.choices(commands, weights=[2, 1], k=1)[0]
        else:
            cmd = 'add'
        if cmd == 'add':
            new = random.choice(args)
            arg = bytearray(b'-')
            arg.append(new)
            if new in b'DIS':
                arg.append(random.choice(string.digits.encode()))
            elif new == b'i':
                arg.append(random.choice(string.printable.encode()))
            cur_args.append(arg)
        else:
            pos = random.randint(0, len(cur_args) - 1)
            cur_args.pop(pos)    
    else:
        commands = ['insert', 'meta', 'replace']
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
    if cur_args:
        return bytearray(b'agrep\0' + b'\0'.join(cur_args) + b'\0' + pattern + b'\0' + parse[-1])
    else:
        return bytearray(b'agrep\0' + pattern + b'\0' + parse[-1])