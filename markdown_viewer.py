import streamlit as st
import os
from pathlib import Path
import markdown
from markdown.extensions import codehilite, fenced_code, tables, toc
from streamlit_ace import st_ace
import base64
import tempfile
import time
from ai_service import ai_service
import markdown2
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import re
from html.parser import HTMLParser

def find_markdown_files(directory):
    """Recursively find all markdown files in a directory"""
    markdown_files = []
    if not os.path.exists(directory):
        return markdown_files
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.md', '.markdown')):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, directory)
                markdown_files.append((rel_path, full_path))
    
    return sorted(markdown_files)

def _build_file_tree(markdown_files):
    """Build a nested dict tree from a list of (rel_path, full_path)."""
    tree = {}
    for rel_path, full_path in markdown_files:
        parts = Path(rel_path).parts
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node.setdefault('__files__', []).append((parts[-1], full_path))
    return tree

def _render_file_tree(tree: dict, selected_full_path: str | None = None, base: str = ""):
    """Render a nested file tree with expanders and return clicked file path if any."""
    clicked = None
    # Render directories first
    for dirname in sorted([k for k in tree.keys() if k != '__files__'], key=lambda s: s.lower()):
        with st.expander(f"📁 {dirname}", expanded=False, key=f"dir:{base}{dirname}"):
            child_clicked = _render_file_tree(tree[dirname], selected_full_path, base=f"{base}{dirname}/")
            if child_clicked:
                clicked = child_clicked
    # Render files at this level
    for fname, full_path in sorted(tree.get('__files__', []), key=lambda x: x[0].lower()):
        is_selected = (selected_full_path == full_path)
        button_type = "primary" if is_selected else "secondary"
        if st.button(f"📄 {fname}", key=f"file:{full_path}", use_container_width=True, type=button_type):
            clicked = full_path
    return clicked

def _render_file_tree_v2(tree: dict, selected_full_path: str | None = None, base: str = ""):
    """Render a nested file tree using expanders (no key arg for compatibility).

    Uses unique labels that include the subpath to avoid collisions.
    Returns the clicked file path if any.
    """
    clicked = None
    # Render directories first
    for dirname in sorted([k for k in tree.keys() if k != '__files__'], key=lambda s: s.lower()):
        label = f"📁 {dirname} [{base}{dirname}]" if base else f"📁 {dirname}"
        with st.expander(label, expanded=False):
            child_clicked = _render_file_tree_v2(tree[dirname], selected_full_path, base=f"{base}{dirname}/")
            if child_clicked:
                clicked = child_clicked
    # Render files at this level
    for fname, full_path in sorted(tree.get('__files__', []), key=lambda x: x[0].lower()):
        is_selected = (selected_full_path == full_path)
        button_type = "primary" if is_selected else "secondary"
        if st.button(f"📄 {fname}", key=f"file:{full_path}", use_container_width=True, type=button_type):
            clicked = full_path
    return clicked

def _preprocess_mermaid(md_text: str) -> str:
    """Convert mermaid code fences or graph TB blocks into raw mermaid divs.

    Supports:
    - ```mermaid ... ```
    - ``` (first non-empty line starts with graph/flowchart)
    """
    lines = md_text.split("\n")
    out = []
    i = 0
    in_fence = False
    fence_lang = None
    buf = []

    def is_mermaid_block(text_block: list[str]) -> bool:
        # Find first non-empty content line
        for t in text_block:
            s = t.strip()
            if not s:
                continue
            # Mermaid flowchart keywords
            if s.lower().startswith("graph "):
                return True
            if s.lower().startswith("flowchart "):
                return True
            return False
        return False

    while i < len(lines):
        line = lines[i]
        if not in_fence:
            if line.startswith("```"):
                in_fence = True
                fence_lang = line.strip().lstrip("`").strip()  # capture language after ```
                buf = []
            else:
                out.append(line)
        else:
            # inside fence
            if line.startswith("```"):
                # fence end
                content_lines = buf
                is_mermaid = (fence_lang.lower() == "mermaid") if fence_lang else False
                if not is_mermaid:
                    # Detect graph TB/TD/LR/RL or flowchart
                    is_mermaid = is_mermaid_block(content_lines)

                if is_mermaid:
                    out.append("<div class=\"mermaid\">")
                    out.extend(content_lines)
                    out.append("</div>")
                else:
                    # restore original fenced block
                    fence_header = "```" + (fence_lang if fence_lang else "")
                    out.append(fence_header)
                    out.extend(content_lines)
                    out.append("```")

                in_fence = False
                fence_lang = None
                buf = []
            else:
                buf.append(line)
        i += 1

    # If file ends while still in fence, just flush as original
    if in_fence:
        fence_header = "```" + (fence_lang if fence_lang else "")
        out.append(fence_header)
        out.extend(buf)
        # Do not append closing fence; keep as-is for visibility

    return "\n".join(out)

def render_markdown(content):
    """Render markdown content with extensions for better formatting, incl. Mermaid."""
    # Preprocess to convert Mermaid fences to raw HTML divs so Markdown won't escape them
    content = _preprocess_mermaid(content)

    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.codehilite',
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list'
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'css_class': 'highlight',
                'use_pygments': True,
                'guess_lang': True,
                'noclasses': False
            }
        }
    )
    return md.convert(content)

