import os
import time
from utils import save_json, load_prompts, validate_prompts
from dotenv import load_dotenv
from config import PERSONAS, get_persona_keys, get_persona_name
from log import get_logger

load_dotenv()

# Get logger for API client messages
logger = get_logger()

# DUAL MODEL CLIENT SETUP (OpenAI first, then Groq)
class DualModelClient:
    """
    Client that tries OpenAI first, then falls back to Groq.
    Once OpenAI quota is exhausted, it automatically uses free version of Groq for the rest of the session.
    """
    def __init__(self):
        self.openai_client = None
        self.groq_client = None
        self.openai_available = False
        self.groq_available = False
        self.openai_quota_exhausted = False
        self.openai_error_count = 0
        self.max_openai_errors = 1  # After 1 quota error, mark as exhausted
        
        # Try to initialize OpenAI
        try:
            from openai import OpenAI
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key and api_key not in ['sk-your-key-here', 'sk-proj-your-openai-key-here', '']:
                self.openai_client = OpenAI(api_key=api_key)
                self.openai_available = True
                logger.info("OpenAI client initialized")
            else:
                logger.info("OpenAI API key not found or invalid")
        except ImportError:
            logger.info("OpenAI not installed. Run: pip install openai")
        except Exception as e:
            logger.info(f"OpenAI init failed: {e}")
        
        # Try to initialize Groq as backup
        try:
            from groq import Groq
            api_key = os.getenv('GROQ_API_KEY')
            if api_key and api_key not in ['your-groq-key-here', 'gsk_your-groq-key-here', '']:
                self.groq_client = Groq(api_key=api_key)
                self.groq_available = True
                logger.info("Groq client initialized (backup)")
            else:
                logger.info("Groq API key not found or invalid")
        except ImportError:
            logger.info("Groq not installed. Run: pip install groq")
        except Exception as e:
            logger.info(f"Groq init failed: {e}")
        
        if not self.openai_available and not self.groq_available:
            logger.info("No API clients available. Please check your API keys.")
    
    def is_openai_quota_error(self, error_msg):
        #Check if error is related to quota exhaustion
        error_lower = str(error_msg).lower()
        quota_indicators = [
            'quota', 'insufficient', 'exceeded', 'billing', 
            'rate limit', '429', 'insufficient_quota'
        ]
        return any(indicator in error_lower for indicator in quota_indicators)
    
    def chat_completion(self, prompt, max_tokens=1500, temperature=0.7):
        """
        Try OpenAI first, then fallback to Groq.
        If OpenAI quota is already exhausted, skip directly to Groq.
        """
        # If OpenAI quota is already exhausted, skip directly to Groq
        if self.openai_quota_exhausted:
            logger.info("OpenAI quota exhausted, using Groq...")
            return self._use_groq(prompt, max_tokens, temperature)
        
        # Try OpenAI first
        if self.openai_available:
            try:
                logger.info("Trying OpenAI...")
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                content = response.choices[0].message.content
                # Only check if content exists, not length
                if content:
                    logger.info("OpenAI succeeded")
                    self.openai_error_count = 0
                    return content
                else:
                    logger.info("OpenAI returned empty content")
                    self.openai_error_count += 1
                    
            except Exception as e:
                error_msg = str(e)
                logger.info(f"OpenAI error: {error_msg[:100]}...")
                
                # Check if this is a quota error
                if self.is_openai_quota_error(error_msg):
                    self.openai_error_count += 1
                    logger.info(f"OpenAI quota error detected")
                    
                    if self.openai_error_count >= self.max_openai_errors:
                        self.openai_quota_exhausted = True
                        logger.info("OpenAI quota marked as EXHAUSTED for this session")
                        logger.info("Will use Groq for all remaining calls")
                else:
                    self.openai_error_count += 1
        
        # Fallback to Groq
        return self._use_groq(prompt, max_tokens, temperature)
    
    def _use_groq(self, prompt, max_tokens, temperature):
        # Use Groq as fallback
        if not self.groq_available:
            raise ValueError("Groq is not available")
        
        try:
            logger.info("Trying Groq...")
            response = self.groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            content = response.choices[0].message.content
            if content:
                logger.info("Groq succeeded")
                return content
            else:
                raise ValueError("Groq returned empty content")
        except Exception as e:
            logger.info(f"Groq error: {e}")
            raise ValueError(f"Groq failed: {e}")
    
    def is_available(self):
        #Check if any API client is available
        return self.openai_available or self.groq_available
    
    def get_status(self):
        #Get current status of both clients
        status = {
            'openai_available': self.openai_available,
            'groq_available': self.groq_available,
            'openai_quota_exhausted': self.openai_quota_exhausted,
            'openai_error_count': self.openai_error_count,
            'active_model': 'Groq' if self.openai_quota_exhausted or not self.openai_available else 'OpenAI'
        }
        return status


# Initialize the dual model client
llm_client = DualModelClient()

# Rate limiting: delay between API calls (in seconds)
API_DELAY = 2

# Load prompts from external file
PROMPTS = load_prompts('prompts/prompts.txt')

