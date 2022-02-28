%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.uint256 import Uint256, uint256_add

@storage_var
func balances(address: felt) -> (amount: Uint256):
end

@external
func transfer{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr,
    }(
        recipient: felt,
        amount: Uint256
    ) -> (success: felt):
    let (current_balance) = balances.read(recipient)
    let (new_balance, _) = uint256_add(current_balance, amount)
    balances.write(recipient, new_balance)
    return (1)
end

@view
func balance_of{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr
    }(
        address: felt
    ) -> (amount: Uint256):
    let (amount) = balances.read(address)
    return (amount)
end