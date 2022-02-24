from starkware.crypto.signature.fast_pedersen_hash import pedersen_hash

# generates merkle root from values list
# each pair of values must be in sorted order
def generate_merkle_root(values: list[int]) -> int:
    if len(values) == 1:
        return values[0]

    if len(values) % 2 != 0:
        values.append(0)

    next_level = get_next_level(values)
    return generate_merkle_root(next_level)

# generates merkle proof from an index of the value list
# each pair of values must be in sorted order
def generate_merkle_proof(values: list[int], index: int) -> list[int]:
    return generate_proof_helper(values, index, [])

# checks the validity of a merkle proof
# the last element of the proof should be the root
def verify_merkle_proof(leaf: int, proof: list[int]) -> bool:
    root = proof[len(proof)-1]
    proof = proof[:-1]
    curr = leaf

    for proofElement in proof:
        if curr < proofElement:
            curr = pedersen_hash(curr, proofElement)
        else:
            curr = pedersen_hash(proofElement, curr)

    return curr == root

def get_next_level(level: list[int]) -> list[int]:
    next_level = []

    for i in range(0, len(level), 2):
        node = 0
        if level[i] < level[i+1]:
            node = pedersen_hash(level[i], level[i+1])
        else:
            node = pedersen_hash(level[i+1], level[i])

        next_level.append(node)

    return next_level

def generate_proof_helper(level: list[int], index: int, proof: list[int]) -> list[int]:
    if len(level) == 1:
        return proof
    if len(level) % 2 != 0:
        level.append(0)

    next_level = get_next_level(level)
    index_parent = 0

    for i in range(0, len(level)):
        if i == index:
            index_parent = i // 2
            if i % 2 == 0:
                proof.append(level[index+1])
            else:
                proof.append(level[index-1])

    return generate_proof_helper(next_level, index_parent, proof)