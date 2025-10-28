"""AI summarization Pydantic models"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class AITemplateType(str, Enum):
    """AI summary template types"""
    HIGH_LEVEL = "high_level"
    DETAILED = "detailed"
    TECHNICAL = "technical"
    EXECUTIVE = "executive"
    QUICK = "quick"
    CUSTOM = "custom"


class AITemplate(BaseModel):
    """AI template information"""
    type: AITemplateType = Field(..., description="Template type")
    name: str = Field(..., description="Display name")
    description: str = Field(..., description="Template description")
    prompt: str = Field(..., description="Prompt template")


class AISummaryRequest(BaseModel):
    """Request to generate AI summary"""
    content: str = Field(..., description="Markdown content to summarize")
    template: AITemplateType = Field(
        AITemplateType.HIGH_LEVEL,
        description="Summary template to use"
    )
    custom_prompt: Optional[str] = Field(
        None,
        description="Custom prompt (only used when template is 'custom')"
    )
    model: str = Field("gpt-4o-mini", description="AI model to use")


class AISummaryResponse(BaseModel):
    """Response with AI-generated summary"""
    summary: str = Field(..., description="Generated summary")
    template_used: str = Field(..., description="Template that was used")
    tokens_used: Optional[int] = Field(None, description="Number of tokens consumed")
    model: str = Field(..., description="Model used for generation")
    success: bool = Field(True, description="Whether generation was successful")
    error: Optional[str] = Field(None, description="Error message if failed")


class AISaveSummaryRequest(BaseModel):
    """Request to save AI summary to project"""
    summary: str = Field(..., description="Summary content to save")
    source_file: str = Field(..., description="Source markdown file path")
    template_name: str = Field(..., description="Template/analysis name")
    project_root: str = Field(..., description="Project root folder")
