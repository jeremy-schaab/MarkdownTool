import os
import time
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from openai import AzureOpenAI
import streamlit as st

# Load environment variables
load_dotenv()

class AIService:
    def __init__(self):
        self.client = None
        self.config = {
            'endpoint': os.getenv('AZURE_OPENAI_ENDPOINT'),
            'api_key': os.getenv('AZURE_OPENAI_API_KEY'),
            'api_version': os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
            'deployment': os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT', 'gpt-5-mini'),
            'max_tokens': int(os.getenv('AZURE_OPENAI_MAX_TOKENS', 128000)),
            'temperature': float(os.getenv('AZURE_OPENAI_TEMPERATURE', 0.25)),
            'timeout': int(os.getenv('AZURE_OPENAI_REQUEST_TIMEOUT', 180)),
            'max_context_tokens': 400000  # GPT-5 Mini context window
        }
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Azure OpenAI client"""
        try:
            if not self.config['endpoint'] or not self.config['api_key']:
                raise ValueError("Azure OpenAI endpoint and API key must be provided")
            
            self.client = AzureOpenAI(
                azure_endpoint=self.config['endpoint'],
                api_key=self.config['api_key'],
                api_version=self.config['api_version']
            )
        except Exception as e:
            st.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
            self.client = None
    
    def is_configured(self) -> bool:
        """Check if the AI service is properly configured"""
        return self.client is not None
    
    def get_prompt_templates(self) -> Dict[str, Dict[str, str]]:
        """Get all available prompt templates"""
        return {
            "high_level": {
                "name": "High Level Summary",
                "description": "Brief overview focusing on main topics and key points",
                "prompt": """Please provide a high-level summary of this markdown document. Focus on:
- Main topics and key themes
- Primary purpose and objectives
- Key takeaways
- Target audience (if apparent)

Keep the summary concise (2-4 paragraphs) and accessible to a general audience.

