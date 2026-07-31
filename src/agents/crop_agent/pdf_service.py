"""PDF generation service for crop diagnosis reports.

Converts markdown report → HTML template → PDF using WeasyPrint.
"""

import base64
import re
from datetime import datetime
from pathlib import Path

from src.utils import logger

try:
    import markdown
except ImportError:
    markdown = None

try:
    from weasyprint import HTML
except ImportError:
    HTML = None


def _parse_cover_meta(md_text: str) -> dict:
    """Extract metadata from markdown for the cover page."""
    meta = {}
    for line in md_text.split("\n")[:30]:
        m = re.search(r"作物名称[：:]\s*(.+)", line)
        if m:
            meta["crop_name"] = m.group(1).strip()
        m = re.search(r"生成日期[：:]\s*(.+)", line)
        if m:
            meta["date"] = m.group(1).strip()
    return meta


def _md_to_html(md_text: str) -> str:
    """Convert markdown text to HTML."""
    if markdown is None:
        logger.warning("markdown package not available, using basic HTML conversion")
        return _basic_md_to_html(md_text)

    extensions = ["extra", "codehilite", "sane_lists", "toc"]
    return markdown.markdown(md_text, extensions=extensions)


def _basic_md_to_html(md_text: str) -> str:
    """Basic markdown to HTML conversion fallback."""
    html = []
    lines = md_text.split("\n")
    in_list = in_code = False

    for line in lines:
        if line.startswith("```"):
            html.append("</code></pre>" if in_code else "<pre><code>")
            in_code = not in_code
            continue
        if in_code:
            html.append(line)
            continue

        m = re.match(r"^(#{1,3})\s+(.+)$", line)
        if m:
            html.append(f"<h{m.group(1)}>{m.group(2)}</h{m.group(1)}>")
            continue

        if re.match(r"^[\s]*[-*+]\s+", line):
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{re.sub(r'^[\s]*[-*+]\s+', '', line)}</li>")
            continue
        elif in_list:
            html.append("</ul>")
            in_list = False

        if not line.strip():
            continue
        html.append(f"<p>{line}</p>")

    if in_list:
        html.append("</ul>")
    if in_code:
        html.append("</code></pre>")
    return "\n".join(html)


def _load_logo_data_uri() -> str:
    """Load the logo image and return as a base64 data URI."""
    logo_path = Path(__file__).parent / "logo.png"
    if not logo_path.exists():
        return ""
    try:
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f'<img src="data:image/png;base64,{data}" alt="logo">'
    except Exception as e:
        logger.warning(f"Failed to load logo: {e}")
        return ""


def _render_template(body_html: str, cover_meta: dict, report_id: str) -> str:
    """Render the HTML template with content and metadata."""
    template_path = Path(__file__).parent / "report_template.html"
    if not template_path.exists():
        logger.error(f"Report template not found: {template_path}")
        return f"<html><body>{body_html}</body></html>"

    with open(template_path, encoding="utf-8") as f:
        template = f.read()

    date_str = datetime.now().strftime("%Y年%m月%d日")
    logo_data_uri = _load_logo_data_uri()

    replacements = {
        "{{ report_id }}": report_id,
        "{{ date }}": date_str,
        "{% if crop_name %}": "",
        "{{ crop_name }}": cover_meta.get("crop_name", ""),
        "{% endif %}": "",
        "{% if agent_name %}": "",
        "{{ agent_name }}": "千寻有方",
        "{% endif %}": "",
        "{{ logo_data_uri }}": logo_data_uri,
        "{{ body_html }}": body_html,
    }

    result = template
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, str(value))

    # Remove any remaining Jinja template tags
    result = re.sub(r"\{%.*?%\}", "", result)
    result = re.sub(r"\{\{.*?\}\}", "", result)

    return result


def generate_pdf(md_text: str, output_path: str | Path) -> str | None:
    """Generate a PDF from markdown text.

    Args:
        md_text: Markdown content of the report
        output_path: Path to save the PDF file

    Returns:
        The output path if successful, None otherwise
    """
    if HTML is None:
        logger.error("WeasyPrint not available, cannot generate PDF")
        return None

    try:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        report_id = f"CR-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        cover_meta = _parse_cover_meta(md_text)

        # Convert markdown → rendered HTML
        body_html = _md_to_html(md_text)
        full_html = _render_template(body_html, cover_meta, report_id)

        # Generate PDF via WeasyPrint
        HTML(string=full_html).write_pdf(str(output_path))

        logger.info(f"PDF generated successfully: {output_path}")
        return str(output_path)

    except Exception as e:
        logger.error(f"Failed to generate PDF: {e}", exc_info=True)
        return None
