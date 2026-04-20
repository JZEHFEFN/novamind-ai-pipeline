# NovaMind AI Marketing Pipeline

AI-powered content generation + CRM distribution + performance analysis.

## Architecture

User Input → AI Blog + 3 Newsletters → HubSpot CRM → Simulated Metrics → AI Insights

## Setup

1. Clone repo
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Add API keys to `.env`:
   - `OPENAI_API_KEY`
   - `HUBSPOT_ACCESS_TOKEN`

## Run

```bash
python3 main.py --topic "Your topic here"