class MarkdownToPDFConverter:
    """Convert markdown to PDF using ReportLab"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        
    def _setup_styles(self):
        """Setup custom styles for markdown elements"""
        # Heading styles
        self.styles.add(ParagraphStyle(
            name='CustomH1',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomH2',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=10,
            spaceBefore=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomH3',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=8
        ))
        
        # Code block style
        self.styles.add(ParagraphStyle(
            name='CodeBlock',
            parent=self.styles['Code'],
            fontSize=9,
            fontName='Courier',
            backgroundColor=colors.HexColor('#f6f8fa'),
            leftIndent=10,
            rightIndent=10,
            spaceAfter=10,
            spaceBefore=10
        ))
        
        # Regular paragraph
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=8
        ))

    def markdown_to_pdf_elements(self, markdown_text):
        """Convert markdown text to ReportLab elements"""
        elements = []
        
        # Split by lines for processing
        lines = markdown_text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Headers
            if line.startswith('### '):
                elements.append(Paragraph(line[4:], self.styles['CustomH3']))
                elements.append(Spacer(1, 0.1*inch))
            elif line.startswith('## '):
                elements.append(Paragraph(line[3:], self.styles['CustomH2']))
                elements.append(Spacer(1, 0.15*inch))
            elif line.startswith('# '):
                elements.append(Paragraph(line[2:], self.styles['CustomH1']))
                elements.append(Spacer(1, 0.2*inch))
            
            # Code blocks
            elif line.startswith('```'):
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                if code_lines:
                    code_text = '\n'.join(code_lines)
                    # Use Preformatted for code blocks
                    elements.append(Preformatted(code_text, self.styles['CodeBlock']))
                    elements.append(Spacer(1, 0.1*inch))
            
            # Bullet points
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                bullet_text = line.strip()[2:]
                elements.append(Paragraph(f"• {bullet_text}", self.styles['CustomBody']))
            
            # Numbered lists
            elif re.match(r'^\d+\.\s', line.strip()):
                elements.append(Paragraph(line.strip(), self.styles['CustomBody']))
            
            # Regular paragraphs
            elif line.strip():
                # Handle inline code
                line = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', line)
                # Handle bold
                line = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', line)
                line = re.sub(r'__([^_]+)__', r'<b>\1</b>', line)
                # Handle italic
                line = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', line)
                line = re.sub(r'_([^_]+)_', r'<i>\1</i>', line)
                
                elements.append(Paragraph(line, self.styles['CustomBody']))
            
            # Empty lines
            elif not line.strip():
                elements.append(Spacer(1, 0.1*inch))
            
            i += 1
        
        return elements

def export_to_pdf(markdown_content, output_filename):
    """Export markdown content to PDF using ReportLab"""
    try:
        # Create PDF document
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Convert markdown to PDF elements
        converter = MarkdownToPDFConverter()
        elements = converter.markdown_to_pdf_elements(markdown_content)
        
        # Build PDF
        doc.build(elements)
        return True
        
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return False

def resolve_markdown_link(current_file_path, link_href):
    """Resolve a markdown link relative to the current file"""
    current_dir = os.path.dirname(current_file_path)
    
    # Handle relative links
    if not link_href.startswith('/'):
        target_path = os.path.join(current_dir, link_href)
    else:
        target_path = link_href
    
    # Normalize the path
    target_path = os.path.normpath(target_path)
    
    # Check if the file exists and is a markdown file
    if os.path.exists(target_path) and target_path.lower().endswith(('.md', '.markdown')):
        return target_path
    
    return None

def initialize_session_state():
    """Initialize session state variables for editor functionality"""
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    if 'editor_content' not in st.session_state:
        st.session_state.editor_content = ""
    if 'has_unsaved_changes' not in st.session_state:
        st.session_state.has_unsaved_changes = False
    if 'editor_layout' not in st.session_state:
        st.session_state.editor_layout = "inline"  # inline, side-by-side, tabbed
    if 'original_content' not in st.session_state:
        st.session_state.original_content = ""
    if 'confirm_save' not in st.session_state:
        st.session_state.confirm_save = False
    
    # AI summarization session state
    if 'ai_summary' not in st.session_state:
        st.session_state.ai_summary = ""
    if 'ai_summary_template' not in st.session_state:
        st.session_state.ai_summary_template = "high_level"
    if 'ai_generating' not in st.session_state:
        st.session_state.ai_generating = False
    if 'ai_last_template_used' not in st.session_state:
        st.session_state.ai_last_template_used = ""
    if 'ai_summary_tokens' not in st.session_state:
        st.session_state.ai_summary_tokens = None
    if 'ai_summary_layout' not in st.session_state:
        st.session_state.ai_summary_layout = "sidebar"  # sidebar, side-by-side, tabbed

def toggle_edit_mode():
    """Toggle between view and edit modes"""
    st.session_state.edit_mode = not st.session_state.edit_mode
    # Reset confirmation state when toggling modes
    st.session_state.confirm_save = False
    
def save_file_content(content, filename):
    """Create a download link for the modified content"""
    b64 = base64.b64encode(content.encode()).decode()
    href = f'data:text/markdown;base64,{b64}'
    return href

def save_file_directly(file_path, content):
    """Save content directly to the file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True, "File saved successfully!"
    except Exception as e:
        return False, f"Error saving file: {str(e)}"

def get_ai_summary_folder():
    """Get or create the AISummary folder in the current project directory"""
    if 'last_folder_path' not in st.session_state:
        return None, "No folder selected"
    
    base_folder = st.session_state.last_folder_path
    if not base_folder or not os.path.exists(base_folder):
        return None, "Invalid project folder path"
    
    summary_folder = os.path.join(base_folder, "AISummary")
    
    try:
        # Create the folder if it doesn't exist
        if not os.path.exists(summary_folder):
            os.makedirs(summary_folder)
        return summary_folder, "AISummary folder ready"
    except Exception as e:
        return None, f"Error creating AISummary folder: {str(e)}"

