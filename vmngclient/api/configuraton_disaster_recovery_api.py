from typing import List

from attr import define, field  # type: ignore

from vmngclient.dataclasses import DataclassBase
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import FIELD_NAME, create_dataclass


@define
class ClusterInfoDevice(DataclassBase):
    hostname: str = field(metadata={FIELD_NAME: "host-name"})
    device_ip: str = field(metadata={FIELD_NAME: "deviceIP"})
    state: str  # might be good idea to have enum here
    is_current_vmanage: bool = field(metadata={FIELD_NAME: "isCurrentVManage"})

    @staticmethod
    def from_dict(dict):
        return create_dataclass(ClusterInfoDevice, dict)


@define
class ClusterInfo(DataclassBase):
    primary: List[ClusterInfoDevice] = field(converter=ClusterInfoDevice.from_dict)
    secondary: List[ClusterInfoDevice] = field(converter=ClusterInfoDevice.from_dict)


class ConfigurationDisasterRecoveryApi:
    def __init__(self, session: vManageSession):
        self.session = session

    def get_cluster_info(self):
        response = self.session.get("dataservice/disasterrecovery/clusterInfo")
        return create_dataclass(ClusterInfo, response.payload.json.get("clusterInfo"))


def test_dataclass_parse():
    json_payload = {
        "clusterInfo": {
            "primary": [
                {
                    "host-name": "vm12",
                    "deviceIP": "10.0.105.32",
                    "state": "UP",
                    "isCurrentVManage": True,
                }
            ],
            "secondary": [
                {"host-name": "dc1-vm3", "deviceIP": "123.10.1.103", "state": "UP", "isCurrentVManage": True},
                {"host-name": "dc1-vm2", "deviceIP": "123.10.1.102", "state": "UP", "isCurrentVManage": True},
            ],
        }
    }
    return create_dataclass(ClusterInfo, json_payload.get("clusterInfo"))