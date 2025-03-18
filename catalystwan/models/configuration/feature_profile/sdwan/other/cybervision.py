# Copyright 2025 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import AddressWithMask, RefIdItem

CaptureInterfaceSubnetMask = Literal[
    "0.0.0.0",
    "128.0.0.0",
    "192.0.0.0",
    "224.0.0.0",
    "240.0.0.0",
    "248.0.0.0",
    "252.0.0.0",
    "254.0.0.0",
    "255.0.0.0",
    "255.128.0.0",
    "255.192.0.0",
    "255.224.0.0",
    "255.240.0.0",
    "255.252.0.0",
    "255.254.0.0",
    "255.255.0.0",
    "255.255.128.0",
    "255.255.192.0",
    "255.255.224.0",
    "255.255.240.0",
    "255.255.248.0",
    "255.255.252.0",
    "255.255.254.0",
    "255.255.255.0",
    "255.255.255.128",
    "255.255.255.192",
    "255.255.255.224",
    "255.255.255.240",
    "255.255.255.248",
    "255.255.255.252",
    "255.255.255.254",
    "255.255.255.255",
]


class VirtualApplication(BaseModel):
    capture_interface_i_p: Union[Global[str], Default[None]] = Field(
        validation_alias="captureInterfaceIP", serialization_alias="captureInterfaceIP"
    )
    capture_interface_subnet_mask: Union[Global[CaptureInterfaceSubnetMask], Default[None]] = Field(
        validation_alias="captureInterfaceSubnetMask", serialization_alias="captureInterfaceSubnetMask"
    )
    multiple_erspan_source_interfaces: List[Global[str]] = Field(
        validation_alias="multipleErspanSourceInterfaces",
        serialization_alias="multipleErspanSourceInterfaces",
        description="multipleErspanSourceInterfaces",
    )
    virtual_port_group6_ip: Union[Global[str], Default[None]] = Field(
        validation_alias="virtualPortGroup6Ip", serialization_alias="virtualPortGroup6Ip"
    )
    collection_interface_i_p: Optional[Variable] = Field(
        default=None, validation_alias="collectionInterfaceIP", serialization_alias="collectionInterfaceIP"
    )
    collection_interface_subnet_mask: Optional[Variable] = Field(
        default=None,
        validation_alias="collectionInterfaceSubnetMask",
        serialization_alias="collectionInterfaceSubnetMask",
    )
    cvc_id: Optional[Global[str]] = Field(default=None, validation_alias="cvcId", serialization_alias="cvcId")
    virtual_port_group5_ip: Optional[Variable] = Field(
        default=None, validation_alias="virtualPortGroup5Ip", serialization_alias="virtualPortGroup5Ip"
    )


class CyberVisonParcel(_ParcelBase):
    type_: Literal["cybervision"] = Field(default="cybervision", exclude=True)
    virtual_application: VirtualApplication = Field(
        validation_alias=AliasPath("data", "virtualApplication"),
        description="Virtual application Instance",
    )
