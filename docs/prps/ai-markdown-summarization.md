# Product Requirement Prompt: AI-Powered Markdown Document Summarization

## Objective/Problem Statement
Users need the ability to quickly understand and analyze markdown documents without reading through entire files. The application should leverage AI to provide structured summaries based on different analytical perspectives, helping users extract relevant information efficiently.

## Success Metrics
- Users can successfully generate AI summaries for any loaded markdown file
- All 5 prompt templates produce relevant, well-structured summaries
- Azure OpenAI integration works reliably with proper error handling
- Summary generation completes within 30 seconds for typical documents
- User can easily switch between different summary types for the same document

## User Stories
- **As a developer**, I want a high-level summary to quickly understand what a documentation file covers
- **As a project manager**, I want detailed overviews to understand project scope and requirements
- **As a software architect**, I want architectural overviews to understand system design and components
- **As a technical lead**, I want technical details to understand implementation specifics
- **As a code reviewer**, I want technical reviews to identify potential issues or improvements

## Functional Requirements

### Core Functionality
1. **AI Summary Panel** - Add new UI section in sidebar or main area for AI operations
2. **Prompt Template Selector** - Dropdown/radio buttons to choose from 5 templates:
   - High Level Summary: Brief overview focusing on main topics and key points
   - Detailed Overview: Comprehensive analysis including context, scope, and implications
   - Architectural Overview: Focus on system design, components, and relationships
   - Technical Detail: Deep dive into implementation details, code examples, and technical specifications
   - Technical Review: Critical analysis identifying strengths, weaknesses, and recommendations
3. **Generate Summary Button** - Trigger AI processing for selected template
4. **Summary Display Area** - Formatted output area showing AI-generated content
5. **Loading States** - Progress indicators during AI processing
6. **Error Handling** - User-friendly error messages for API failures

### Azure OpenAI Integration
1. **Configuration Management** - Secure storage of Azure OpenAI credentials
2. **API Client** - Integration with Azure OpenAI Python SDK
3. **Token Management** - Handle token limits and chunking for large documents
4. **Model Selection** - Use appropriate GPT model (GPT-4 recommended)

## Non-Functional Requirements

### Performance
- Summary generation: < 30 seconds for documents up to 50KB
- UI responsiveness during processing (non-blocking)
- Efficient token usage to minimize API costs

### Security
- Azure OpenAI credentials stored securely (environment variables or config file)
- No sensitive data logged in AI requests
- Proper API key validation

### Usability
- Clear visual distinction between original content and AI-generated summaries
- Copy/export functionality for generated summaries
- Maintain summary history during session

### Reliability
- Graceful handling of API rate limits
- Retry logic for transient failures
- Fallback messaging when AI service unavailable

## Technical Implementation Details

### New Components Required
1. **AI Service Module** (`ai_service.py`)
   - Azure OpenAI client configuration
   - Prompt template definitions
   - Summary generation functions
   - Error handling and retries

2. **UI Enhancements** (in `markdown_viewer.py`)
   - AI summary sidebar section
   - Template selection controls
   - Summary display component
   - Loading/error state management

### Configuration
- Environment variables: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`
- Model configuration: deployment name, temperature, max tokens

### Dependencies
- `openai` - Azure OpenAI Python SDK
- `python-dotenv` - Environment variable management

## Acceptance Criteria
1. User can select any of the 5 prompt templates from a clear UI control
2. Clicking "Generate Summary" processes the currently loaded markdown file
3. Loading indicator appears during processing
4. Generated summary displays in dedicated area with proper formatting
5. Error messages appear for invalid API credentials or service failures
6. User can generate multiple summaries with different templates for same document
7. Summary content is relevant and well-structured based on selected template type
8. All Azure OpenAI API calls include proper authentication and error handling
9. Application remains responsive during AI processing
10. Generated summaries can be copied or saved by user

## Out of Scope
- Custom prompt editing (templates are predefined)
- Summary comparison features
- AI model fine-tuning
- Multi-language support for summaries
- Batch processing multiple files
- Summary export to external formats