# Markdown Link Navigation Solutions for Streamlit

## Problem Statement
The current Streamlit markdown viewer displays markdown files but local markdown links don't navigate within the app. When clicking a link like `[README](README.md)`, it tries to open the raw file instead of loading it in the viewer.

## Technical Challenges
- `components.html()` in Streamlit is primarily for display only
- No built-in bidirectional communication between iframe JavaScript and Python
- JavaScript postMessage events don't reliably reach Streamlit backend
- Streamlit reruns the entire script on each interaction, making state management complex

## Proposed Solutions

### Option 1: Parse and Replace Links Before Rendering (RECOMMENDED)
**Approach:** Pre-process markdown content to replace local `.md` links with Streamlit-native interactive elements.

**Implementation Steps:**
1. Parse markdown content using regex to find all `[text](*.md)` patterns
2. Replace each local markdown link with:
   - Unique placeholder text (e.g., `{{LINK_001}}`)
   - Store link mapping in session state
3. Render the modified markdown
4. After rendering, use `st.markdown()` with custom HTML buttons or `st.button()` elements
5. Handle clicks through native Streamlit callbacks

**Pros:**
- Works within Streamlit's paradigm
- No JavaScript communication issues
- Reliable and maintainable
- Can style links as buttons or keep link appearance

**Cons:**
- Requires parsing and modifying markdown content
- Links won't be inline with text (buttons appear separately)

**Example Implementation:**
```python
import re

def parse_markdown_links(content, base_dir):
    """Extract and replace markdown links with placeholders"""
    link_pattern = r'\[([^\]]+)\]\(([^)]+\.md)\)'
    links = []
    
    def replace_link(match):
        text = match.group(1)
        href = match.group(2)
        link_id = f"LINK_{len(links)}"
        links.append({
            'id': link_id,
            'text': text,
            'href': href,
            'path': resolve_path(base_dir, href)
        })
        return f"[{text}](#{link_id})"
    
    modified_content = re.sub(link_pattern, replace_link, content)
    return modified_content, links

def render_with_navigation(content, base_dir):
    modified_content, links = parse_markdown_links(content, base_dir)
    
    # Render the markdown
    st.markdown(modified_content)
    
    # Create navigation buttons
    if links:
        st.divider()
        st.subheader("Document Links")
        cols = st.columns(min(len(links), 3))
        for idx, link in enumerate(links):
            with cols[idx % 3]:
                if st.button(f"📄 {link['text']}", key=f"nav_{link['id']}"):
                    navigate_to_file(link['path'])
```

### Option 2: Use streamlit-bridge Component
**Approach:** Install third-party library that provides proper JavaScript-to-Python communication.

**Implementation Steps:**
1. Install: `pip install streamlit-bridge`
2. Use `bridge.html()` instead of `components.html()`
3. Implement JavaScript event listeners for link clicks
4. Receive events in Python through bridge's communication channel

**Pros:**
- Proper bidirectional communication
- Keeps links inline and clickable
- More control over HTML rendering

**Cons:**
- External dependency
- May have compatibility issues with Streamlit updates
- Limited documentation

### Option 3: Split Content and Navigation
**Approach:** Separate markdown display from navigation controls.

**Implementation Steps:**
1. Scan all markdown files and extract their links on startup
2. Create a navigation sidebar with all available documents
3. Display links as a separate navigation section above/below content
4. Use `st.button()` or `st.selectbox()` for navigation

**Pros:**
- Clear separation of concerns
- Easy to implement
- No JavaScript needed

**Cons:**
- Links not inline with content
- Less intuitive user experience
- Requires pre-scanning all files

### Option 4: Custom Streamlit Component
**Approach:** Build a proper Streamlit component with full bidirectional communication.

**Implementation Steps:**
1. Create component directory structure:
   ```
   markdown_viewer_component/
   ├── __init__.py
   ├── frontend/
   │   ├── index.html
   │   └── main.js
   ```
2. Implement Streamlit communication protocol in JavaScript
3. Use `Streamlit.setComponentValue()` for sending data back
4. Package and import as custom component

**Pros:**
- Full control over behavior
- Proper bidirectional communication
- Reusable component

**Cons:**
- Complex implementation
- Requires maintaining separate frontend code
- More development time

### Option 5: Hybrid Approach with Tabs
**Approach:** Use Streamlit's native UI elements for navigation.

**Implementation Steps:**
1. Parse all markdown files to build navigation structure
2. Create tabs for each major section or file
3. Use `st.tabs()` or nested `st.expander()` elements
4. Display markdown content in selected tab
5. Update tabs based on links in current file

**Pros:**
- Native Streamlit components
- Good for documentation-style navigation
- No JavaScript needed

**Cons:**
- Different UX from traditional link navigation
- May not scale well with many files

### Option 6: Use st.page_link with Dynamic Pages
**Approach:** Leverage Streamlit's multipage app features.

**Implementation Steps:**
1. Create a page router that dynamically loads markdown files
2. Use `st.page_link()` for navigation (reliable built-in component)
3. Pass file path as query parameter
4. Load and display markdown based on parameter

**Pros:**
- Uses Streamlit's official navigation features
- Reliable and well-supported
- Handles browser history

**Cons:**
- Requires restructuring as multipage app
- May have URL limitations

## Recommendation

**For immediate implementation:** Option 1 (Parse and Replace Links)
- Most reliable within current architecture
- Can be implemented quickly
- Works with existing single-page structure

**For long-term solution:** Option 4 (Custom Component) or Option 6 (Multipage)
- Better user experience
- More maintainable
- Proper navigation handling

## Implementation Priority

1. **Quick Fix:** Implement Option 1 to get working navigation immediately
2. **Enhancement:** Add visual indicators for clickable links
3. **Future:** Consider migrating to Option 4 or 6 for better UX

## Testing Strategy

1. Test with various link formats:
   - Relative: `[Link](file.md)`, `[Link](./file.md)`
   - Subfolder: `[Link](folder/file.md)`
   - Parent: `[Link](../file.md)`
   
2. Verify external links still work normally
3. Test with special characters in filenames
4. Ensure navigation updates sidebar selection
5. Test browser back/forward behavior

## Conclusion

While Streamlit's `components.html()` doesn't support proper bidirectional communication for link clicks, there are several viable workarounds. The parse-and-replace approach (Option 1) provides the best balance of reliability and implementation speed for the current needs.