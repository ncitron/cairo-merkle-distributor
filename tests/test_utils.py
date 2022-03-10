from starkware.starkware_utils.error_handling import StarkException

# taken from https://github.com/OpenZeppelin/cairo-contracts/blob/main/tests/utils.py#L86
async def assert_revert(fun, reverted_with=None):
    try:
        await fun
        assert False
    except StarkException as err:
        _, error = err.args
        if reverted_with is not None:
            assert reverted_with in error['message']
