from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from domain.targeted_resume import FactName, FactualSourceType, ResumeSection


class TargetedResumePreviewRequest(BaseModel):
    profile_id: int = Field(gt=0)
    job_id: int = Field(gt=0)

    model_config = ConfigDict(extra="forbid")


class SourceReferenceResponse(BaseModel):
    source_type: FactualSourceType
    source_id: int

    model_config = ConfigDict(from_attributes=True)


class FactualValueResponse(BaseModel):
    name: FactName
    value: str | int | bool | date

    model_config = ConfigDict(from_attributes=True)


class FactualBlockResponse(BaseModel):
    section: ResumeSection
    facts: tuple[FactualValueResponse, ...]
    provenance: tuple[SourceReferenceResponse, ...]

    model_config = ConfigDict(from_attributes=True)


class TargetedResumeCompositionResponse(BaseModel):
    profile_id: int
    job_id: int
    ruleset_version: str
    blocks: tuple[FactualBlockResponse, ...]
    source_manifest: tuple[SourceReferenceResponse, ...]

    model_config = ConfigDict(from_attributes=True)


class TargetedResumePreviewResponse(BaseModel):
    preview_id: str
    state: Literal["preview"]
    composition: TargetedResumeCompositionResponse

    model_config = ConfigDict(from_attributes=True)
