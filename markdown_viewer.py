import streamlit as st
import os
from pathlib import Path
import markdown
from markdown.extensions import codehilite, fenced_code, tables, toc

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

def render_markdown(content):
    """Render markdown content with extensions for better formatting"""
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

def main():
    st.set_page_config(
        page_title="Markdown Viewer",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Check for navigation via URL parameters
    query_params = st.query_params
    if 'navigate_to' in query_params:
        nav_file = query_params['navigate_to']
        if os.path.exists(nav_file) and nav_file.lower().endswith(('.md', '.markdown')):
            st.session_state.selected_file = nav_file
            st.session_state.file_name = os.path.basename(nav_file)
            st.session_state.last_selected_file = nav_file
            st.session_state.last_folder_path = os.path.dirname(nav_file)
            # Clear the query parameter
            st.query_params.clear()
            st.rerun()
    
    st.title("📄 Markdown File Viewer")
    
    # Sidebar with file selection
    with st.sidebar:
        st.header("📁 Select Markdown File")
        
        # File uploader for markdown files
        uploaded_file = st.file_uploader(
            "Choose a markdown file",
            type=['md', 'markdown'],
            help="Upload a .md or .markdown file to view"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily and display it
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.md', delete=False) as tmp_file:
                content = uploaded_file.getvalue().decode('utf-8')
                tmp_file.write(content)
                tmp_file.flush()
                st.session_state.selected_file = tmp_file.name
                st.session_state.file_name = uploaded_file.name
        
        st.divider()
        
        # Alternative: Browse local files (folder path input)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Or browse local folder")
        with col2:
            if st.button("🔄 Refresh", help="Refresh file list", use_container_width=True):
                st.rerun()
        
        # Initialize folder path in session state if not exists
        if 'last_folder_path' not in st.session_state:
            st.session_state.last_folder_path = os.getcwd()
            
        folder_path = st.text_input(
            "Enter folder path:",
            value=st.session_state.last_folder_path,
            help="Enter the path to browse markdown files from your local system",
            key="folder_path_input"
        )
        
        # Update session state when folder path changes
        if folder_path != st.session_state.last_folder_path:
            st.session_state.last_folder_path = folder_path
        
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Find markdown files
            markdown_files = find_markdown_files(folder_path)
            
            if markdown_files:
                st.write(f"📄 Found {len(markdown_files)} files:")
                
                selected_file = None
                for rel_path, full_path in markdown_files:
                    # Highlight the currently selected file
                    is_selected = ('selected_file' in st.session_state and 
                                 st.session_state.selected_file == full_path)
                    button_type = "primary" if is_selected else "secondary"
                    
                    if st.button(
                        rel_path, 
                        key=full_path, 
                        use_container_width=True,
                        type=button_type
                    ):
                        selected_file = full_path
                        st.session_state.file_name = os.path.basename(full_path)
                        st.session_state.last_selected_file = full_path  # Remember for refresh
                
                # Store selected file in session state
                if selected_file:
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
            
            if content.strip():
                # Render markdown
                html_content = render_markdown(content)
                
                
                # Display the rendered markdown using HTML component
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
                    <script>
                        // Debug function to log messages
                        function debugLog(message) {{
                            console.log('[Markdown Viewer Debug]', message);
                        }}

                        document.addEventListener('DOMContentLoaded', function() {{
                            debugLog('DOM loaded, setting up link listeners');
                            
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
                                                    currentUrl.searchParams.set('navigate_to', targetPath.replace(/\//g, '\\\\'));
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
                clicked_link = components.html(
                    full_html,
                    height=800,
                    scrolling=True
                )
                
                # Debug: Show component return value
                if clicked_link:
                    st.sidebar.write("Debug - Component returned:", clicked_link)
                
                # Handle link navigation
                if clicked_link and isinstance(clicked_link, dict) and clicked_link.get('action') == 'navigate_to_file':
                    href = clicked_link.get('href')
                    base_dir = clicked_link.get('baseDir', '').replace('/', os.sep)
                    
                    st.sidebar.write(f"Debug - Navigating to: {href}")
                    st.sidebar.write(f"Debug - Base dir: {base_dir}")
                    
                    if href:
                        # Resolve the target file path
                        target_path = resolve_markdown_link(selected_file_path, href)
                        st.sidebar.write(f"Debug - Resolved path: {target_path}")
                        
                        if target_path and os.path.exists(target_path):
                            st.sidebar.success(f"Debug - File found, navigating to: {target_path}")
                            # Update session state to navigate to the new file
                            st.session_state.selected_file = target_path
                            st.session_state.file_name = os.path.basename(target_path)
                            st.session_state.last_selected_file = target_path
                            
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