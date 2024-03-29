from brownie import FundMe, config, network

from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
)


def deploy_fund_me():
    account = get_account()
    fund_me = FundMe.deploy({"from": account}, publish_source=True)
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
