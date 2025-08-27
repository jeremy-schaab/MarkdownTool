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

Document content:
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
                
                response = self.client.chat.completions.create(
                    model=self.config['deployment'],
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful AI assistant that analyzes and summarizes markdown documents. Provide clear, well-structured responses based on the content provided."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    max_tokens=self.config['max_tokens'],
                    temperature=self.config['temperature'],
                    timeout=self.config['timeout']
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