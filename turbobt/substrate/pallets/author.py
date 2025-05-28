import asyncio
import hashlib
import typing

import bittensor_wallet
import scalecodec

from ..extrinsic import ExtrinsicResult
from ._base import Pallet
from .state import RuntimeVersion


class Author(Pallet):
    async def submitAndWatchExtrinsic(
        self,
        call_module: str,
        call_function: str,
        call_args: dict[str, typing.Any],
        key: bittensor_wallet.Keypair,
        era: dict | None = None,
        nonce: int | None = None,
    ) -> ExtrinsicResult:
        """
        Submit and subscribe to watch an extrinsic until unsubscribed.

        :param call_module: The module to call.
        :type call_module: str
        :param call_function: The function to call.
        :type call_function: str
        :param call_args: The arguments to pass to the function.
        :type call_args: dict[str, typing.Any]
        :param wallet: The wallet associated with the account making this call.
        :type wallet:
        :param era: The era to use for this extrinsic.
        :type era: dict | None
        :param nonce: The nonce to use for this extrinsic.
        :type nonce: int | None
        :return: An asynchronous result of the extrinsic submission.
        :rtype: ExtrinsicResult
        """

        await self.substrate._init_runtime()

        call = self.substrate._registry.create_scale_object(
            "Call",
            metadata=self.substrate._metadata,
        )
        call.encode(
            {
                "call_module": call_module,
                "call_function": call_function,
                "call_args": call_args,
            }
        )

        if not era:
            era = {}

        era_obj = self.substrate._registry.create_scale_object("Era")
        era_obj.encode(era or "00")

        runtime_version, nonce, genesis_hash, block_hash = await asyncio.gather(
            self.substrate.state.getRuntimeVersion(),
            self.substrate.system.accountNextIndex(key.ss58_address),
            self.substrate.chain.getBlockHash(0),
            self.substrate.chain.getBlockHash(era_obj.birth(era.get("current"))),
        )

        extrinsic = self._sign(
            call,
            key,
            nonce=nonce,
            era=era_obj.value,
            block_hash=block_hash,
            genesis_hash=genesis_hash,
            runtime_version=runtime_version,
        )

        subscription_id = await self.substrate.rpc(
            method="author_submitAndWatchExtrinsic",
            params={
                "bytes": str(extrinsic.data),
            },
        )
        subscription = await self.substrate.subscribe(subscription_id)

        return ExtrinsicResult(
            extrinsic,
            subscription,
            self.substrate,
        )

    async def unwatchExtrinsic(self, subscription_id):
        await self.substrate.unsubscribe(subscription_id)

        return await self.substrate.rpc(
            method="author_unwatchExtrinsic",
            params={
                "bytes": subscription_id,
            },
        )

    def _sign(
        self,
        call: scalecodec.types.GenericCall,
        keypair: bittensor_wallet.Keypair,
        nonce: int | None,
        era: dict,
        block_hash: str,
        genesis_hash: str,
        runtime_version: RuntimeVersion,
        tip: int = 0,
        tip_asset_id=None,
    ):
        extrinsic_payload = self.substrate._registry.create_scale_object(
            "ExtrinsicPayloadValue",
        )

        if "signed_extensions" in self.substrate._metadata[1][1]["extrinsic"]:
            signed_extensions = self.substrate._metadata.get_signed_extensions()

            extrinsic_payload.type_mapping = [
                ["call", "CallBytes"],
            ]
            extrinsic_payload.type_mapping.extend(
                [
                    attr,
                    signed_extensions[ext][ext_type],
                ]
                for attr, ext, ext_type in (
                    ("era", "CheckMortality", "extrinsic"),
                    ("era", "CheckEra", "extrinsic"),
                    ("nonce", "CheckNonce", "extrinsic"),
                    ("tip", "ChargeTransactionPayment", "extrinsic"),
                    ("asset_id", "ChargeAssetTxPayment", "extrinsic"),
                    ("mode", "CheckMetadataHash", "extrinsic"),
                    ("spec_version", "CheckSpecVersion", "additional_signed"),
                    ("transaction_version", "CheckTxVersion", "additional_signed"),
                    ("genesis_hash", "CheckGenesis", "additional_signed"),
                    ("block_hash", "CheckMortality", "additional_signed"),
                    ("block_hash", "CheckEra", "additional_signed"),
                    ("metadata_hash", "CheckMetadataHash", "additional_signed"),
                )
                if ext in signed_extensions
            )

        extrinsic_payload.encode(
            {
                "asset_id": {
                    "asset_id": tip_asset_id,
                    "tip": tip,
                },
                "block_hash": block_hash,
                "call": str(call.data),
                "era": era,
                "genesis_hash": genesis_hash,
                "metadata_hash": None,
                "mode": "Disabled",
                "nonce": nonce,
                "spec_version": runtime_version["specVersion"],
                "tip": tip,
                "transaction_version": runtime_version["transactionVersion"],
            }
        )

        if extrinsic_payload.data.length > 256:
            extrinsic_payload.data = scalecodec.ScaleBytes(
                data=hashlib.blake2b(
                    extrinsic_payload.data.data, digest_size=32
                ).digest()
            )

        signature = keypair.sign(extrinsic_payload.data)

        # https://github.com/polkadot-js/api/blob/cf7e2f01ac61be2c18523ea210c018f96c18ad3d/packages/api/src/submittable/createClass.ts#L247
        extrinsic = self.substrate._registry.create_scale_object(
            "Extrinsic",
            metadata=self.substrate._metadata,
        )
        extrinsic.encode(
            {
                "account_id": f"0x{keypair.public_key.hex()}",
                "signature": f"0x{signature.hex()}",
                "call_function": call.value["call_function"],
                "call_module": call.value["call_module"],
                "call_args": call.value["call_args"],
                "nonce": nonce,
                "era": era,
                "tip": tip,
                "asset_id": {"tip": tip, "asset_id": tip_asset_id},
                "mode": "Disabled",
                # signer?
                "signature_version": keypair.crypto_type,
            }
        )

        return extrinsic
