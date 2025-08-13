from __future__ import annotations

import ipaddress
import typing

import bittensor_wallet

from ...substrate.extrinsic import ExtrinsicResult
from ...substrate.pallets.author import DEFAULT_ERA, Era
from ..types import (
    HotKey,
    NetUid,
    Uid,
)
from ._base import Pallet
from ._types import StorageDoubleMap

if typing.TYPE_CHECKING:
    from .. import Subtensor


class AssociatedEvmAddress(typing.NamedTuple):
    h160_address: str
    last_block: int  # last block where ownership was proven


class NeuronCertificate(typing.TypedDict):
    algorithm: int
    public_key: str


class ZippedWeights(typing.NamedTuple):
    uid: Uid
    weight: int


class SubtensorModule(Pallet):
    def __init__(self, subtensor: Subtensor):
        super().__init__(subtensor)

        self.AssociatedEvmAddress = StorageDoubleMap[NetUid, Uid, AssociatedEvmAddress](
            subtensor,
            "SubtensorModule",
            "AssociatedEvmAddress",
        )
        self.CRV3WeightCommitsV2 = StorageDoubleMap[NetUid, int, None](
            subtensor,
            "SubtensorModule",
            "CRV3WeightCommitsV2",
        )
        self.NeuronCertificates = StorageDoubleMap[NetUid, HotKey, NeuronCertificate](
            subtensor,
            "SubtensorModule",
            "NeuronCertificates",
        )
        self.Uids = StorageDoubleMap[NetUid, HotKey, Uid](
            subtensor,
            "SubtensorModule",
            "Uids",
        )
        self.Weights = StorageDoubleMap[NetUid, Uid, list[ZippedWeights]](
            subtensor,
            "SubtensorModule",
            "Weights",
        )

    async def burned_register(
        self,
        netuid: int,
        hotkey: str,
        wallet: bittensor_wallet.Wallet,
        era: Era | None = DEFAULT_ERA,
    ) -> ExtrinsicResult:
        """
        Registers a neuron on the Bittensor network by recycling TAO.

        :param netuid: The unique identifier of the subnet.
        :type netuid: int
        :param hotkey: Hotkey to be registered to the network.
        :type hotkey: str
        :param wallet: The wallet associated with the neuron to be registered.
        :type wallet:
        :return: An asynchronous result of the extrinsic submission.
        :rtype: ExtrinsicResult
        """

        return await self.subtensor.author.submitAndWatchExtrinsic(
            "SubtensorModule",
            "burned_register",
            {
                "netuid": netuid,
                "hotkey": hotkey,
            },
            key=wallet.coldkey,
            era=era,
        )

    async def commit_crv3_weights(
        self,
        netuid: int,
        commit: bytes,
        reveal_round: int,
        wallet: bittensor_wallet.Wallet,
        era: Era | None = DEFAULT_ERA,
    ) -> ExtrinsicResult:
        return await self.subtensor.author.submitAndWatchExtrinsic(
            "SubtensorModule",
            "commit_crv3_weights",
            {
                "netuid": netuid,
                "commit": f"0x{commit.hex()}",
                "reveal_round": reveal_round,
            },
            key=wallet.hotkey,
            era=era,
        )

    async def commit_timelocked_weights(
        self,
        netuid: int,
        commit: bytes,
        reveal_round: int,
        commit_reveal_version: int,
        wallet: bittensor_wallet.Wallet,
        era: Era | None = DEFAULT_ERA,
    ) -> ExtrinsicResult:
        return await self.subtensor.author.submitAndWatchExtrinsic(
            "SubtensorModule",
            "commit_timelocked_weights",
            {
                "netuid": netuid,
                "commit": f"0x{commit.hex()}",
                "reveal_round": reveal_round,
                "commit_reveal_version": commit_reveal_version,
            },
            key=wallet.hotkey,
            era=era,
        )

    async def register_network(
        self,
        hotkey: bittensor_wallet.Keypair,
        mechid: int,
        wallet: bittensor_wallet.Wallet,
        era: Era | None = DEFAULT_ERA,
    ) -> ExtrinsicResult:
        return await self.subtensor.author.submitAndWatchExtrinsic(
            "SubtensorModule",
            "register_network",
            {
                "hotkey": hotkey,
                "mechid": mechid,
            },
            key=wallet.coldkey,
            era=era,
        )

    async def serve_axon(
        self,
        netuid: int,
        ip: str,
        port: int,
        wallet: bittensor_wallet.Wallet,
        protocol: int,
        version: int,
        placeholder1: int = 0,
        placeholder2: int = 0,
        era: Era | None = DEFAULT_ERA,
    ) -> ExtrinsicResult:
        """
        Submits an extrinsic to serve an Axon endpoint on the Bittensor network.

        :param netuid: The unique identifier of the subnet.
        :type netuid: int
        :param ip: The IP address of the Axon endpoint.
        :type ip: str
        :param port: The port number for the Axon endpoint.
        :type port: int
        :param wallet: The wallet associated with the Axon service.
        :type wallet: bittensor_wallet.Wallet
        :param version: The Bittensor version identifier.
        :type version: int
        :param placeholder1: Placeholder for further extra params.
        :type placeholder1: int
        :param placeholder2: Placeholder for further extra params.
        :type placeholder2: int
        :return: An asynchronous result of the extrinsic submission.
        :rtype: ExtrinsicResult
        """

        ip_address = ipaddress.ip_address(ip)

        return await self.subtensor.author.submitAndWatchExtrinsic(
            "SubtensorModule",
            "serve_axon",
            {
                "ip_type": ip_address.version,
                "ip": int(ip_address),
                "netuid": netuid,
                "placeholder1": placeholder1,
                "placeholder2": placeholder2,
                "port": port,
                "protocol": protocol,
                "version": version,
            },
            key=wallet.hotkey,
            era=era,
        )

    async def serve_axon_tls(
        self,
        netuid: int,
        ip: str,
        port: int,
        certificate: bytes,
        wallet: bittensor_wallet.Wallet,
        protocol: int,
        version: int,
        placeholder1: int = 0,
        placeholder2: int = 0,
        era: Era | None = DEFAULT_ERA,
    ) -> ExtrinsicResult:
        """
        Submits an extrinsic to serve an Axon endpoint on the Bittensor network.

        :param netuid: The unique identifier of the subnet.
        :type netuid: int
        :param ip: The IP address of the Axon endpoint.
        :type ip: str
        :param port: The port number for the Axon endpoint.
        :type port: int
        :param wallet: The wallet associated with the Axon service.
        :type wallet: bittensor_wallet.Wallet
        :param certificate: The certificate for securing the Axon endpoint.
        :type certificate: bytes
        :param protocol: Axon protocol. TCP, UDP, other.
        :type protocol: int
        :param version: The Bittensor version identifier.
        :type version: int
        :param placeholder1: Placeholder for further extra params.
        :type placeholder1: int
        :param placeholder2: Placeholder for further extra params.
        :type placeholder2: int
        :return: An asynchronous result of the extrinsic submission.
        :rtype: ExtrinsicResult
        """

        ip_address = ipaddress.ip_address(ip)

        return await self.subtensor.author.submitAndWatchExtrinsic(
            "SubtensorModule",
            "serve_axon_tls",
            {
                "certificate": certificate,
                "ip_type": ip_address.version,
                "ip": int(ip_address),
                "netuid": netuid,
                "placeholder1": placeholder1,
                "placeholder2": placeholder2,
                "port": port,
                "protocol": protocol,
                "version": version,
            },
            key=wallet.hotkey,
            era=era,
        )

    async def set_weights(
        self,
        netuid: int,
        dests: list[int],
        weights: list[int],
        version_key: int,
        wallet: bittensor_wallet.Wallet,
        era: Era | None = DEFAULT_ERA,
    ) -> ExtrinsicResult:
        return await self.subtensor.author.submitAndWatchExtrinsic(
            "SubtensorModule",
            "set_weights",
            {
                "netuid": netuid,
                "dests": dests,
                "weights": weights,
                "version_key": version_key,
            },
            key=wallet.hotkey,
            era=era,
        )
