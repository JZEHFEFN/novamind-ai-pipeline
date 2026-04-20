# NovaMind AI Marketing Pipeline

> AI-powered marketing automation that generates blog content, distributes persona-based newsletters, syncs with HubSpot CRM, and provides AI-driven performance insights.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [HubSpot Setup](#hubspot-setup)
- [Usage](#usage)

---

# Overview

This pipeline automates the entire marketing content workflow:

1. **Generate** - AI creates a blog post and 3 persona-specific newsletters
2. **Distribute** - Syncs contacts to HubSpot CRM with persona segmentation
3. **Analyze** - Simulates engagement metrics and provides AI-powered optimization insights

The system supports dual AI models (OpenAI primary, Groq fallback) with automatic quota detection.

---

# Features

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

# Prerequisites

- **Python 3.10+**
- **OpenAI API Key** (primary) - [Get one here](https://platform.openai.com/api-keys)
- **Groq API Key** (fallback) - [Get one here](https://console.groq.com)
- **HubSpot Access Token** - [Free developer account](https://developers.hubspot.com/)

---

# Installation

```bash
# Clone the repository
git clone https://github.com/JZEHFEFN/novamind-ai-pipeline
cd novamind-pipeline

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate

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
```
# Configuration

Personas: Edit config/personas.py to modify personas:
Prompts: Edit prompts/prompts.txt to change AI prompts.
Demo Contacts: Edit config/mock_contacts.py to change demo contacts.

---

# HubSpot Setup

## Step 1: Create a HubSpot Developer Account

1. Go to [developers.hubspot.com](https://developers.hubspot.com/)
2. Click **"Get Started"** in the top right corner
3. Select **"Create a developer account"**
4. Fill in your email address and create a password
5. Verify your email address via the link sent to your inbox
6. Log in to your new developer account

> **Note:** Developer accounts are completely free and include API access for testing and development.

---

## Step 2: Create a Private App

1. In your developer account dashboard, navigate to **Apps** in the left sidebar
2. Click the **"Create app"** button
3. You'll see a warning about "Legacy App" - this is fine for our purposes. Click **"Continue"**
4. Select **"Private"** app type (for one account)
5. Fill in the app details:

| Field | Value |
|-------|-------|
| **App name** | `NovaMind AI Marketing Pipeline(Or anything you desire)` |
| **Description** | `AI-powered content generation and distribution pipeline(Or anything you desire)` |
| **Logo** | (Optional - skip) |

---

## Step 3: Configure Required Scopes

Under the **Scopes** section, you need to add the following permissions:

### Required Scopes

| Scope | Permission | Why Needed |
|-------|------------|------------|
| `crm.objects.contacts.read` | Read contacts | To fetch existing contacts |
| `crm.objects.contacts.write` | Create/update contacts | To create and update contacts |
| `crm.objects.contacts.sensitive.read` | Read sensitive contact data | To access email addresses |
| `crm.schemas.contacts.read` | Read contact properties | To check contact schema |
| `crm.objects.notes.read` | Read notes | To verify campaign logging |
| `crm.objects.notes.write` | Create notes | To log campaigns to contact timelines |

### How to Add Scopes

1. Click **"Add scopes"**
2. Search for each scope in the search bar
3. Check the box next to the scope
4. For scopes with multiple levels, select **"Read & Write"** where available
---

## Step 4: Generate Access Token

1. Scroll to the bottom of the page and click **"Create app"**
2. On the app dashboard, locate the **"Access token"** section
3. Click **"Generate token"**
4. A popup will appear with your access token

> ⚠️ **IMPORTANT**: Copy the token immediately and save it somewhere secure. You will only see it once!

The token will look like: pat-na1-xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx


---

## Step 5: Add Token to Your Project

1. Open your `.env` file in the project root:

```bash
nano .env
```
Add the HubSpot access token:
```bash
HUBSPOT_ACCESS_TOKEN=pat-na1-your-token-here
```
---
# Usage

```bash
python3 main.py --topic "Your topic here"
```

---
