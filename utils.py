import json
from datetime import datetime
from log import get_logger

# Get logger for API client messages
logger = get_logger()

def save_json(data, filename):
    # Save data to JSON file
    with open(f"data/{filename}", 'w') as f:
        json.dump(data, f, indent=2)

def load_json(filename):
    # Load data from JSON file
    try:
        with open(f"data/{filename}", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def log_campaign(blog_title, persona, campaign_id, contact_ids, log_file='campaign_log.json', list_id=None):
    #Log campaign to specified JSON file with optional list_id
    log = load_json(log_file) or []
    
    entry = {
        'date': datetime.now().isoformat(),
        'blog_title': blog_title,
        'persona': persona,
        'campaign_id': campaign_id,
        'contact_ids': contact_ids
    }
    
    if list_id:
        entry['hubspot_list_id'] = list_id
    
    log.append(entry)
    save_json(log, log_file)
    logger.info(f"Logged to {log_file}")

def load_prompts(filepath='prompts/prompts.txt'):
    """
    Load prompts from text file into a dictionary
    Returns: {
        'BLOG_GENERATION': 'prompt text...',
        'NEWSLETTER_CREATIVE_DIRECTOR': 'prompt text...',
        ...
    }
    """
    prompts = {}
    current_key = None
    current_content = []
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                
                # Check if line is a section header (starts with === and ends with ===)
                if line.startswith('===') and line.endswith('==='):
                    # Save previous section if exists
                    if current_key and current_content:
                        prompts[current_key] = '\n'.join(current_content).strip()
                    
                    # Start new section (remove the === markers)
                    current_key = line.strip('= ')
                    current_content = []
                else:
                    if current_key:  # Only add content if we're inside a section
                        current_content.append(line)
        
        # Don't forget the last section
        if current_key and current_content:
            prompts[current_key] = '\n'.join(current_content).strip()
            
    except FileNotFoundError:
        logger.info(f"prompts.txt not found. Using default prompts.")
        return get_default_prompts()
    
    return prompts

def get_default_prompts():
    #Fallback prompts in case prompts.txt is missing
    return {
        'BLOG_GENERATION': "Write a 500-word blog post about {topic} for an AI startup...",
        'NEWSLETTER_CREATIVE_DIRECTOR': "Rewrite this blog as a 150-word newsletter for a Creative Director...",
        'NEWSLETTER_AUTOMATION_SPECIALIST': "Rewrite this blog as a 150-word newsletter for an Automation Specialist...",
        'NEWSLETTER_FREELANCE_DESIGNER': "Rewrite this blog as a 150-word newsletter for a Freelance Designer..."
    }

def validate_prompts(prompts):
    #Check that all required prompts exist
    required = [
        'BLOG_GENERATION',
        'NEWSLETTER_CREATIVE_DIRECTOR',
        'NEWSLETTER_AUTOMATION_SPECIALIST',
        'NEWSLETTER_FREELANCE_DESIGNER'
    ]
    
    missing = [r for r in required if r not in prompts]
    if missing:
        logger.info(f"Missing prompts: {missing}")
        return False
    return True
