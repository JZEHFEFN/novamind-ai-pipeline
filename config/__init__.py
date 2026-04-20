# config/__init__.py
"""
Configuration package for NovaMind AI Marketing Pipeline
"""

from .personas import (
    PERSONAS,
    get_persona_keys,
    get_persona_by_key,
    get_persona_value,
    get_persona_name,
    get_all_personas
)

from .mock_contacts import (
    DEMO_CONTACTS,
    EMAIL_TO_PERSONA,
    get_demo_contacts,
    get_demo_contacts_by_persona,
    get_email_to_persona_map
)

__all__ = [
    'PERSONAS',
    'get_persona_keys',
    'get_persona_by_key',
    'get_persona_value',
    'get_persona_name',
    'get_all_personas',
    'DEMO_CONTACTS',
    'EMAIL_TO_PERSONA',
    'get_demo_contacts',
    'get_demo_contacts_by_persona',
    'get_email_to_persona_map'
]
