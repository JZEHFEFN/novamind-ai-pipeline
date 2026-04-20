import os
import random
import requests
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput, ApiException
from dotenv import load_dotenv
from utils import save_json, log_campaign

load_dotenv()

# Persona to list ID mapping (we'll create these lists)
PERSONA_LISTS = {
    'creative_director': None,  # Will be created dynamically
    'automation_specialist': None,
    'freelance_designer': None
}

# Mock contact data (for testing without real API)
MOCK_CONTACTS = {
    'creative_director': [
        {'email': 'sarah@creativeagency.com', 'firstname': 'Sarah', 'lastname': 'Chen'},
        {'email': 'marcus@designstudio.com', 'firstname': 'Marcus', 'lastname': 'Rodriguez'},
        {'email': 'emily@brandlab.com', 'firstname': 'Emily', 'lastname': 'Wong'}
    ],
    'automation_specialist': [
        {'email': 'alex@workflowpro.com', 'firstname': 'Alex', 'lastname': 'Kim'},
        {'email': 'jordan@automate.io', 'firstname': 'Jordan', 'lastname': 'Patel'},
        {'email': 'taylor@opsmaster.com', 'firstname': 'Taylor', 'lastname': 'Nguyen'}
    ],
    'freelance_designer': [
        {'email': 'chloe@creativemuse.com', 'firstname': 'Chloe', 'lastname': 'Davis'},
        {'email': 'ryan@designfreelance.com', 'firstname': 'Ryan', 'lastname': 'Martinez'},
        {'email': 'zoe@artspace.com', 'firstname': 'Zoe', 'lastname': 'Thompson'}
    ]
}

# Initialize HubSpot client
try:
    hubspot_client = HubSpot(access_token=os.getenv('HUBSPOT_ACCESS_TOKEN'))
    print("HubSpot client initialized")
except Exception as e:
    print(f"HubSpot init failed: {e}")
    print("Will use mock mode instead")
    hubspot_client = None

