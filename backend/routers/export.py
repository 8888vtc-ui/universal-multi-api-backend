"""Export Router - Export search results in various formats"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import Dict, Any, List, Optional
import json
import csv
import io

router = APIRouter(prefix="/api/export", tags=["export"])


@router.post("/json")
async def export_to_json(data: Dict[str, Any]):
    """
    📄 Export data to JSON format
    
    Returns a downloadable JSON file
    """
    try:
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        return StreamingResponse(
            io.StringIO(json_str),
            media_type="application/json",
            headers={
                "Content-Disposition": "attachment; filename=export.json"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/csv")
async def export_to_csv(
    data: List[Dict[str, Any]],
    filename: str = Query("export", description="Filename without extension")
):
    """
    📊 Export data to CSV format
    
    Expects a list of dictionaries with the same keys
    """
    try:
        if not data:
            raise HTTPException(status_code=400, detail="No data to export")
        
        output = io.StringIO()
        
        # Get headers from first item
        headers = list(data[0].keys())
        
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        
        for row in data:
            # Flatten nested dicts
            flat_row = {}
            for key, value in row.items():
                if isinstance(value, (dict, list)):
                    flat_row[key] = json.dumps(value, ensure_ascii=False)
                else:
                    flat_row[key] = value
            writer.writerow(flat_row)
        
        output.seek(0)
        
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename}.csv"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/markdown")
async def export_to_markdown(
    data: Dict[str, Any],
    title: str = Query("Export", description="Document title")
):
    """
    [NOTE] Export data to Markdown format
    """
    try:
        md_lines = [f"# {title}\n"]
        
        def dict_to_md(d: dict, level: int = 2):
            lines = []
            for key, value in d.items():
                if isinstance(value, dict):
                    lines.append(f"{'#' * level} {key}\n")
                    lines.extend(dict_to_md(value, level + 1))
                elif isinstance(value, list):
                    lines.append(f"{'#' * level} {key}\n")
                    for item in value:
                        if isinstance(item, dict):
                            lines.append(f"- {json.dumps(item, ensure_ascii=False)}")
                        else:
                            lines.append(f"- {item}")
                    lines.append("")
                else:
                    lines.append(f"**{key}**: {value}\n")
            return lines
        
        md_lines.extend(dict_to_md(data))
        md_content = "\n".join(md_lines)
        
        return StreamingResponse(
            io.StringIO(md_content),
            media_type="text/markdown",
            headers={
                "Content-Disposition": "attachment; filename=export.md"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/formats")
async def get_export_formats():
    """
    📋 Get available export formats
    """
    return {
        "formats": [
            {"format": "json", "description": "JSON format", "endpoint": "/api/export/json"},
            {"format": "csv", "description": "CSV format", "endpoint": "/api/export/csv"},
            {"format": "markdown", "description": "Markdown format", "endpoint": "/api/export/markdown"}
        ]
    }






