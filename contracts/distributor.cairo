%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.hash import hash2
from starkware.cairo.common.uint256 import Uint256

from contracts.merkle import merkle_verify
from contracts.IERC20 import IERC20

@storage_var
func merkle_root() -> (root: felt):
end

@storage_var
func token_address() -> (token: felt):
end

@storage_var
func has_claimed(leaf: felt) -> (claimed: felt):
end

@constructor
func constructor{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(
        root: felt,
        token: felt
    ):
    merkle_root.write(value=root)
    token_address.write(value=token)
    return ()
end

@external
func claim{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(
        recipient: felt,
        amount: Uint256,
        proof_len: felt,
        proof: felt*
    ):
    alloc_locals

    let (amount_hash) = hash2{hash_ptr=pedersen_ptr}(amount.low, amount.high)
    let (leaf) = hash2{hash_ptr=pedersen_ptr}(recipient, amount_hash)

    # check that leaf has not been claimed
    let (claimed) = has_claimed.read(leaf)
    assert claimed = 0

    # check that proof is valid
    let (root) = merkle_root.read()
    let (proof_valid) = merkle_verify(leaf, root, proof_len, proof)
    assert proof_valid = 1

    # mark leaf as claimed
    has_claimed.write(leaf, 1)

    # transfer tokens to recipient
    let (token) = token_address.read()
    let (success) = IERC20.transfer(token, recipient, amount)
    assert success = 1

    return ()
end