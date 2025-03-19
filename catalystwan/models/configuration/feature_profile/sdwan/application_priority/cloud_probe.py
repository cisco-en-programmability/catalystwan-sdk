# Copyright 2025 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, Field

from catalystwan.api.configuration_groups.parcel import Global, Variable, _ParcelBase
from catalystwan.models.common import TLOCColor

CloudSaaSDeviceRole = Literal[
    "client",
    "dia",
    "gateway",
]

VpnType = Literal[
    "service-vpn",
    "vpn-0",
]


class Loadbalance(BaseModel):
    latency: Optional[Union[Global[str], Variable]] = Field(default=None)
    loss: Optional[Union[Global[str], Variable]] = Field(default=None)
    source_ip_based: Optional[Union[Global[bool], Variable]] = Field(
        default=None, validation_alias="sourceIpBased", serialization_alias="sourceIpBased"
    )


class CloudProbeParcel(_ParcelBase):
    type_: Literal["could-probe"] = Field(default="could-probe", exclude=True)
    cloud_saa_s_device_role: Optional[Union[Variable, Global[CloudSaaSDeviceRole]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "cloudSaaSDeviceRole"),
    )
    cloud_saa_s_l_b_enabled: Optional[Union[Global[bool], Variable]] = Field(
        default=None,
        validation_alias=AliasPath("data", "cloudSaaSLBEnabled"),
    )
    cloud_saa_s_sig_enabled: Optional[Union[Global[bool], Variable]] = Field(
        default=None,
        validation_alias=AliasPath("data", "cloudSaaSSigEnabled"),
    )
    interface_list: Optional[Union[Global[List[str]], Variable]] = Field(
        default=None,
        validation_alias=AliasPath("data", "interfaceList"),
    )
    loadbalance: Optional[Loadbalance] = Field(
        default=None,
        validation_alias=AliasPath("data", "loadbalance"),
    )
    parcel_type: Optional[str] = Field(default=None, validation_alias="parcelType", serialization_alias="parcelType")
    sig_tunnel_list: Optional[Union[Global[List[str]], Variable]] = Field(
        default=None,
        validation_alias=AliasPath("data", "sigTunnelList"),
    )
    tloc_list: Optional[Union[Global[List[TLOCColor]], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "tlocList")
    )
    vpn_type: Optional[Union[Variable, Global[VpnType]]] = Field(
        default=None, validation_alias=AliasPath("data", "vpnType")
    )
