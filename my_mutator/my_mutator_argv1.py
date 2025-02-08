import random
import string

args = b'012345678cdehiklnprstvwxyABDGIRS'
meta = b'-\^$.#*,;([{<'
mods = ['arg', 'pattern']
strcts = [b'\z', b'(a)*', b'a(a)*', b'[b-dq-tz]', b'[^b-diq-tz]', b'ab|cd', b'<abcd>', b'cat,dog', b'cat;dog', b'\\']
syms = string.ascii_letters + string.digits + string.punctuation
syms = syms.encode()


def get_weights(len):
    if len == 0:
        return [2, 3, 3, 0]
    elif len > 10000:
        return [2, 4, 4, 1]
    else:
        return [3, 4, 4, 2]

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
        commands = ['insert', 'meta', 'meta_strct', 'replace']
        global strcts
        for _ in range(random.randint(1, 5)):
            cmd = random.choices(commands, weights=get_weights(len(pattern)), k=1)[0]
            match(cmd):
                case 'insert':
                    for _ in range(random.randint(1, 10)):
                        new = random.randint(0, 255)
                        pos = random.randint(0, len(pattern))
                    pattern.insert(pos, new)
                case 'meta':
                    for _ in range(random.randint(1, 3)):
                        new = random.choice(meta)
                        pos = random.randint(0, len(pattern))
                        pattern.insert(pos, new)
                        if new in b'[(<{':
                            new_pos = random.randint(pos + 1, len(pattern))
                            if new == b'['[0]:
                                new = b']'[0]
                            elif new == b'('[0]:
                                new = b')'[0]
                            elif new == b'<'[0]:
                                new = b'>'[0]
                            else:
                                new = b'}'[0]
                            pattern.insert(new_pos, new)
                            acts = ['bracket', 'meta', 'none']
                            act = random.choice(acts)
                            if act == 'bracket':
                                new = random.choice(b'[(<{')
                                left = random.randint(pos, new_pos)
                                right = random.randint(left, new_pos)
                                pattern.insert(left, new)
                                if new == b'['[0]:
                                    new = b']'[0]
                                elif new == b'('[0]:
                                    new = b')'[0]
                                elif new == b'<'[0]:
                                    new = b'>'[0]
                                else:
                                    new = b'}'[0]
                                pattern.insert(right, new)
                            elif act == 'meta':
                                new = random.choice(meta)
                                pos = random.randint(pos, new_pos)
                                pattern.insert(pos, new)
                case 'meta_strct':
                    for _ in range(random.randint(1, 3)):
                        pos = random.randint(0, len(pattern))
                        new = random.choice(strcts)
                        if len(strcts) > 5000:
                            strcts = strcts[:30]
                        if any(b not in meta for b in new):
                            new = new.replace(random.choice([b for b in new if b not in meta]).to_bytes(), random.randint(0, 255).to_bytes())
                        else:
                            new = new.replace(random.choice(new).to_bytes(), random.randint(0, 255).to_bytes())
                        pattern = pattern[:pos] + new + pattern[pos:]
                case 'replace': 
                    for _ in range(random.randint(1, 10)):
                        pos = random.randint(0, len(pattern) - 1)
                        pattern[pos] = random.randint(0, 255)
    if cur_args:
        return bytearray(b'agrep\0' + b'\0'.join(cur_args) + b'\0' + pattern + b'\0' + parse[-1])
    else:
        return bytearray(b'agrep\0' + pattern + b'\0' + parse[-1])