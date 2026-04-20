import random
from openai import OpenAI
from groq import Groq
from utils import save_json, load_json
from dotenv import load_dotenv
import os

load_dotenv()
#client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def simulate_performance(campaign_results):
    """Simulate engagement metrics for each campaign"""
    performance_data = {}
    
    for persona, campaign_info in campaign_results.items():
        # Realistic mock metrics
        metrics = {
            'open_rate': round(random.uniform(0.25, 0.55), 3),  # 25-55%
            'click_rate': round(random.uniform(0.05, 0.28), 3),  # 5-28%
            'unsubscribe_rate': round(random.uniform(0.01, 0.04), 3),  # 1-4%
            'unique_opens': random.randint(50, 200),
            'total_clicks': random.randint(10, 80)
        }
        
        performance_data[persona] = {
            'campaign_id': campaign_info['campaign_id'],
            'metrics': metrics,
            'persona_description': {
                'creative_director': 'Agency owner focused on ROI',
                'automation_specialist': 'Operations person focused on efficiency',
                'freelance_designer': 'Independent creative focused on ease of use'
            }[persona]
        }
    
    # Save historical performance
    history = load_json('performance_history.json') or []
    history.append({
        'date': __import__('datetime').datetime.now().isoformat(),
        'campaign': campaign_results,
        'metrics': performance_data
    })
    save_json(history, 'performance_history.json')
    
    return performance_data

def generate_ai_insights(performance_data):
    """Use AI to analyze performance and provide recommendations"""
    
    # Create a readable summary for the AI
    summary = "Campaign Performance Summary:\n"
    for persona, data in performance_data.items():
        m = data['metrics']
        summary += f"""
        {persona.replace('_', ' ').title()}:
        - Open rate: {m['open_rate']*100:.1f}%
        - Click rate: {m['click_rate']*100:.1f}%
        - Unsubscribe rate: {m['unsubscribe_rate']*100:.1f}%
        """
    
    analysis_prompt = f"""As a marketing analyst, analyze this newsletter campaign performance and provide:

1. Key insight (1 sentence)
2. Top performing persona (and why)
3. Specific recommendation for next week's content
4. One thing to improve

{summary}

Keep response under 150 words, be actionable."""
    
    try:
        '''response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": analysis_prompt}],
            temperature=0.7
        )'''
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # Groq's free model
            messages=[{"role": "user", "content": analysis_prompt}],
            temperature=0.7
        )
        insights = response.choices[0].message.content
    except Exception as e:
        insights = f"AI analysis failed: {e}. Based on metrics, focus on improving content for lower-performing personas."
    
    # Save insights
    result = {
        'performance_data': performance_data,
        'ai_insights': insights,
        'timestamp': __import__('datetime').datetime.now().isoformat()
    }
    save_json(result, 'latest_performance.json')
    
    return insights

if __name__ == "__main__":
    # Test with mock campaign results
    test_campaign = {
        'creative_director': {'campaign_id': 'test_1'},
        'automation_specialist': {'campaign_id': 'test_2'},
        'freelance_designer': {'campaign_id': 'test_3'}
    }
    perf = simulate_performance(test_campaign)
    insights = generate_ai_insights(perf)
    print("\nAI Insights:\n", insights)
