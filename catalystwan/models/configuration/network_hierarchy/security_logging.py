# Copyright 2026 Cisco Systems, Inc. and its affiliates
from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal, Optional, Union, get_args

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase

HSLName = Literal[
    "server1",
    "server2",
    "server3",
    "server4",
]
SERVER_NAMES: tuple[HSLName, ...] = get_args(HSLName)


class HSLEntry(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    name: Optional[HSLName] = Field(
        default=None,
        validation_alias="name",
        serialization_alias="name",
        description="This field is required in version >=20.16. In versions <20.16 it must be None",
    )
    vrf: Global[str] = Field(validation_alias="vrf", serialization_alias="vrf")
    serverIp: Global[Union[IPv4Address, IPv6Address]] = Field(
        validation_alias="serverIp", serialization_alias="serverIp"
    )
    port: Global[int] = Field(validation_alias="port", serialization_alias="port")


class UTDSyslog(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    vpn: Global[str] = Field(validation_alias="vpn", serialization_alias="vpn")
    server_ip: Global[IPv4Address] = Field(validation_alias="serverIp", serialization_alias="serverIp")


class SecurityLoggingParcel(_ParcelBase):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    type_: Literal["security-logging"] = Field(default="security-logging", exclude=True)
    parcel_name: str = Field(
        default="SecurityLogging",
        exclude=True,
        description="This field is not defined for this model",
        serialization_alias="name",
        validation_alias="name",
    )
    high_speed_logging: List[HSLEntry] = Field(
        default_factory=list,
        max_length=4,
        validation_alias=AliasPath("data", "highSpeedLogging"),
        description="High Speed Logging",
    )
    utd_syslog: List[UTDSyslog] = Field(
        default_factory=list,
        validation_alias=AliasPath("data", "utdSyslog"),
        description="UTD Syslog",
    )

    def add_hsl_server(
        self,
        vrf: str,
        serverIp: Union[IPv4Address, IPv6Address],
        port: int,
        name: Optional[HSLName] = None,
    ):
        if self.high_speed_logging is None:
            self.high_speed_logging = []

        if len(self.high_speed_logging) >= 4:
            raise ValueError("Max 4 servers allowed")

        taken_server_names = {entry.name for entry in self.high_speed_logging}

        if name is not None and name in taken_server_names:
            raise ValueError(f"{name} is already used")

        self.high_speed_logging.append(
            HSLEntry(
                name=name,
                vrf=Global[str](value=vrf),
                serverIp=Global[Union[IPv4Address, IPv6Address]](value=serverIp),
                port=Global[int](value=port),
            )
        )

    def get_next_server_name(self) -> HSLName | None:
        taken_server_names = {entry.name for entry in self.high_speed_logging}
        name: HSLName | None = next((name for name in SERVER_NAMES if name not in taken_server_names), None)
        return name
