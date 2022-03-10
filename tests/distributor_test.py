import os
import pytest

from starkware.starknet.testing.starknet import Starknet
from merkle_utils import generate_merkle_proof, generate_merkle_root, get_leaves, verify_merkle_proof
from test_utils import assert_revert

DISTRIBUTOR_FILE = os.path.join("contracts", "distributor.cairo")
TOKEN_FILE = os.path.join("contracts", "ERC20_mock.cairo")

MERKLE_INFO = get_leaves(
    [0xbadbeef, 0xcafebabe, 0x1337, 0x81, 0x1234],
    [1, 4, 18, 9, 72]
)

async def deploy():
    starknet = await Starknet.empty()

    leaves = list(map(lambda x: x[0], MERKLE_INFO))
    root = generate_merkle_root(leaves)

    token = await starknet.deploy(source=TOKEN_FILE)
    distributor = await starknet.deploy(
        source=DISTRIBUTOR_FILE,
        constructor_calldata=[root, token.contract_address]
    )

    return (distributor, token)

@pytest.mark.asyncio
async def test_claim():
    distributor, token = await deploy()
    leaves = list(map(lambda x: x[0], MERKLE_INFO))
    proof = generate_merkle_proof(leaves, 0)

    claimer = MERKLE_INFO[0][1]
    amount = MERKLE_INFO[0][2]

    exec_info = await token.balance_of(claimer).call()
    init_bal = exec_info.result.amount
    assert init_bal.high == 0
    assert init_bal.low == 0

    amount_uint = (amount, 0)
    await distributor.claim(claimer, amount_uint, proof).invoke()
    exec_info = await token.balance_of(claimer).call()
    final_bal = exec_info.result.amount
    assert final_bal.high == 0
    assert final_bal.low == amount

@pytest.mark.asyncio
async def test_claim_incorrect_proof():
    distributor, token = await deploy()
    leaves = list(map(lambda x: x[0], MERKLE_INFO))
    proof = generate_merkle_proof(leaves, 0)

    claimer = 0xbadbadbadbad
    amount = 100000
    amount_uint = (amount, 0)

    await assert_revert(distributor.claim(claimer, amount_uint, proof).invoke())

@pytest.mark.asyncio
async def test_claim_twice():
    distributor, token = await deploy()
    leaves = list(map(lambda x: x[0], MERKLE_INFO))
    proof = generate_merkle_proof(leaves, 0)

    claimer = MERKLE_INFO[0][1]
    amount = MERKLE_INFO[0][2]
    amount_uint = (amount, 0)

    await distributor.claim(claimer, amount_uint, proof).invoke()
    await assert_revert(distributor.claim(claimer, amount_uint, proof).invoke())