# Validate prompts are loaded correctly
if not validate_prompts(PROMPTS):
    logger.info("Some prompts missing. Check prompts.txt format.")
    logger.info("Available prompts:", list(PROMPTS.keys()))

# Map persona keys to prompt keys
PERSONA_PROMPT_MAP = {
    key: f"NEWSLETTER_{key.upper()}" for key in get_persona_keys()
}


def call_llm_with_retry(prompt, max_tokens=1500, retries=3):
    """
    Call LLM with retry logic and rate limiting
    Uses OpenAI first, then falls back to Groq
    """
    last_error = None
    
    for attempt in range(retries):
        try:
            content = llm_client.chat_completion(prompt, max_tokens=max_tokens)
            
            # Only check if content is not None/empty
            if content and len(content.strip()) > 0:
                return content
            else:
                logger.info(f"Attempt {attempt + 1}: Empty content received")
                if attempt < retries - 1:
                    time.sleep(API_DELAY)
                    
        except Exception as e:
            last_error = e
            logger.info(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(API_DELAY * (attempt + 1))
    
    raise ValueError(f"Failed to generate content after {retries} attempts. Last error: {last_error}")


def generate_blog(topic):
    #Generate blog post using external prompt
    blog_prompt = PROMPTS.get('BLOG_GENERATION', '').format(topic=topic)
    
    if not blog_prompt:
        raise ValueError("BLOG_GENERATION prompt not found in prompts.txt")
    
    logger.info("Calling API for blog generation...")
    blog_content = call_llm_with_retry(blog_prompt, max_tokens=2000, retries=3)
    
    # Add delay after blog generation
    time.sleep(API_DELAY)
    
    return blog_content


def generate_newsletter(persona_key, blog_content):
    #Generate newsletter for specific persona using external prompt
    prompt_key = PERSONA_PROMPT_MAP.get(persona_key)
    
    if not prompt_key:
        raise ValueError(f"Unknown persona: {persona_key}")
    
    newsletter_prompt = PROMPTS.get(prompt_key, '').format(blog_content=blog_content)
    
    if not newsletter_prompt:
        raise ValueError(f"Prompt not found for {prompt_key}")
    
    # Add delay before each newsletter generation
    time.sleep(API_DELAY)
    
    newsletter_content = call_llm_with_retry(newsletter_prompt, max_tokens=800, retries=3)
    
    return newsletter_content


def print_client_status():
    #Print the current status of API clients
    status = llm_client.get_status()
    logger.info("\n" + "="*50)
    logger.info("🔧 API CLIENT STATUS")
    logger.info("="*50)
    logger.info(f"   OpenAI Available: {'Yes' if status['openai_available'] else 'No'}")
    logger.info(f"   Groq Available: {'Yes' if status['groq_available'] else 'No'}")
    logger.info(f"   OpenAI Quota Exhausted: {'Yes' if status['openai_quota_exhausted'] else 'No'}")
    logger.info(f"   OpenAI Error Count: {status['openai_error_count']}")
    logger.info(f"   Active Model: {status['active_model']}")
    logger.info("="*50)


def generate_blog_and_newsletters(topic):
    #Generate blog post and newsletter for each persona
    
    if not llm_client.is_available():
        logger.info("\nNo API clients available. Please check your API keys.")
        return None
    
    # Print client status before starting
    print_client_status()
    
    logger.info("\nGenerating blog post...")
    blog_content = generate_blog(topic)
    
    logger.info("\nGenerating newsletters for each persona...")
    newsletters = {}
    
    for persona_key in get_persona_keys():
        persona_name = get_persona_name(persona_key)
        print(f"   - {persona_name}...")
        
        try:
            newsletters[persona_key] = generate_newsletter(persona_key, blog_content)
            logger.info(f"{persona_name} newsletter generated")
        except Exception as e:
            logger.info(f"Failed to generate {persona_name} newsletter: {e}")
            raise  # Re-raise the error instead of using fallback
    
    # Build output using config
    output = {
        'topic': topic,
        'blog_post': blog_content,
        'newsletters': newsletters,
        'personas': {
            key: PERSONAS[key]['description'] 
            for key in get_persona_keys()
        }
    }
    
    save_json(output, 'generated_content.json')
    
    # Show preview
    logger.info(f"\nComplete! Generated blog + {len(newsletters)} newsletters for: {topic}")
    logger.info("\nBlog Preview:")
    first_line = blog_content.split('\n')[0] if blog_content else "No content"
    logger.info(f"   {first_line[:80]}...")
    logger.info(f"   ✓ Blog post created ({len(blog_content)} chars)")
    logger.info(f"   ✓ {len(newsletters)} newsletter variants generated")
    
    return output


if __name__ == "__main__":
    test_topic = "AI for creative agency workflows"
    result = generate_blog_and_newsletters(test_topic)
    
    if result:
        # Show preview for each persona
        for persona_key in get_persona_keys():
            persona_name = get_persona_name(persona_key)
            newsletter = result['newsletters'].get(persona_key, "")
            logger.info(f"\n{persona_name} Preview:")
            logger.info("-" * 50)
            logger.info(newsletter[:300] + "...")
            