"""
NovaMind AI Marketing Pipeline
Run with: python3 main.py --topic "Your topic here"
"""

import argparse
from content_gen import generate_blog_and_newsletters
from crm_integration import sync_contacts_and_campaign
from performance import simulate_performance, generate_ai_insights

def run_pipeline(topic):
    """Run the complete marketing pipeline"""
    
    print("\n" + "="*50)
    print(f"Starting NovaMind Pipeline: {topic}")
    print("="*50 + "\n")
    
    # Step 1: Generate content
    print("STEP 1: Generating AI Content...")
    content = generate_blog_and_newsletters(topic)
    print(f"   ✓ Blog post created ({len(content['blog_post'])} chars)")
    print(f"   ✓ {len(content['newsletters'])} newsletter variants generated\n")
    
    # Step 2: Sync to CRM
    print("STEP 2: Syncing to HubSpot CRM...")
    campaign_results = sync_contacts_and_campaign(topic, content['newsletters'])
    print(f"   ✓ Campaigns logged for {len(campaign_results)} personas\n")
    
    # Step 3: Simulate performance
    print("STEP 3: Collecting Engagement Data...")
    performance = simulate_performance(campaign_results)
    
    # Print quick metrics
    print("\n Performance Summary:")
    for persona, data in performance.items():
        m = data['metrics']
        print(f"   • {persona.replace('_', ' ').title()}: {m['open_rate']*100:.0f}% open, {m['click_rate']*100:.0f}% click")
    
    # Step 4: AI analysis
    print("\nSTEP 4: AI Performance Analysis...")
    insights = generate_ai_insights(performance)
    
    print("\n" + "="*50)
    print("PIPELINE COMPLETE")
    print("="*50)
    print("\nAI-GENERATED INSIGHTS:")
    print("-"*40)
    print(insights)
    print("-"*40)
    
    # Print next steps
    print("\nNext Steps:")
    print("   1. Check data/ folder for all generated content")
    print("   2. Review data/performance_history.json for trends")
    print("   3. Run again with a different topic")
    
    return insights

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NovaMind AI Marketing Pipeline')
    parser.add_argument('--topic', type=str, 
                       default="How AI is transforming creative agency workflows",
                       help='Topic for blog and newsletter')
    
    args = parser.parse_args()
    run_pipeline(args.topic)
