
def lzw_decompress(compressed: bytes) -> bytes:
    maxDictEntries = 3532
    compressed_bits = len(compressed) * 8
    decompressed = []
    dictionary = {i: (i, 0) for i in range(256)}
    stack = []
    old_code, bits_read = _lzw_get_code(compressed, 0)
    decompressed.append(old_code)
    character = old_code
    while bits_read + 12 <= compressed_bits:
        new_code, bits_read = _lzw_get_code(compressed, bits_read)
        if new_code in dictionary:
            _lzw_get_string(new_code, dictionary, stack)
        else:
            stack.append(character)
            _lzw_get_string(old_code, dictionary, stack)
        character = stack[-1]
        while stack:
            decompressed.append(stack.pop())

        newpos = _lzw_get_new_hash_code(character, old_code, dictionary)
        dictionary[newpos] = (character, old_code)
        if len(dictionary) > maxDictEntries:
            dictionary = {i: (i, 0) for i in range(256)}
            if bits_read + 12 <= compressed_bits:
                new_code, bits_read = _lzw_get_code(compressed, bits_read)
                decompressed.append(new_code)
                character = new_code
            else:
                break
        old_code = new_code

    return decompressed

def _lzw_get_code(bytes, bits_read):
    index, r = divmod(bits_read, 8)
    code = (bytes[index] << 8) + bytes[index + 1]
    code = code >> 4 - r & 4095
    bits_read += 12
    return (code, bits_read)


def _lzw_get_string(code, dictionary, stack):
    current_code = code
    while current_code > 255:
        root, current_code = dictionary[current_code]
        stack.append(root)

    stack.append(current_code)


def _lzw_hash_probe1(root, code):
    newhash_code = (root << 4 ^ code) & 4095
    return newhash_code


def _lzw_hash_probe2(root, code):
    register = [
     0, 0]
    register[0] = (root << 1) + code | 2048
    register[1] = 0
    temp = register[0] * register[0]
    register[1] = temp >> 16
    register[0] = temp & 65535
    if register[1] == 0:
        carry = 0
    else:
        carry = 1
    for i in range(2):
        for j in range(2):
            old_carry = carry
            carry = register[j] >> 15 & 1
            register[j] = register[j] << 1 | old_carry
            register[j] = register[j] & 65535

    register[0] = (register[0] >> 8 | register[1] << 8) & 4095
    return register[0]


def _lzw_hash_probe3(hash_code):
    _lzw_hash_probeOffset = 509
    newhash_code = hash_code + _lzw_hash_probeOffset & 4095
    return newhash_code


def _lzw_hash_pos_found(hash_code, root, code, dictionary):
    if hash_code < 256:
        return False

    if hash_code not in dictionary:
        return True

    a, b = dictionary[hash_code]
    return a == root and b == code


def _lzw_get_new_hash_code(root, code, dictionary):
    hash_code = _lzw_hash_probe1(root, code)
    if _lzw_hash_pos_found(hash_code, root, code, dictionary):
        return hash_code
    else:
        hash_code = _lzw_hash_probe2(root, code)
        if _lzw_hash_pos_found(hash_code, root, code, dictionary):
            return hash_code
        while 1:
            hash_code = _lzw_hash_probe3(hash_code)
            if _lzw_hash_pos_found(hash_code, root, code, dictionary):
                break

        return hash_code
