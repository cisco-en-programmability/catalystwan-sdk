# Copyright 2026 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from pathlib import Path

from catalystwan.endpoints import APIEndpoints, CustomPayloadType, PreparedPayload, post, versions
from catalystwan.models.configuration.packages import (
    CatalogPackageExportRequest,
    CatalogPackageImportResponse,
    TemplatePackageExportRequest,
)


class CatalogImportTarballFile(CustomPayloadType):
    def __init__(self, filename: Path):
        self.filename = filename

    def prepared(self) -> PreparedPayload:
        data = open(self.filename, "rb")
        return PreparedPayload(files={"file": (Path(data.name).name, data)})


class DeviceConfigPackageEndpoints(APIEndpoints):

    @versions(supported_versions=(">=20.12"), raises=False)
    @post("/templates/package/export")
    def export_templates(self, payload: TemplatePackageExportRequest = TemplatePackageExportRequest()) -> bytes: ...

    @versions(supported_versions=(">=20.14"), raises=False)
    @post("/v1/packages/export")
    def export_catalog(self, payload: CatalogPackageExportRequest) -> bytes: ...

    @versions(supported_versions=(">=20.14"), raises=False)
    @post("/v1/packages/import")
    def import_catalog(self, payload: CatalogImportTarballFile) -> CatalogPackageImportResponse: ...