def save_ai_summary_to_project(summary_content, base_filename, template_name):
    """Save AI summary to the project's AISummary folder"""
    summary_folder, message = get_ai_summary_folder()
    if not summary_folder:
        return False, message
    
    # Create a descriptive filename
    safe_template = template_name.replace(" ", "_").lower()
    safe_filename = base_filename.replace(".md", "").replace(".markdown", "")
    summary_filename = f"{safe_filename}_{safe_template}_summary.md"
    full_path = os.path.join(summary_folder, summary_filename)
    
    try:
        with open(full_path, 'w', encoding='utf-8') as file:
            # Add metadata header to the summary
            file.write(f"# AI Summary: {base_filename}\n\n")
            file.write(f"**Template**: {template_name}  \n")
            file.write(f"**Generated**: {time.strftime('%Y-%m-%d %H:%M:%S')}  \n")
            file.write(f"**Source**: {base_filename}  \n\n")
            file.write("---\n\n")
            file.write(summary_content)
        
        return True, f"Summary saved to: AISummary/{summary_filename}"
    except Exception as e:
        return False, f"Error saving summary: {str(e)}"

def check_unsaved_changes():
    """Check if there are unsaved changes"""
    if hasattr(st.session_state, 'editor_content') and hasattr(st.session_state, 'original_content'):
        return st.session_state.editor_content != st.session_state.original_content
    return False

