# config/personas.py
"""
Persona configuration for NovaMind AI Marketing Pipeline
Edit this file to add, remove, or modify personas
"""

PERSONAS = {
    'creative_director': {
        'name': 'Creative Director',
        'value': 'creative_director',
        'description': 'Agency owner focused on ROI and time savings',
        'list_name': 'NovaMind - Creative Director',
        'prompt_key': 'NEWSLETTER_CREATIVE_DIRECTOR'  # Links to prompts.txt
    },
    'automation_specialist': {
        'name': 'Automation Specialist',
        'value': 'automation_specialist',
        'description': 'Operations person who loves integrations',
        'list_name': 'NovaMind - Automation Specialist',
        'prompt_key': 'NEWSLETTER_AUTOMATION_SPECIALIST'
    },
    'freelance_designer': {
        'name': 'Freelance Designer',
        'value': 'freelance_designer',
        'description': 'Independent creative wanting ease of use',
        'list_name': 'NovaMind - Freelance Designer',
        'prompt_key': 'NEWSLETTER_FREELANCE_DESIGNER'
    }
}

def get_persona_keys():
    """Return list of persona keys"""
    return list(PERSONAS.keys())

def get_persona_by_key(key):
    """Get persona configuration by key"""
    return PERSONAS.get(key)

def get_persona_value(key):
    """Get persona value for HubSpot hs_persona property"""
    return PERSONAS.get(key, {}).get('value')

def get_persona_name(key):
    """Get display name for persona"""
    return PERSONAS.get(key, {}).get('name')

def get_all_personas():
    """Return all personas"""
    return PERSONAS
