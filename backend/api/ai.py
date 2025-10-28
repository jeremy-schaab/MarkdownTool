"""AI summarization API endpoints"""

from fastapi import APIRouter, HTTPException
from typing import List
import logging
import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src/markdown_manager'))

from models.ai import (
    AISummaryRequest,
    AISummaryResponse,
    AITemplate,
    AITemplateType,
    AISaveSummaryRequest
)

router = APIRouter()
logger = logging.getLogger(__name__)

# Import AI service from existing codebase
try:
    from ai_service import ai_service, ANALYSIS_TEMPLATES
except ImportError:
    logger.warning("Could not import ai_service from existing codebase")
    ai_service = None
    ANALYSIS_TEMPLATES = {}


@router.get("/templates", response_model=List[AITemplate])
async def get_templates():
    """
    Get available AI summary templates.
    """
    templates = []

    # Convert existing templates to API format
    for key, template in ANALYSIS_TEMPLATES.items():
        templates.append(AITemplate(
            type=key,
            name=template["name"],
            description=template["description"],
            prompt=template.get("prompt", "")
        ))

    return templates


@router.post("/summarize", response_model=AISummaryResponse)
async def generate_summary(request: AISummaryRequest):
    """
    Generate AI summary of markdown content using specified template.
    """
    try:
        if not ai_service:
            raise HTTPException(
                status_code=503,
                detail="AI service not available. Check Azure OpenAI configuration."
            )

        # Validate template
        if request.template == AITemplateType.CUSTOM and not request.custom_prompt:
            raise HTTPException(
                status_code=400,
                detail="Custom prompt required when using custom template"
            )

        # Generate summary using existing service
        if request.template == AITemplateType.CUSTOM:
            # Use custom prompt
            summary_result = ai_service.generate_summary(
                content=request.content,
                custom_prompt=request.custom_prompt
            )
        else:
            # Use template
            template_key = request.template.value
            if template_key not in ANALYSIS_TEMPLATES:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid template: {template_key}"
                )

            summary_result = ai_service.generate_summary_with_template(
                content=request.content,
                template_name=template_key
            )

        if not summary_result.get("success", False):
            return AISummaryResponse(
                summary="",
                template_used=request.template.value,
                tokens_used=summary_result.get("tokens_used"),
                model=request.model,
                success=False,
                error=summary_result.get("error", "Unknown error")
            )

        return AISummaryResponse(
            summary=summary_result.get("summary", ""),
            template_used=request.template.value,
            tokens_used=summary_result.get("tokens_used"),
            model=request.model,
            success=True
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return AISummaryResponse(
            summary="",
            template_used=request.template.value,
            model=request.model,
            success=False,
            error=str(e)
        )


@router.post("/save-summary")
async def save_summary(request: AISaveSummaryRequest):
    """
    Save AI summary to project's ai-summary folder structure.
    """
    try:
        import re
        import time
        from pathlib import Path

        # Build subfolder using analysis/template name
        safe_template = re.sub(r"[^a-z0-9-_]", "", request.template_name.replace(" ", "-").lower())
        summary_folder = Path(request.project_root) / "ai-summary" / safe_template

        # Create folder if it doesn't exist
        summary_folder.mkdir(parents=True, exist_ok=True)

        # Use the base file name with a '_summary' suffix
        source_name = Path(request.source_file).stem
        summary_filename = f"{source_name}_summary.md"
        full_path = summary_folder / summary_filename

        # Write summary with metadata
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(f"# AI Summary: {Path(request.source_file).name}\n\n")
            f.write(f"**Template**: {request.template_name}  \n")
            f.write(f"**Generated**: {time.strftime('%Y-%m-%d %H:%M:%S')}  \n")
            f.write(f"**Source**: {Path(request.source_file).name}  \n\n")
            f.write("---\n\n")
            f.write(request.summary)

        return {
            "success": True,
            "message": f"Summary saved to: {full_path.relative_to(request.project_root)}",
            "path": str(full_path)
        }

    except Exception as e:
        logger.error(f"Error saving summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estimate-tokens")
async def estimate_tokens(content: str):
    """
    Estimate token count for content.
    """
    try:
        if not ai_service:
            raise HTTPException(
                status_code=503,
                detail="AI service not available"
            )

        token_count = ai_service.estimate_tokens(content)

        return {
            "content_length": len(content),
            "estimated_tokens": token_count,
            "estimated_cost_usd": token_count * 0.00015 / 1000  # Rough estimate for GPT-4o-mini
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error estimating tokens: {e}")
        raise HTTPException(status_code=500, detail=str(e))
