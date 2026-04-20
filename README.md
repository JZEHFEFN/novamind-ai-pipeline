# NovaMind AI Marketing Pipeline

> AI-powered marketing automation that generates blog content, distributes persona-based newsletters, syncs with HubSpot CRM, and provides AI-driven performance insights.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Output](#output)
- [HubSpot Setup](#hubspot-setup)
- [Troubleshooting](#troubleshooting)
- [Assumptions](#assumptions)

---

## Overview

This pipeline automates the entire marketing content workflow:

1. **Generate** - AI creates a blog post and 3 persona-specific newsletters
2. **Distribute** - Syncs contacts to HubSpot CRM with persona segmentation
3. **Analyze** - Simulates engagement metrics and provides AI-powered optimization insights

The system supports dual AI models (OpenAI primary, Groq fallback) with automatic quota detection.

---

## Features

| Feature | Description |
|---------|-------------|
| **Dual AI Models** | OpenAI primary with automatic Groq fallback on quota exhaustion |
| **Persona Segmentation** | 3 personas: Creative Director, Automation Specialist, Freelance Designer |
| **HubSpot Integration** | Creates contacts, assigns personas, logs campaigns to contact timelines |
| **Campaign Logging** | JSON file backup + HubSpot contact notes with full campaign details |
| **Performance Analysis** | Simulated metrics with AI-generated actionable insights |
| **Rate Limiting** | Built-in delays and retry logic to prevent API throttling |
| **External Prompts** | All prompts stored in `prompts/prompts.txt` for easy editing |

---

## Prerequisites

- **Python 3.10+**
- **OpenAI API Key** (primary) - [Get one here](https://platform.openai.com/api-keys)
- **Groq API Key** (fallback) - [Get one here](https://console.groq.com)
- **HubSpot Access Token** - [Free developer account](https://developers.hubspot.com/)

---

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/novamind-pipeline.git
cd novamind-pipeline

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with API keys
cat > .env << 'EOF'
# OpenAI API Key (primary)
OPENAI_API_KEY=your-openai-key-here

# Groq API Key (fallback) - using openai/gpt-oss-120b model
GROQ_API_KEY=your-groq-key-here

# HubSpot Access Token
HUBSPOT_ACCESS_TOKEN=your-hubspot-token-here
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
openai==1.12.0
groq==0.9.0
hubspot-api-client==8.0.0
python-dotenv==1.0.0
requests==2.31.0
EOF

# Run the pipeline
python3 main.py --topic "Your topic here"
