import os
import pytest

from starkware.starknet.testing.starknet import Starknet
from merkle_utils import generate_merkle_proof, generate_merkle_root

CONTRACT_FILE = os.path.join("contracts", "merkle_mock.cairo")

@pytest.mark.asyncio
async def test_merkle():

    starknet = await Starknet.empty()
    contract = await starknet.deploy(source=CONTRACT_FILE)

    values = [6, 7, 3, 4, 5, 12, 2]
    leaf_index = 1

    proof = generate_merkle_proof(values, leaf_index)
    root = generate_merkle_root(values)

    exec_info = await contract.verify(values[leaf_index], root, proof).call()
    is_valid = exec_info.result.res

    assert is_valid == 1

@pytest.mark.asyncio
async def test_merkle_fail():

    starknet = await Starknet.empty()
    contract = await starknet.deploy(source=CONTRACT_FILE)

    values = [6, 7, 3, 4, 5, 12, 2]
    leaf_index = 1

    proof = generate_merkle_proof(values, leaf_index)
    root = generate_merkle_root(values)

    # provide a wrong leaf value
    exec_info = await contract.verify(42, root, proof).call()
    is_valid = exec_info.result.res

    assert is_valid == 0