from ._base import Pallet


class System(Pallet):
    async def accountNextIndex(self, account_id: str) -> int:
        """
        Retrieve the next account index for the specified account ID from the node.

        This function queries the blockchain node to get the next available
        transaction index (nonce) for the given account. The nonce is used to
        ensure transactions are processed in order and to prevent replay attacks.

        :param account_id: The SS58-encoded address of the account.
        :type account_id: str
        :return: The next account index (nonce) for the specified account.
        :rtype: int
        """

        return await self.substrate.rpc(
            method="system_accountNextIndex",
            params={
                "account": account_id,
            },
        )