**Format Requirements:**
- Use proper Markdown headers (# ## ###)
- Use bullet points for lists
- Use **bold** for emphasis on key points
- Use *italic* for subtle emphasis
- Ensure proper paragraph spacing
- Structure as a complete, well-formatted Markdown document

Document content:
{content}"""
            },
            "detailed": {
                "name": "Detailed Overview", 
                "description": "Comprehensive analysis including context, scope, and implications",
                "prompt": """Please provide a detailed overview of this markdown document. Include:
- Comprehensive summary of all major sections
- Context and background information
- Scope and coverage of the content
- Key concepts and terminology explained
- Implications or significance of the information
- Relationships between different topics covered

Provide a thorough analysis suitable for someone who needs to understand the full scope of the document.

**Format Requirements:**
- Use clear Markdown headers (# ## ###) to organize sections
- Use numbered lists for sequential information
- Use bullet points for related items
- Use `code blocks` for technical terms or code
- Use **bold** for important concepts
- Use *italic* for definitions or emphasis
- Include proper paragraph breaks and spacing
- Structure as a professional, well-formatted Markdown document

Document content:
{content}"""
            },
            "architectural": {
                "name": "Architectural Overview",
                "description": "Focus on system design, components, and relationships", 
                "prompt": """Please analyze this markdown document from an architectural perspective. Focus on:
- System components and their roles
- Architecture patterns and design principles
- Component relationships and dependencies
- Data flow and communication patterns
- Technical stack and technologies mentioned
- Scalability and performance considerations
- Integration points and interfaces

Present the analysis in a way that would be useful for software architects and technical leads.

**Format Requirements:**
- Use clear Markdown headers (# ## ###) for different architectural aspects
- Use bullet points for component lists and features
- Use numbered lists for processes or sequential steps
- Use ```code blocks``` for technical specifications or code examples
- Use **bold** for component names and important terms
- Use *italic* for architectural patterns or concepts
- Include diagrams descriptions in text format where helpful
- Structure as a technical Markdown document with proper formatting

Document content:
{content}"""
            },
            "technical": {
                "name": "Technical Detail",
                "description": "Deep dive into implementation details and technical specifications",
                "prompt": """Please provide a technical deep-dive analysis of this markdown document. Focus on:
- Implementation details and code examples
- Technical specifications and requirements
- APIs, protocols, and data formats
- Configuration and setup instructions
- Technical dependencies and prerequisites
- Performance metrics and optimization details
- Troubleshooting and debugging information
- Best practices and conventions mentioned

Provide technical insights suitable for developers and engineers working with this system.

**Format Requirements:**
- Use clear Markdown headers (# ## ###) for different technical aspects
- Use ```code blocks``` with language specification for all code examples
- Use bullet points for requirements, features, and lists
- Use numbered lists for step-by-step procedures
- Use **bold** for important technical terms and concepts
- Use *italic* for file names, variables, and parameters
- Use tables for specifications and comparisons where appropriate
- Include proper code formatting and syntax highlighting
- Structure as a comprehensive technical Markdown document

Document content:
{content}"""
            },
            "review": {
                "name": "Technical Review",
                "description": "Critical analysis identifying strengths, weaknesses, and recommendations",
                "prompt": """Please provide a technical review of this markdown document. Include:
- Strengths and positive aspects
- Areas for improvement or potential issues
- Missing information or gaps in documentation
- Clarity and organization assessment
- Technical accuracy review (if applicable)
- Recommendations for enhancements
- Suggested next steps or follow-up actions
- Risk assessment or potential concerns

Provide constructive feedback that would help improve the document or the system it describes.

**Format Requirements:**
- Use clear Markdown headers (# ## ###) to organize review sections
- Use bullet points for strengths, weaknesses, and recommendations
- Use numbered lists for prioritized action items or steps
- Use **bold** for important findings and key recommendations
- Use *italic* for document references and specific concerns
- Use `code` formatting for specific technical issues
- Include checkboxes (- [ ]) for actionable items
- Structure as a professional review document with clear formatting

Document content:
{content}"""
            },
            "improve": {
                "name": "Improve this Document",
                "description": "Enhanced version with improved readability, organization, and added context",
                "prompt": """Please analyze this markdown document and provide an improved version that enhances readability and organization. Your improvements should:

**Structure & Organization:**
- Reorganize content for better logical flow
- Add or improve section headers and subheaders
- Create clear hierarchies and groupings
- Add table of contents if beneficial

**Readability Enhancements:**
- Improve clarity of explanations
- Break up dense paragraphs into digestible chunks
- Add bullet points and numbered lists where appropriate
- Enhance formatting for better visual appeal

**Content Enrichment:**
- Add contextual information where helpful
- Include brief explanations for technical terms
- Add introductory paragraphs to sections when needed
- Suggest examples or use cases where relevant
- Add cross-references between related sections

**Quality Improvements:**
- Fix any formatting inconsistencies
- Ensure consistent terminology throughout
- Improve transitions between sections
- Add summary points where beneficial

**Important Guidelines:**
- DO NOT remove any existing content
- DO NOT change the core meaning or intent
- DO NOT add information that isn't supported by the original content
- Focus on making the existing information clearer and more accessible
- Preserve all original technical details and specifications

**Markdown Formatting Requirements:**
- Use proper Markdown headers (# ## ### ####) for clear hierarchy
- Use bullet points and numbered lists appropriately
- Use **bold** for important terms and concepts
- Use *italic* for emphasis and definitions
- Use `code` blocks for technical terms, file names, and code
- Use tables for structured information
- Include proper line spacing and paragraph breaks
- Add table of contents using Markdown links if beneficial
- Ensure all formatting follows Markdown best practices

Please provide the complete improved document as a well-formatted Markdown file with clear explanations of major changes made.

Original document content:
{content}"""
            }
        }
    
    def generate_summary(self, content: str, template_key: str, progress_callback=None) -> Dict[str, Any]:
        """Generate a summary using the specified template"""
        if not self.is_configured():
            return {
                'success': False,
                'error': 'AI service is not properly configured. Please check your Azure OpenAI credentials.',
                'summary': ''
            }
        
        templates = self.get_prompt_templates()
        if template_key not in templates:
            return {
                'success': False,
                'error': f'Invalid template key: {template_key}',
                'summary': ''
            }
        
        template = templates[template_key]
        prompt = template['prompt'].format(content=content)
        
        try:
            if progress_callback:
                progress_callback("Sending request to Azure OpenAI...")
            
            # Make the API call with retry logic
            response = self._call_api_with_retry(prompt, progress_callback)
            
            if response:
                summary = response.choices[0].message.content
                return {
                    'success': True,
                    'summary': summary,
                    'template_name': template['name'],
                    'template_description': template['description'],
                    'tokens_used': response.usage.total_tokens if response.usage else None
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to get response from Azure OpenAI',
                    'summary': ''
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Error generating summary: {str(e)}',
                'summary': ''
            }
    
    def _call_api_with_retry(self, prompt: str, progress_callback=None, max_retries: int = 3):
        """Call the Azure OpenAI API with retry logic"""
        for attempt in range(max_retries):
            try:
                if progress_callback:
                    progress_callback(f"Attempt {attempt + 1} of {max_retries}...")
                
                # Use only parameters supported by the model
                response = self.client.chat.completions.create(
                    model=self.config['deployment'],
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful AI assistant that analyzes and summarizes markdown documents. ALWAYS format your responses using proper Markdown syntax including headers (# ## ###), bullet points, numbered lists, code blocks (```), emphasis (*italic*, **bold**), and proper line spacing. Ensure your output is a well-structured, properly formatted Markdown document that will render beautifully."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ]
                )
                
                return response
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                
                if progress_callback:
                    progress_callback(f"Attempt {attempt + 1} failed, retrying...")
                
                # Wait before retrying (exponential backoff)
                time.sleep(2 ** attempt)
        
        return None
    
    def estimate_tokens(self, content: str) -> int:
        """Rough estimation of tokens in content (4 characters ≈ 1 token)"""
        return len(content) // 4
    
    def validate_content_size(self, content: str) -> Dict[str, Any]:
        """Validate that content size is appropriate for API limits"""
        estimated_tokens = self.estimate_tokens(content)
        # Reserve tokens for system prompt, user prompt formatting, and response
        system_prompt_tokens = 200  # Estimated tokens for system prompt
        formatting_tokens = 300     # Estimated tokens for prompt formatting
        response_tokens = self.config['max_tokens']  # Reserve full response capacity
        
        max_input_tokens = self.config['max_context_tokens'] - system_prompt_tokens - formatting_tokens - response_tokens
        
        if estimated_tokens > max_input_tokens:
            return {
                'valid': False,
                'estimated_tokens': estimated_tokens,
                'max_tokens': max_input_tokens,
                'message': f'Content is too large ({estimated_tokens:,} estimated tokens). Maximum allowed is {max_input_tokens:,} tokens.'
            }
        
        return {
            'valid': True,
            'estimated_tokens': estimated_tokens,
            'max_tokens': max_input_tokens,
            'message': f'Content size is acceptable ({estimated_tokens:,} estimated tokens out of {max_input_tokens:,} max).'
        }

# Global instance
ai_service = AIService()