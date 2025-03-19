# Copyright 2025 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, Field

from catalystwan.api.configuration_groups.parcel import Global, Variable, _ParcelBase

ServiceType = Literal[
    "Firewall",
    "Intrusion-detection",
    "Intrusion-detection-prevention",
    "NETSVC1",
    "NETSVC10",
    "NETSVC2",
    "NETSVC3",
    "NETSVC4",
    "NETSVC5",
    "NETSVC6",
    "NETSVC7",
    "NETSVC8",
    "NETSVC9",
]


class Services(BaseModel):
    order: Union[Global[str], Variable] = Field()
    service_type: Union[Global[ServiceType], Variable] = Field(
        validation_alias="serviceType", serialization_alias="serviceType"
    )


class ServiceChainParcel(_ParcelBase):
    type_: Literal["service-chain"] = Field(default="service-chain", exclude=True)
    services: Optional[List[Services]] = Field(
        default=None,
        validation_alias=AliasPath("data", "services"),
        description="Services details",
    )