def create_contact_list(list_name, persona):
    """Create a contact list in HubSpot for a persona"""
    if not hubspot_client:
        print(f"   ⚠️ WARNING: HubSpot client not available - cannot create list '{list_name}'")
        return None
    
    try:
        # Correct HubSpot Lists API v3 endpoint
        url = "https://api.hubapi.com/crm/v3/lists/"
        headers = {
            "Authorization": f"Bearer {os.getenv('HUBSPOT_ACCESS_TOKEN')}",
            "Content-Type": "application/json"
        }
        
        # Correct payload format for HubSpot v3 lists
        payload = {
            "name": list_name,
            "objectType": "CONTACT",
            "processingType": "MANUAL",
            "customProperties": {}
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            list_id = response.json().get('id')
            print(f"Created list '{list_name}' (ID: {list_id})")
            return list_id
        else:
            print(f"Failed to create list: HTTP {response.status_code}")
            # Don't show HTML error, just a clean message
            if response.status_code == 401:
                print(f"Authentication failed - check your HubSpot token")
            elif response.status_code == 403:
                print(f"Permission denied - check your app scopes")
            return None
            
    except Exception as e:
        print(f"Error creating list: {e}")
        return None

def add_contact_to_list(contact_id, list_id):
    """Add a contact to a specific list"""
    if not hubspot_client or not list_id:
        return False
    
    try:
        # Correct endpoint for adding contacts to list
        url = f"https://api.hubapi.com/crm/v3/lists/{list_id}/memberships/add"
        headers = {
            "Authorization": f"Bearer {os.getenv('HUBSPOT_ACCESS_TOKEN')}",
            "Content-Type": "application/json"
        }
        
        # Contact IDs must be integers
        payload = {
            "recordIds": [int(contact_id)]  # Changed from "contactIds" to "recordIds"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"Added contact to list")
            return True
        else:
            print(f"Failed to add to list: HTTP {response.status_code}")
            return False
        
    except Exception as e:
        print(f"Error adding to list: {e}")
        return False

def create_or_update_contact(contact_info, persona):
    """Create or update a contact in HubSpot and add to persona list"""
    contact_id = None
    
    if hubspot_client:
        try:
            properties = {
                'email': contact_info['email'],
                'firstname': contact_info['firstname'],
                'lastname': contact_info['lastname'],
                'hs_lead_status': 'NEW'
            }
            contact_input = SimplePublicObjectInput(properties=properties)
            contact = hubspot_client.crm.contacts.basic_api.create(
                simple_public_object_input_for_create=contact_input
            )
            contact_id = contact.id
            print(f"Created contact: {contact_info['firstname']} {contact_info['lastname']} (ID: {contact_id})")
            
        except ApiException as e:
            if "already exists" in str(e) or "409" in str(e):
                # Contact exists, search for it
                try:
                    search_response = hubspot_client.crm.contacts.search_api.do_search(
                        public_object_search_request={
                            "filterGroups": [{
                                "filters": [{
                                    "propertyName": "email",
                                    "operator": "EQ",
                                    "value": contact_info['email']
                                }]
                            }]
                        }
                    )
                    if search_response.results:
                        contact_id = search_response.results[0].id
                        print(f"Contact exists: {contact_info['email']} (ID: {contact_id})")
                except Exception as search_error:
                    print(f"Search error: {search_error}")
                    contact_id = f"mock_{contact_info['email']}"
            else:
                print(f"HubSpot error: {e}")
                contact_id = f"mock_{contact_info['email']}"
    else:
        # Mock mode
        contact_id = f"mock_{contact_info['email']}"
        print(f"   Mock: Created contact {contact_info['email']} for {persona}")
    
    return contact_id

def sync_contacts_and_campaign(blog_title, newsletters):
    """Sync contacts to CRM, add to lists, and log campaign"""
    campaign_results = {}
    
    # Check if HubSpot is available
    if not hubspot_client:
        print("\nWARNING: HubSpot client not initialized")
        print("Continuing with mock mode - contacts will not be created in HubSpot")
        print("Add HUBSPOT_ACCESS_TOKEN to .env to enable real CRM integration\n")
    
    # Create lists for each persona (only if HubSpot available)
    print("\nSetting up persona lists...")
    for persona in PERSONA_LISTS.keys():
        list_name = f"NovaMind - {persona.replace('_', ' ').title()}"
        
        if hubspot_client:
            list_id = create_contact_list(list_name, persona)
        else:
            print(f"Skipping list creation for '{list_name}' (no HubSpot client)")
            list_id = None
        
        PERSONA_LISTS[persona] = list_id
    
    for persona, newsletter_content in newsletters.items():
        print(f"\nProcessing {persona}...")
        contact_ids = []
        list_id = PERSONA_LISTS.get(persona)
        
        # Create/update contacts for this persona
        for contact in MOCK_CONTACTS[persona]:
            if hubspot_client:
                contact_id = create_or_update_contact(contact, persona)
                contact_ids.append(contact_id)
                
                # Add to persona list if list exists
                if list_id and contact_id and not isinstance(contact_id, str):
                    add_contact_to_list(contact_id, list_id)
            else:
                # Mock mode - just track what would happen
                contact_id = f"mock_{contact['email']}"
                contact_ids.append(contact_id)
                print(f"   Mock: Would create contact {contact['email']} for {persona}")
        
        # Create campaign log entry
        campaign_id = f"campaign_{blog_title[:20].replace(' ', '_')}_{persona}_{random.randint(1000,9999)}"
        
        # Log to JSON
        log_campaign(blog_title, persona, campaign_id, contact_ids, 
                    log_file='campaign_log.json', 
                    list_id=list_id)
        
        campaign_results[persona] = {
            'campaign_id': campaign_id,
            'contact_ids': contact_ids,
            'list_id': list_id,
            'newsletter_content': newsletter_content
        }
        
        if hubspot_client and list_id:
            print(f"Synced {len(contact_ids)} contacts to list for {persona}")
        else:
            print(f"Mock: Would sync {len(contact_ids)} contacts for {persona}")
    
    save_json(campaign_results, 'latest_campaign.json')
    return campaign_results

if __name__ == "__main__":
    # Test mode
    test_newsletters = {
        'creative_director': 'Test newsletter for creative directors',
        'automation_specialist': 'Test for automation specialists',
        'freelance_designer': 'Test for freelancers'
    }
    sync_contacts_and_campaign("Test AI Campaign", test_newsletters)