def render_markdown_component(html_content, selected_file_path):
    """Render the markdown HTML component"""
    import streamlit.components.v1 as components
    
    # Get the base directory for resolving relative links
    base_dir = os.path.dirname(selected_file_path)
    
    full_html = f'''
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
    <style>
        .markdown-content {{
            line-height: 1.6;
            font-size: 16px;
            color: #333;
        }}
        .markdown-content h1, .markdown-content h2, .markdown-content h3 {{
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            color: #1f2937;
        }}
        .markdown-content pre {{
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 1rem;
            overflow-x: auto;
            margin: 1em 0;
        }}
        .markdown-content code {{
            background-color: #f8f9fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-size: 0.9em;
            font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
        }}
        .markdown-content pre code {{
            background: transparent;
            padding: 0;
        }}
        .markdown-content table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}
        .markdown-content th, .markdown-content td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        .markdown-content th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .highlight {{
            background-color: #f6f8fa;
            border-radius: 6px;
            margin: 1em 0;
            border: 1px solid #d1d9e0;
        }}
        .highlight pre {{
            margin: 0;
            background: transparent;
            border: none;
        }}
        
        /* Syntax highlighting colors - GitHub style */
        .highlight .k {{ color: #d73a49; font-weight: bold; }} /* Keywords */
        .highlight .kd {{ color: #d73a49; font-weight: bold; }} /* Keyword declarations */
        .highlight .kt {{ color: #d73a49; font-weight: bold; }} /* Keyword types */
        .highlight .s {{ color: #032f62; }} /* Strings */
        .highlight .s1 {{ color: #032f62; }} /* Single quoted strings */
        .highlight .s2 {{ color: #032f62; }} /* Double quoted strings */
        .highlight .sb {{ color: #032f62; }} /* Backtick strings */
        .highlight .sc {{ color: #032f62; }} /* String chars */
        .highlight .sd {{ color: #032f62; }} /* String docs */
        .highlight .se {{ color: #032f62; }} /* String escapes */
        .highlight .sh {{ color: #032f62; }} /* String heredoc */
        .highlight .si {{ color: #032f62; }} /* String interpolated */
        .highlight .sx {{ color: #032f62; }} /* String other */
        .highlight .sr {{ color: #032f62; }} /* String regex */
        .highlight .ss {{ color: #032f62; }} /* String symbol */
        .highlight .c {{ color: #6a737d; font-style: italic; }} /* Comments */
        .highlight .c1 {{ color: #6a737d; font-style: italic; }} /* Single line comments */
        .highlight .cm {{ color: #6a737d; font-style: italic; }} /* Multi-line comments */
        .highlight .cp {{ color: #6a737d; font-style: italic; }} /* Preprocessor comments */
        .highlight .cs {{ color: #6a737d; font-style: italic; }} /* Comment special */
        .highlight .n {{ color: #24292e; }} /* Names */
        .highlight .na {{ color: #6f42c1; }} /* Name attributes */
        .highlight .nb {{ color: #005cc5; }} /* Name builtins */
        .highlight .nc {{ color: #6f42c1; }} /* Name class */
        .highlight .nd {{ color: #6f42c1; }} /* Name decorator */
        .highlight .ne {{ color: #6f42c1; }} /* Name exception */
        .highlight .nf {{ color: #6f42c1; }} /* Name function */
        .highlight .ni {{ color: #005cc5; }} /* Name entity */
        .highlight .nl {{ color: #005cc5; }} /* Name label */
        .highlight .nn {{ color: #6f42c1; }} /* Name namespace */
        .highlight .no {{ color: #005cc5; }} /* Name constant */
        .highlight .nt {{ color: #22863a; }} /* Name tag */
        .highlight .nv {{ color: #e36209; }} /* Name variable */
        .highlight .nx {{ color: #24292e; }} /* Name other */
        .highlight .o {{ color: #d73a49; }} /* Operators */
        .highlight .ow {{ color: #d73a49; }} /* Operator word */
        .highlight .p {{ color: #24292e; }} /* Punctuation */
        .highlight .m {{ color: #005cc5; }} /* Numbers */
        .highlight .mf {{ color: #005cc5; }} /* Float */
        .highlight .mh {{ color: #005cc5; }} /* Hex */
        .highlight .mi {{ color: #005cc5; }} /* Integer */
        .highlight .mo {{ color: #005cc5; }} /* Octal */
        .highlight .mb {{ color: #005cc5; }} /* Binary */
        .highlight .il {{ color: #005cc5; }} /* Integer long */
        .highlight .err {{ color: #cb2431; background-color: #ffeef0; }} /* Errors */
        .highlight .gh {{ color: #005cc5; font-weight: bold; }} /* Generic heading */
        .highlight .gi {{ color: #22863a; background-color: #f0fff4; }} /* Generic inserted */
        .highlight .gd {{ color: #cb2431; background-color: #ffeef0; }} /* Generic deleted */
        .highlight .ge {{ font-style: italic; }} /* Generic emphasis */
        .highlight .gr {{ color: #cb2431; }} /* Generic error */
        .highlight .gs {{ font-weight: bold; }} /* Generic strong */
        .highlight .gu {{ color: #6f42c1; font-weight: bold; }} /* Generic subheading */
        .highlight .w {{ color: #24292e; }} /* Whitespace */
    </style>
    <!-- Mermaid JS for diagrams -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        if (window.mermaid) {{
            try {{
                mermaid.initialize({{ startOnLoad: true, securityLevel: 'loose' }});
            }} catch (e) {{
                console.error('Mermaid init error', e);
            }}
        }}
    </script>
    <script>
        // Debug function to log messages
        function debugLog(message) {{
            console.log('[Markdown Viewer Debug]', message);
        }}

        document.addEventListener('DOMContentLoaded', function() {{
            debugLog('DOM loaded, setting up link listeners');
            // Initialize Mermaid on load (in case dynamic content)
            try {{
                if (window.mermaid) {{
                    mermaid.init(undefined, document.querySelectorAll('.mermaid'));
                }}
            }} catch (e) {{
                console.error('Mermaid run error', e);
            }}
            
            // Intercept clicks on links
            document.addEventListener('click', function(e) {{
                debugLog('Click detected on:', e.target.tagName, e.target.href);
                
                if (e.target.tagName === 'A') {{
                    const href = e.target.getAttribute('href');
                    debugLog('Link href:', href);
                    
                    // Check if it's a local markdown file link
                    if (href && !href.startsWith('http://') && !href.startsWith('https://') && !href.startsWith('#')) {{
                        debugLog('Local link detected:', href);
                        
                        // Check if it's a markdown file
                        if (href.toLowerCase().endsWith('.md') || href.toLowerCase().endsWith('.markdown')) {{
                            debugLog('Markdown file link - preventing default and sending to Streamlit');
                            e.preventDefault();
                            
                            // Try multiple communication methods
                            const linkData = {{
                                action: 'navigate_to_file',
                                href: href,
                                baseDir: '{base_dir.replace(os.sep, "/")}'
                            }};
                            
                            // Method 1: Streamlit component communication
                            try {{
                                window.parent.postMessage({{
                                    type: "streamlit:setComponentValue",
                                    value: linkData
                                }}, "*");
                                debugLog('Sent via postMessage method 1');
                            }} catch (e1) {{
                                debugLog('Method 1 failed:', e1);
                            }}
                            
                            // Method 2: Try different postMessage format
                            try {{
                                window.parent.postMessage(linkData, "*");
                                debugLog('Sent via postMessage method 2');
                            }} catch (e2) {{
                                debugLog('Method 2 failed:', e2);
                            }}
                            
                            // Method 3: Store in localStorage and trigger custom event
                            try {{
                                localStorage.setItem('markdown_navigation', JSON.stringify(linkData));
                                window.dispatchEvent(new CustomEvent('markdown_link_clicked', {{ detail: linkData }}));
                                debugLog('Stored in localStorage and triggered event');
                            }} catch (e3) {{
                                debugLog('Method 3 failed:', e3);
                            }}
                            
                            // Method 4: URL navigation fallback
                            setTimeout(function() {{
                                try {{
                                    // Resolve the full path
                                    let targetPath = href;
                                    if (!href.startsWith('/')) {{
                                        targetPath = '{base_dir.replace(os.sep, "/").replace(os.sep, "/")}/' + href;
                                    }}
                                    
                            // Navigate using URL parameters
                                    const currentUrl = new URL(window.parent.location);
                                    currentUrl.searchParams.set('navigate_to', targetPath.replace(/\\//g, '\\\\\\\\'));
                                    window.parent.location.href = currentUrl.toString();
                                    debugLog('Attempting URL navigation to:', targetPath);
                                }} catch (e4) {{
                                    debugLog('Method 4 failed:', e4);
                                }}
                            }}, 100);
                        }} else {{
                            debugLog('Not a markdown file:', href);
                        }}
                    }} else {{
                        debugLog('External or anchor link, allowing default behavior:', href);
                    }}
                }}
            }});
            
            debugLog('Link listener setup complete');
        }});
    </script>
    <div class="markdown-content">
        {html_content}
    </div>
</div>
'''
    
    # Create an interactive component that can communicate back to Streamlit
    # Increased height to prevent content cutoff at bottom
    clicked_link = components.html(
        full_html,
        height=1000,  # Increased from 800 to 1000
        scrolling=True
    )
    
    return clicked_link

def render_editor_toolbar():
    """Render the editor toolbar with formatting buttons"""
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 2])
    
    with col1:
        if st.button("**B**", help="Bold text", key="bold_btn"):
            st.session_state.editor_insert = "**bold text**"
    with col2:
        if st.button("*I*", help="Italic text", key="italic_btn"):
            st.session_state.editor_insert = "*italic text*"
    with col3:
        if st.button("H1", help="Header 1", key="h1_btn"):
            st.session_state.editor_insert = "# Header 1"
    with col4:
        if st.button("H2", help="Header 2", key="h2_btn"):
            st.session_state.editor_insert = "## Header 2"
    with col5:
        if st.button("[](", help="Link", key="link_btn"):
            st.session_state.editor_insert = "[link text](url)"
    with col6:
        if st.button("`", help="Code", key="code_btn"):
            st.session_state.editor_insert = "`code`"
    with col7:
        if st.button("📋 Copy", help="Copy content to clipboard", key="copy_btn"):
            st.code(st.session_state.editor_content)

