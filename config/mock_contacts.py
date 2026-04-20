# config/mock_contacts.py
"""
Mock contact data for demonstration purposes
Edit this file to add, remove, or modify demo contacts
"""

from .personas import get_persona_value

# Demo contacts with their personas
DEMO_CONTACTS = [
    # Creative Directors
    {
        'email': 'sarah@creativeagency.com',
        'firstname': 'Sarah',
        'lastname': 'Chen',
        'persona': 'creative_director'
    },
    {
        'email': 'marcus@designstudio.com',
        'firstname': 'Marcus',
        'lastname': 'Rodriguez',
        'persona': 'creative_director'
    },
    {
        'email': 'emily@brandlab.com',
        'firstname': 'Emily',
        'lastname': 'Wong',
        'persona': 'creative_director'
    },
    
    # Automation Specialists
    {
        'email': 'alex@workflowpro.com',
        'firstname': 'Alex',
        'lastname': 'Kim',
        'persona': 'automation_specialist'
    },
    {
        'email': 'jordan@automate.io',
        'firstname': 'Jordan',
        'lastname': 'Patel',
        'persona': 'automation_specialist'
    },
    {
        'email': 'taylor@opsmaster.com',
        'firstname': 'Taylor',
        'lastname': 'Nguyen',
        'persona': 'automation_specialist'
    },
    
    # Freelance Designers
    {
        'email': 'chloe@creativemuse.com',
        'firstname': 'Chloe',
        'lastname': 'Davis',
        'persona': 'freelance_designer'
    },
    {
        'email': 'ryan@designfreelance.com',
        'firstname': 'Ryan',
        'lastname': 'Martinez',
        'persona': 'freelance_designer'
    },
    {
        'email': 'zoe@artspace.com',
        'firstname': 'Zoe',
        'lastname': 'Thompson',
        'persona': 'freelance_designer'
    }
]

# Optional: Email to persona mapping for quick lookup
EMAIL_TO_PERSONA = {contact['email']: contact['persona'] for contact in DEMO_CONTACTS}

def get_demo_contacts():
    """Return list of all demo contacts"""
    return DEMO_CONTACTS

def get_demo_contacts_by_persona(persona_key):
    """Get demo contacts filtered by persona"""
    return [c for c in DEMO_CONTACTS if c.get('persona') == persona_key]

def get_email_to_persona_map():
    """Return mapping of email to persona for quick lookup"""
    return EMAIL_TO_PERSONA
