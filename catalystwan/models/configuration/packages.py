# Copyright 2026 Cisco Systems, Inc. and its affiliates
from typing import Iterable, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Self

CatalogObjectType = Literal[
    "config-group",
    "policy-group",
    "topology-group",
]


class CatalogPackageContents(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    object_list: List[UUID] = Field(
        default_factory=list,
        validation_alias="objectList",
        serialization_alias="objectList",
        description="list of object uuids",
    )
    object_type: Optional[CatalogObjectType] = Field(
        default=None, validation_alias="objectType", serialization_alias="objectType"
    )


class CatalogPackageExportRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    package_contents: List[CatalogPackageContents] = Field(
        default_factory=list,
        validation_alias="packageContents",
        serialization_alias="packageContents",
        description="package contents",
    )

    def add_objects(self, object_type: CatalogObjectType, ids: Iterable[UUID]) -> Self:
        contents = CatalogPackageContents(object_type=object_type, object_list=list(ids))
        self.package_contents.append(contents)
        return self


class CatalogPackageImportResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    task_id: UUID = Field(validation_alias="taskId", serialization_alias="taskId")


class TemplatePackageExportRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    template_ids: Optional[List[UUID]] = Field(
        default=list(),
        validation_alias="templateIds",
        serialization_alias="templateIds",
        description="Select Device Templates for export by providing list of Ids"
        "when list empty or parameter is missing all templates will be provided",
    )
    extras: bool = Field(default=True, description="Include extra items for Config Migration Tool")