def main():
    st.set_page_config(
        page_title="Markdown Manager",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Check for navigation via URL parameters
    query_params = st.query_params
    if 'navigate_to' in query_params:
        nav_file = query_params['navigate_to']
        if os.path.exists(nav_file) and nav_file.lower().endswith(('.md', '.markdown')):
            st.session_state.selected_file = nav_file
            st.session_state.file_name = os.path.basename(nav_file)
            st.session_state.last_selected_file = nav_file
            st.session_state.last_folder_path = os.path.dirname(nav_file)
            # Update URL to remember the folder but clear navigate_to
            st.query_params.update({"folder": os.path.dirname(nav_file)})
            if 'navigate_to' in st.query_params:
                del st.query_params['navigate_to']
            st.rerun()
    
    # Custom CSS to reduce top padding
    st.markdown("""
    <style>
    .stMainBlockContainer.block-container.st-emotion-cache-zy6yx3.e4man114 {
        padding-top: 1.25rem !important;
    }
    
    /* Alternative selectors in case the class names change */
    .stMainBlockContainer {
        padding-top: 1.25rem !important;
    }
    
    .block-container {
        padding-top: 1.25rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("⚡ Markdown Manager")
    
    # Sidebar with file selection
    with st.sidebar:
        # File uploader for markdown files
        uploaded_file = st.file_uploader(
            "Choose a markdown file",
            type=['md', 'markdown'],
            help="Upload a .md or .markdown file to view"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily and display it
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.md', delete=False) as tmp_file:
                content = uploaded_file.getvalue().decode('utf-8')
                tmp_file.write(content)
                tmp_file.flush()
                st.session_state.selected_file = tmp_file.name
                st.session_state.file_name = uploaded_file.name
        
        st.divider()
        
        # Alternative: Browse local files (folder path input)
        st.subheader("Or browse local folder")
        if st.button("🔄 Refresh", help="Refresh file list", use_container_width=True):
            st.rerun()
        
        # Initialize folder path with persistent storage using query params
        # Check if there's a stored folder path in the URL or use current working directory
        if 'last_folder_path' not in st.session_state:
            # Try to get folder from URL parameters first
            query_params = st.query_params
            stored_folder = query_params.get('folder', '')
            if stored_folder and os.path.exists(stored_folder) and os.path.isdir(stored_folder):
                st.session_state.last_folder_path = stored_folder
            else:
                st.session_state.last_folder_path = os.getcwd()
            
        folder_path = st.text_input(
            "Enter folder path:",
            value=st.session_state.last_folder_path,
            help="Enter the path to browse markdown files from your local system",
            key="folder_path_input"
        )
        
        # Update session state and URL when folder path changes
        if folder_path != st.session_state.last_folder_path:
            st.session_state.last_folder_path = folder_path
            # Store folder path in URL for persistence across refreshes
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                st.query_params.update({"folder": folder_path})
        
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Find markdown files
            markdown_files = find_markdown_files(folder_path)
            
            if markdown_files:
                st.write(f"📄 Found {len(markdown_files)} files:")
                
                # Tree view instead of flat list
                file_tree = _build_file_tree(markdown_files)
                selected_file = _render_file_tree_v2(
                    file_tree,
                    selected_full_path=st.session_state.get('selected_file'),
                    base=""
                )
                if selected_file:
                    st.session_state.file_name = os.path.basename(selected_file)
                    st.session_state.last_selected_file = selected_file  # Remember for refresh
                
                # Store selected file in session state
                if selected_file:
                    # Reset AI summary when selecting new file
                    if selected_file != st.session_state.get('selected_file'):
                        st.session_state.ai_summary = ""
                        st.session_state.ai_last_template_used = ""
                        st.session_state.ai_summary_tokens = None
                        st.session_state.ai_generating = False
                    
                    st.session_state.selected_file = selected_file
                    
                # Auto-reload last selected file if it still exists in current folder
                elif ('last_selected_file' in st.session_state and 
                      st.session_state.last_selected_file in [full_path for _, full_path in markdown_files] and
                      'selected_file' not in st.session_state):
                    st.session_state.selected_file = st.session_state.last_selected_file
                    st.session_state.file_name = os.path.basename(st.session_state.last_selected_file)
            else:
                st.info("No markdown files found in this folder")
        elif folder_path:
            st.error("Invalid folder path")
        
        # Editor controls in sidebar (always show for demonstration)
        if True:  # Temporarily always show editor controls
            st.divider()
            st.subheader("✏️ Editor Controls")
            
            # Edit mode toggle
            edit_btn_text = "📝 Exit Edit Mode" if st.session_state.edit_mode else "✏️ Edit File"
            if st.button(edit_btn_text, use_container_width=True, type="primary" if st.session_state.edit_mode else "secondary"):
                if st.session_state.edit_mode and check_unsaved_changes():
                    st.warning("⚠️ You have unsaved changes! Please save or they will be lost.")
                toggle_edit_mode()
                st.rerun()
            
            # Export to PDF button (only show when viewing a file)
            if 'selected_file' in st.session_state and st.session_state.selected_file and not st.session_state.edit_mode:
                if st.button("📄 Export to PDF", use_container_width=True, type="secondary"):
                    try:
                        # Read the markdown file content
                        with open(st.session_state.selected_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Generate PDF filename based on markdown filename
                        base_name = os.path.splitext(os.path.basename(st.session_state.selected_file))[0]
                        pdf_filename = f"{base_name}.pdf"
                        
                        # Create a temporary file for the PDF
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                            tmp_filename = tmp_file.name
                        
                        # Export to PDF
                        if export_to_pdf(content, tmp_filename):
                            # Read the PDF file
                            with open(tmp_filename, 'rb') as pdf_file:
                                pdf_data = pdf_file.read()
                            
                            # Clean up temp file
                            os.unlink(tmp_filename)
                            
                            # Offer download
                            st.download_button(
                                label="⬇️ Download PDF",
                                data=pdf_data,
                                file_name=pdf_filename,
                                mime="application/pdf",
                                use_container_width=True
                            )
                            st.success(f"✅ PDF generated successfully!")
                    except Exception as e:
                        st.error(f"❌ Error exporting to PDF: {str(e)}")
            
            # Layout options (only show in edit mode)
            if st.session_state.edit_mode:
                st.session_state.editor_layout = st.radio(
                    "Layout:",
                    ["inline", "side-by-side", "tabbed"],
                    index=["inline", "side-by-side", "tabbed"].index(st.session_state.editor_layout),
                    help="Choose how to display editor and preview"
                )
                
                # Unsaved changes indicator
                if check_unsaved_changes():
                    st.warning("⚠️ Unsaved changes")
                else:
                    st.success("✅ No unsaved changes")
                
                # Save buttons
                if check_unsaved_changes():
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Save directly to file (only for non-temporary files)
                        file_path = st.session_state.get('selected_file', '')
                        is_temp_file = file_path.endswith('.tmp') or 'temp' in file_path.lower()
                        
                        if not st.session_state.confirm_save:
                            if st.button("💾 Save File", use_container_width=True, disabled=is_temp_file, 
                                       help="Save changes directly to the original file" if not is_temp_file else "Cannot save temporary uploaded files directly"):
                                if not is_temp_file:
                                    st.session_state.confirm_save = True
                                    st.rerun()
                        else:
                            st.warning("⚠️ This will overwrite the original file. Are you sure?")
                            col_yes, col_no = st.columns(2)
                            with col_yes:
                                if st.button("✅ Yes, Save", use_container_width=True):
                                    success, message = save_file_directly(file_path, st.session_state.editor_content)
                                    if success:
                                        st.success(message)
                                        # Update original content to reflect saved state
                                        st.session_state.original_content = st.session_state.editor_content
                                        st.session_state.confirm_save = False
                                        st.rerun()
                                    else:
                                        st.error(message)
                                        st.session_state.confirm_save = False
                            with col_no:
                                if st.button("❌ Cancel", use_container_width=True):
                                    st.session_state.confirm_save = False
                                    st.rerun()
                    
                    with col2:
                        # Download option (always available)
                        if st.button("📥 Download", use_container_width=True, help="Download modified file"):
                            if st.session_state.editor_content:
                                filename = st.session_state.get('file_name', 'edited_file.md')
                                st.download_button(
                                    label="📥 Download Modified File",
                                    data=st.session_state.editor_content,
                                    file_name=filename,
                                    mime="text/markdown",
                                    use_container_width=True
                                )
                else:
                    st.info("💾 No changes to save")
        
        # AI Summarization section
        if 'selected_file' in st.session_state and os.path.exists(st.session_state.selected_file):
            st.divider()
            st.subheader("🤖 AI Summary")
            
            # Check AI service configuration
            if not ai_service.is_configured():
                st.error("⚠️ AI service not configured. Please check your Azure OpenAI credentials in .env file.")
            else:
                # Template selector
                templates = ai_service.get_prompt_templates()
                template_options = {key: data['name'] for key, data in templates.items()}
                
                selected_template_key = st.selectbox(
                    "Choose summary type:",
                    options=list(template_options.keys()),
                    format_func=lambda x: template_options[x],
                    index=list(template_options.keys()).index(st.session_state.ai_summary_template),
                    help="Select the type of summary you want to generate",
                    key="ai_template_selector"
                )
                
                # Update session state when template changes
                if selected_template_key != st.session_state.ai_summary_template:
                    st.session_state.ai_summary_template = selected_template_key
                
                # Show template description
                template_info = templates[selected_template_key]
                st.caption(f"📝 {template_info['description']}")
                
                # Layout selector (only show when there's a summary)
                if st.session_state.ai_summary:
                    st.session_state.ai_summary_layout = st.radio(
                        "Display layout:",
                        ["sidebar", "side-by-side", "tabbed"],
                        index=["sidebar", "side-by-side", "tabbed"].index(st.session_state.ai_summary_layout),
                        help="Choose how to display the summary",
                        horizontal=True
                    )
                
                # Generate button
                generate_disabled = st.session_state.ai_generating
                generate_text = "🔄 Generating..." if st.session_state.ai_generating else "✨ Generate Summary"
                
                if st.button(generate_text, disabled=generate_disabled, use_container_width=True, type="primary"):
                    # Read current file content
                    try:
                        with open(st.session_state.selected_file, 'r', encoding='utf-8') as file:
                            file_content = file.read()
                        
                        # Validate content size
                        validation = ai_service.validate_content_size(file_content)
                        if not validation['valid']:
                            st.error(validation['message'])
                        else:
                            # Generate summary
                            st.session_state.ai_generating = True
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error reading file: {str(e)}")
                
                # Handle the actual generation (runs when ai_generating is True)
                if st.session_state.ai_generating:
                    try:
                        with open(st.session_state.selected_file, 'r', encoding='utf-8') as file:
                            file_content = file.read()
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        def progress_callback(message):
                            status_text.text(message)
                            progress_bar.progress(0.5)
                        
                        progress_callback("Generating summary...")
                        result = ai_service.generate_summary(file_content, selected_template_key, progress_callback)
                        
                        progress_bar.progress(1.0)
                        status_text.text("Summary generated!")
                        
                        if result['success']:
                            st.session_state.ai_summary = result['summary']
                            st.session_state.ai_last_template_used = result['template_name']
                            st.session_state.ai_summary_tokens = result.get('tokens_used')
                            st.success(f"✅ Summary generated successfully!")
                            if result.get('tokens_used'):
                                st.caption(f"Tokens used: {result['tokens_used']}")
                        else:
                            st.error(f"❌ {result['error']}")
                        
                        st.session_state.ai_generating = False
                        progress_bar.empty()
                        status_text.empty()
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
                        st.session_state.ai_generating = False
                        st.rerun()
                
                # Display existing summary in sidebar (only for sidebar layout)
                if (st.session_state.ai_summary and 
                    not st.session_state.ai_generating and 
                    st.session_state.ai_summary_layout == "sidebar"):
                    
                    st.subheader("📄 Summary")
                    if st.session_state.ai_last_template_used:
                        st.caption(f"Generated using: {st.session_state.ai_last_template_used}")
                    
                    # Summary content in an expandable container
                    with st.expander("View Summary", expanded=True):
                        st.markdown(st.session_state.ai_summary)
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Copy button (using st.code for easy copying)
                        if st.button("📋 Copy Summary", use_container_width=True, key="sidebar_copy"):
                            st.code(st.session_state.ai_summary, language=None)
                            st.success("Summary copied to view! Use Ctrl+A, Ctrl+C to copy.")
                    
                    with col2:
                        # Save to project button
                        if st.button("💾 Save to Project", use_container_width=True, key="sidebar_save"):
                            success, message = save_ai_summary_to_project(
                                st.session_state.ai_summary,
                                st.session_state.get('file_name', 'document'),
                                st.session_state.ai_last_template_used
                            )
                            if success:
                                st.success(message)
                            else:
                                st.error(message)
                
                # Show info for other layouts
                elif (st.session_state.ai_summary and 
                      not st.session_state.ai_generating and 
                      st.session_state.ai_summary_layout != "sidebar"):
                    st.info(f"📄 Summary available in {st.session_state.ai_summary_layout} layout below")
                    if st.session_state.ai_last_template_used:
                        st.caption(f"Generated using: {st.session_state.ai_last_template_used}")
                    
                    # Save to project button for convenience
                    if st.button("💾 Save to Project", use_container_width=True, key="sidebar_save_alt"):
                        success, message = save_ai_summary_to_project(
                            st.session_state.ai_summary,
                            st.session_state.get('file_name', 'document'),
                            st.session_state.ai_last_template_used
                        )
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
    
    # Main content area
    if 'selected_file' in st.session_state and os.path.exists(st.session_state.selected_file):
        selected_file_path = st.session_state.selected_file
        
        # Display file info
        if 'file_name' in st.session_state:
            file_name = st.session_state.file_name
        else:
            file_name = os.path.basename(selected_file_path)
        
        st.subheader(f"📄 {file_name}")
        if not file_name.endswith('.tmp'):
            st.caption(f"Path: {selected_file_path}")
        
        # Read and render markdown content
        try:
            with open(selected_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Store original content for comparison
            if not st.session_state.edit_mode or st.session_state.original_content == "":
                st.session_state.original_content = content
                if not st.session_state.edit_mode:
                    st.session_state.editor_content = content
            
            if content.strip():
                # Handle different layouts based on edit mode
                if st.session_state.edit_mode:
                    if st.session_state.editor_layout == "inline":
                        # Show only editor
                        st.subheader("✏️ Editing Mode")
                        render_editor_toolbar()
                        
                        # Editor component
                        edited_content = st_ace(
                            value=st.session_state.editor_content,
                            language='markdown',
                            theme='github',
                            key='markdown_editor',
                            height=600,
                            auto_update=True,
                            font_size=14,
                            tab_size=2,
                            wrap=True,
                            annotations=None,
                            markers=None,
                        )
                        
                        # Update editor content and check for changes
                        if edited_content != st.session_state.editor_content:
                            st.session_state.editor_content = edited_content
                            st.session_state.has_unsaved_changes = check_unsaved_changes()
                            st.rerun()
                    
                    elif st.session_state.editor_layout == "side-by-side":
                        # Show editor and preview side by side
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("✏️ Editor")
                            render_editor_toolbar()
                            
                            edited_content = st_ace(
                                value=st.session_state.editor_content,
                                language='markdown',
                                theme='github',
                                key='markdown_editor_sidebyside',
                                height=600,
                                auto_update=True,
                                font_size=14,
                                tab_size=2,
                                wrap=True
                            )
                            
                            if edited_content != st.session_state.editor_content:
                                st.session_state.editor_content = edited_content
                                st.session_state.has_unsaved_changes = check_unsaved_changes()
                                st.rerun()
                        
                        with col2:
                            st.subheader("👁️ Live Preview")
                            preview_content = render_markdown(st.session_state.editor_content)
                            # Use the HTML component so Mermaid and link handling work in preview
                            _ = render_markdown_component(preview_content, selected_file_path)
                    
                    elif st.session_state.editor_layout == "tabbed":
                        # Show tabs for editor and preview
                        tab1, tab2 = st.tabs(["✏️ Editor", "👁️ Preview"])
                        
                        with tab1:
                            render_editor_toolbar()
                            
                            edited_content = st_ace(
                                value=st.session_state.editor_content,
                                language='markdown',
                                theme='github',
                                key='markdown_editor_tabbed',
                                height=600,
                                auto_update=True,
                                font_size=14,
                                tab_size=2,
                                wrap=True
                            )
                            
                            if edited_content != st.session_state.editor_content:
                                st.session_state.editor_content = edited_content
                                st.session_state.has_unsaved_changes = check_unsaved_changes()
                                st.rerun()
                        
                        with tab2:
                            preview_content = render_markdown(st.session_state.editor_content)
                            _ = render_markdown_component(preview_content, selected_file_path)
                
                else:
                    # View mode - show rendered markdown with AI summary layouts
                    html_content = render_markdown(content)
                    
                    # Check if we need to display in special layout with AI summary
                    has_summary = (st.session_state.ai_summary and 
                                 not st.session_state.ai_generating and
                                 st.session_state.ai_summary_layout != "sidebar")
                    
                    if has_summary and st.session_state.ai_summary_layout == "side-by-side":
                        # Side-by-side layout: markdown on left, summary on right
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📄 Document")
                            # Display the rendered markdown using HTML component
                            clicked_link = render_markdown_component(html_content, selected_file_path)
                        
                        with col2:
                            st.subheader("🤖 AI Summary")
                            if st.session_state.ai_last_template_used:
                                st.caption(f"Generated using: {st.session_state.ai_last_template_used}")
                            
                            # Summary content
                            st.markdown(st.session_state.ai_summary)
                            
                            # Action buttons
                            col_copy, col_download = st.columns(2)
                            with col_copy:
                                if st.button("📋 Copy", use_container_width=True, key="main_copy"):
                                    st.code(st.session_state.ai_summary, language=None)
                                    st.success("Summary ready to copy!")
                            
                            with col_download:
                                if st.button("💾 Save to Project", use_container_width=True, key="main_save"):
                                    success, message = save_ai_summary_to_project(
                                        st.session_state.ai_summary,
                                        st.session_state.get('file_name', 'document'),
                                        st.session_state.ai_last_template_used
                                    )
                                    if success:
                                        st.success(message)
                                    else:
                                        st.error(message)
                    
                    elif has_summary and st.session_state.ai_summary_layout == "tabbed":
                        # Tabbed layout: tabs for markdown and summary
                        tab1, tab2 = st.tabs(["📄 Document", "🤖 AI Summary"])
                        
                        with tab1:
                            # Display the rendered markdown using HTML component
                            clicked_link = render_markdown_component(html_content, selected_file_path)
                        
                        with tab2:
                            if st.session_state.ai_last_template_used:
                                st.caption(f"Generated using: {st.session_state.ai_last_template_used}")
                            
                            # Summary content
                            st.markdown(st.session_state.ai_summary)
                            
                            # Action buttons
                            col_copy, col_download = st.columns(2)
                            with col_copy:
                                if st.button("📋 Copy Summary", use_container_width=True, key="tab_copy"):
                                    st.code(st.session_state.ai_summary, language=None)
                                    st.success("Summary ready to copy!")
                            
                            with col_download:
                                if st.button("💾 Save to Project", use_container_width=True, key="tab_save"):
                                    success, message = save_ai_summary_to_project(
                                        st.session_state.ai_summary,
                                        st.session_state.get('file_name', 'document'),
                                        st.session_state.ai_last_template_used
                                    )
                                    if success:
                                        st.success(message)
                                    else:
                                        st.error(message)
                    
                    else:
                        # Default layout (sidebar or no summary)
                        # Display the rendered markdown using HTML component
                        clicked_link = render_markdown_component(html_content, selected_file_path)

                    # Debug toggle in sidebar
                    show_debug = st.sidebar.checkbox("🐛 Show Debug Info", value=False, help="Show debugging information for link navigation")
                    
                    # Debug: Show component return value
                    if show_debug and clicked_link:
                        st.sidebar.write("**Debug - Component returned:**", clicked_link)
                    
                    # Handle link navigation (works for all layouts since clicked_link is always set)
                    if clicked_link and isinstance(clicked_link, dict) and clicked_link.get('action') == 'navigate_to_file':
                        href = clicked_link.get('href')
                        base_dir = clicked_link.get('baseDir', '').replace('/', os.sep)
                        
                        if show_debug:
                            st.sidebar.write(f"**Debug - Navigating to:** {href}")
                            st.sidebar.write(f"**Debug - Base dir:** {base_dir}")
                        
                        if href:
                            # Resolve the target file path
                            target_path = resolve_markdown_link(selected_file_path, href)
                            
                            if show_debug:
                                st.sidebar.write(f"**Debug - Resolved path:** {target_path}")
                            
                            if target_path and os.path.exists(target_path):
                                if show_debug:
                                    st.sidebar.success(f"**Debug - File found, navigating to:** {target_path}")
                                
                                # Update session state to navigate to the new file
                                st.session_state.selected_file = target_path
                                st.session_state.file_name = os.path.basename(target_path)
                                st.session_state.last_selected_file = target_path
                                
                                # Reset editor state when navigating to new file
                                st.session_state.edit_mode = False
                                st.session_state.editor_content = ""
                                st.session_state.original_content = ""
                                st.session_state.has_unsaved_changes = False
                                st.session_state.confirm_save = False
                                
                                # Reset AI summary state when navigating to new file
                                st.session_state.ai_summary = ""
                                st.session_state.ai_last_template_used = ""
                                st.session_state.ai_summary_tokens = None
                                st.session_state.ai_generating = False
                                
                                # Update the folder path to the new file's directory if needed
                                new_dir = os.path.dirname(target_path)
                                if new_dir != st.session_state.get('last_folder_path'):
                                    st.session_state.last_folder_path = new_dir
                                
                                # Rerun to update the display
                                st.rerun()
                            else:
                                st.error(f"Could not find markdown file: {href}")
                                st.info(f"Attempted path: {target_path if target_path else 'Could not resolve'}")
            else:
                st.info("This file is empty.")
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    else:
        st.info("👈 Select a markdown file from the sidebar to view its contents.")

if __name__ == "__main__":
    main()
