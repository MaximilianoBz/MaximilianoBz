#!/usr/bin/env python3
"""
Script to inject dynamic GitHub stats into README.md without overwriting the manual content.
"""

import os
import requests
from datetime import datetime

# Configuration
PERSONAL_TOKEN_A = os.getenv('PERSONAL_TOKEN_A')
PERSONAL_TOKEN_B = os.getenv('PERSONAL_TOKEN_B')
USERS_ENV = os.getenv('USERS')
ORGANIZATIONS_ENV = os.getenv('ORGANIZATIONS')

# Users and Organizations
USERS = [u.strip() for u in USERS_ENV.split(',')] if USERS_ENV else ['MaximilianoBz']
ORGANIZATIONS = [o.strip() for o in ORGANIZATIONS_ENV.split(',')] if ORGANIZATIONS_ENV else []

def get_github_stats(username, token=None):
    """Generate GitHub stats URL for a user"""
    base_url = "https://github-readme-stats.vercel.app/api"
    params = {
        'username': username,
        'show_icons': 'true',
        'theme': 'gruvbox',
        'hide_border': 'true',
        'include_all_commits': 'true',
        'count_private': 'true'
    }
    if token:
        params['token'] = token
    response = requests.get(base_url, params=params)
    return response.url

def get_streak_stats(username, token=None):
    """Generate GitHub streak URL for a user"""
    base_url = "https://github-readme-streak-stats.herokuapp.com"
    params = {
        'user': username,
        'theme': 'gruvbox',
        'hide_border': 'true'
    }
    if token:
        params['token'] = token
    response = requests.get(base_url, params=params)
    return response.url

def get_trophy_stats(username):
    """Generate GitHub trophy URL for a user"""
    base_url = "https://github-profile-trophy.vercel.app"
    params = {
        'username': username,
        'theme': 'gruvbox',
        'no-frame': 'true',
        'no-bg': 'false',
        'margin-w': '4'
    }
    response = requests.get(base_url, params=params)
    return response.url

def generate_dynamic_content():
    """Generate the dynamic stats block for insertion"""
    content = "<!-- STATS_START -->\n"
    for i, username in enumerate(USERS):
        token = PERSONAL_TOKEN_A if i == 0 else PERSONAL_TOKEN_B
        stats_url = get_github_stats(username, token)
        streak_url = get_streak_stats(username, token)
        trophy_url = get_trophy_stats(username)

        content += f"\n### GitHub Stats for {username}\n"
        content += f'<p align="center">\n'
        content += f'  <img src="{stats_url}" alt="GitHub Stats - {username}" />\n'
        content += f'  <img src="{streak_url}" alt="GitHub Streak - {username}" />\n'
        content += f'  <img src="{trophy_url}" alt="GitHub Trophies - {username}" />\n'
        content += '</p>\n'

    content += f"\n_Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}_\n"
    content += "<!-- STATS_END -->\n"
    return content

def main():
    """Main function to inject dynamic stats into README.md"""
    readme_file = "README.md"
    
    if not os.path.exists(readme_file):
        print(f"❌ {readme_file} not found.")
        return

    with open(readme_file, 'r', encoding='utf-8') as f:
        content = f.read()

    dynamic_content = generate_dynamic_content()

    # Replace content between markers
    import re
    pattern = r"<!-- STATS_START -->.*?<!-- STATS_END -->"
    if re.search(pattern, content, flags=re.DOTALL):
        content_new = re.sub(pattern, dynamic_content, content, flags=re.DOTALL)
    else:
        # If markers not found, append at the end
        content_new = content + "\n\n" + dynamic_content

    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(content_new)

    print("✅ README.md updated with dynamic GitHub stats.")

if __name__ == "__main__":
    main()
