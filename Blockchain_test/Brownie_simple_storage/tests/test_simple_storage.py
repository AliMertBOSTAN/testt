from cmath import exp
from unittest import expectedFailure
from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange
    account = accounts[0]
    # act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    # assert
    assert starting_value == expected


def test_updating_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # act
    expected = 15
    simple_storage.store(expected, {"from": account})
    # assert
    assert expected == simple_storage.retrieve()
