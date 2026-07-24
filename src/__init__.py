#!/usr/bin/env python3
"""Repository Initialization Script - Agent Pipe Contributors Page Generator."""

import json
from pathlib import Path


def generate_contributors_page():
    """Generate HTML content for the contributors page with golden egg decorations and goose imagery.*/

    def create_portrait_agent(agent_name, persona):
        # Use a placeholder image URL that looks like a generic corporate office setting (goose people)
        portrait_url = f"https://images.unsplash.com/photo-1573496210980-caa8fbaeebde?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"

        return {
            "name": f"{agent_name} ({persona})",
            "avatar_url": portrait_url,
            "role_description": agent_name + ": A contributing Agent from the C-Suite of AgentPipe",
            "birthplace_agent_profile": f"https://github.com/{agent_name}",
            "signature_note": f"Agent {agent_name}: Your contributions are invaluable to our team."
        }

    # Define agents with golden egg decorations (emoji or text-based) and portrait URLs
    agent_data = [
        ("Mischievous Agent", "<span style='background-color: gold; color: black;'>🎲</span>"),
        ("Grumpy Agent", "<span style='background-color: orange-red; color: white;'>😐</span>"),
        ("The Golden Egg Collector", "<span style='font-size: 12px; background-color: #ffd700; font-weight: bold;' border-radius: 50%; padding: 4px;">🪙✨</span>" + " (Golden Legend)" if False else None,
        ("The Silent Guardian", "<span style='background-color: silver-900; color: gold;'>💎</span>"),
    ]

    # Create HTML skeleton for contributors page with golden eggs and goose imagery
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Congratulations, Contributors!</title>
<style>
/* Golden Egg Decorations */
.golden-egg {
  font-size: 10px; /* Small enough to be readable without specific sizing rules in this context */
}

#hero-image {{
  width: 120%;
  height: auto;
}}

#contributor-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 40px;
    padding: 60px 80px;
}

/* Hero Section */
.hero-section {{
    text-align: center;
}}

#hero-image img {
  width: 100%;
  height: auto;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

/* Golden Egg Decorations */
.golden-egg {
    background-color: #ffd700; /* Gold color for golden eggs */
    padding: 2px 6px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 10px;
}

#contributor-grid {{
    max-width: 980px;
}}

/* Individual Contributor Cards */
.contributor-card {{
    background-color: #f4e6c2; /* Lightened gold/cream color for contrast with golden eggs */
    border-radius: 15px;
    overflow: hidden;
}

#contributor-grid .agent-section {{
    padding-bottom: 30px;
}}

.agent-name-box {{
    display: inline-block;
    background-color: #d4cfcf; /* Slightly darker than card bg */
    border-radius: 12px;
}

#contributor-grid .agent-section h3, 
#contributor-grid .agent-section p {{
    color: #5a6870; /* Darker text for readability on gold cards */
}}

/* Golden Egg Decorations in individual sections */
.golden-egg-in-card {{
    background-color: #ffd700;
    padding: 1px 4px;
    border-radius: 50%;
    font-size: 8px; /* Smaller for card content area */
}}

#contributor-grid .agent-section h3, 
.golden-egg-in-card {{
    color: #d69e7c; /* Slightly darker
