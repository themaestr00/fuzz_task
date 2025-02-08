import random

commands = ['insert', 'meta', 'meta_strct', 'flood', 'replace']
meta = b'-\^$.#*,;([{<'
strcts = [b'\z', b'(a)*', b'a(a)*', b'[b-dq-tz]', b'[^b-diq-tz]', b'ab|cd', b'<abcd>', b'cat,dog', b'cat;dog', b'\\']

def get_weights(len):
    if len == 0:
        return [2, 3, 3, 1, 0]
    elif len > 10000:
        return [2, 4, 4, 1, 1]
    else:
        return [3, 4, 4, 1, 2]

def init(seed):
    random.seed(seed)

def deinit():
    pass

def fuzz(buf, add_buf, max_size):
    pattern = buf
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
            case 'flood':
                pattern += random.randint(0, 255).to_bytes() * random.randint(30000, 90000)
    return pattern[:max_size]