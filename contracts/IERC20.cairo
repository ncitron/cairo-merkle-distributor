%lang starknet

from starkware.cairo.common.uint256 import Uint256

@contract_interface
namespace IERC20:
    func transfer(recipient: felt, amount: Uint256) -> (success: felt):
    end
end
