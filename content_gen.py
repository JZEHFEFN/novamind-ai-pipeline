import os
import httpx
from openai import OpenAI
from groq import Groq
from utils import save_json, load_prompts, validate_prompts
from dotenv import load_dotenv

load_dotenv()

# Create a custom HTTP client without proxy settings
http_client = httpx.Client()
'''client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    http_client=http_client
)'''
#client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
try:
    from groq import Groq
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    USE_GROQ = True
    print("Using Groq API (free)")
except ImportError:
    print("Groq not installed. Run: pip install groq")
except Exception as e:
    print(f"Groq init failed: {e}")

# Load prompts from external file
PROMPTS = load_prompts('prompts/prompts.txt')

# Validate prompts are loaded correctly
if not validate_prompts(PROMPTS):
    print("Some prompts missing. Check prompts.txt format.")
    print("Available prompts:", list(PROMPTS.keys()))

# Define 3 personas
PERSONAS = {
    'creative_director': 'NEWSLETTER_CREATIVE_DIRECTOR',
    'automation_specialist': 'NEWSLETTER_AUTOMATION_SPECIALIST',
    'freelance_designer': 'NEWSLETTER_FREELANCE_DESIGNER'
}

def generate_blog(topic):
    """Generate blog post using external prompt"""
    blog_prompt = PROMPTS.get('BLOG_GENERATION', '').format(topic=topic)
    
    if not blog_prompt:
        raise ValueError("BLOG_GENERATION prompt not found in prompts.txt")
    
    '''response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": blog_prompt}],
        temperature=0.7
    )'''

    response = client.chat.completions.create(
    model="openai/gpt-oss-120b",  # Groq's free model
    messages=[{"role": "user", "content": blog_prompt}],
    temperature=0.7,
    max_tokens=1500
    )

    # Debug: Check if content was returned
    if not response.choices[0].message.content or len(response.choices[0].message.content.strip()) < 50:
        print(f"Warning: Blog content seems short or empty")
        # Fallback to a simple prompt if the main one failed
        fallback_prompt = f"Write a 500-word blog post about '{topic}'. Make it practical and actionable."
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # Groq's free model
            messages=[{"role": "user", "content": fallback_prompt}],
            temperature=0.7,
            max_tokens=1500
        )
    
    return response.choices[0].message.content

def generate_newsletter(persona_key, blog_content):
    """Generate newsletter for specific persona using external prompt"""
    prompt_key = PERSONAS.get(persona_key)
    
    if not prompt_key:
        raise ValueError(f"Unknown persona: {persona_key}")
    
    newsletter_prompt = PROMPTS.get(prompt_key, '').format(blog_content=blog_content)
    
    if not newsletter_prompt:
        raise ValueError(f"Prompt not found for {prompt_key}")
    
    '''response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": newsletter_prompt}],
        temperature=0.8
    )'''
    response = client.chat.completions.create(
    model="openai/gpt-oss-120b",  # Groq's free model
    messages=[{"role": "user", "content": newsletter_prompt}],
    temperature=0.7
    )
    
    return response.choices[0].message.content

def generate_blog_and_newsletters(topic):
    """Generate blog post and 3 newsletter versions"""
    
    print("Generating blog post...")
    blog_content = generate_blog(topic)
    
    print("Generating newsletters for each persona...")
    newsletters = {}
    for persona_key in PERSONAS.keys():
        print(f"   - {persona_key.replace('_', ' ').title()}...")
        newsletters[persona_key] = generate_newsletter(persona_key, blog_content)
    
    # Save everything
    output = {
        'topic': topic,
        'blog_post': blog_content,
        'newsletters': newsletters,
        'personas': {
            'creative_director': 'Agency owner focused on ROI and time savings',
            'automation_specialist': 'Operations person who loves integrations',
            'freelance_designer': 'Independent creative wanting ease of use'
        }
    }
    
    save_json(output, 'generated_content.json')
    print(f"\nComplete! Generated blog + 3 newsletters for: {topic}")
    
    # Show preview
    print("\nBlog Title Preview:")
    first_line = blog_content.split('\n')[0]
    print(f"   {first_line[:80]}...")
    
    return output

def reload_prompts():
    """Utility function to reload prompts without restarting"""
    global PROMPTS
    PROMPTS = load_prompts('prompts.txt')
    validate_prompts(PROMPTS)
    print("Prompts reloaded from prompts.txt")
    return PROMPTS

if __name__ == "__main__":
    # Test the generator
    test_topic = "AI for creative agency workflows"
    result = generate_blog_and_newsletters(test_topic)
    
    print("\n🎨 Newsletter Preview (Creative Director):")
    print("-" * 50)
    print(result['newsletters']['creative_director'][:200] + "...")