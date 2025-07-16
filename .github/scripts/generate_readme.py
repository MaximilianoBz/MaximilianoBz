#!/usr/bin/env python3
"""
Script to generate README.md with GitHub statistics
Includes private repositories and organization contributions
"""

import os
import requests
from github import Github
from datetime import datetime
import json

# Configuration
PERSONAL_TOKEN_A = os.getenv('PERSONAL_TOKEN_A')
PERSONAL_TOKEN_B = os.getenv('PERSONAL_TOKEN_B')

# Get users and organizations from environment variables
USERS_ENV = os.getenv('USERS')
ORGANIZATIONS_ENV = os.getenv('ORGANIZATIONS')

# Clean and split the lists, use defaults if not provided
if USERS_ENV:
    USERS = [user.strip() for user in USERS_ENV.split(',') if user.strip()]
else:
    USERS = ['user1', 'user2']  # Generic default users

if ORGANIZATIONS_ENV:
    ORGANIZATIONS = [org.strip() for org in ORGANIZATIONS_ENV.split(',') if org.strip()]
else:
    ORGANIZATIONS = ['org1', 'org2']  # Generic default organizations

def get_github_stats(username, token=None):
    """Get GitHub statistics for a user"""
    base_url = "https://github-readme-stats.vercel.app/api"
    
    params = {
        'username': username,
        'show_icons': 'true',
        'theme': 'gradient',
        'hide_border': 'true',
        'include_all_commits': 'true',
        'count_private': 'true'
    }
    
    if token:
        params['token'] = token
    
    response = requests.get(f"{base_url}", params=params)
    return response.url

def get_token_for_user(username):
    """Get the appropriate token for a user"""
    if len(USERS) >= 1 and username == USERS[0]:  # First user gets token A
        return PERSONAL_TOKEN_A
    elif len(USERS) >= 2 and username == USERS[1]:  # Second user gets token B
        return PERSONAL_TOKEN_B
    return None

def get_combined_stats():
    """Get combined statistics from all accounts"""
    # Since GitHub stats API doesn't support multiple usernames in one URL,
    # we'll show stats for each account separately
    stats_urls = []
    
    for i, username in enumerate(USERS):
        token = get_token_for_user(username)
        stats_url = get_github_stats(username, token)
        stats_urls.append(stats_url)
    
    return stats_urls

def get_streak_stats(username, token=None):
    """Get streak statistics for a user"""
    base_url = "https://github-readme-streak-stats.herokuapp.com"
    
    params = {
        'user': username,
        'theme': 'gradient',
        'hide_border': 'true'
    }
    
    if token:
        params['token'] = token
    
    response = requests.get(base_url, params=params)
    return response.url

def get_combined_streak():
    """Get combined streak from all accounts"""
    # Since GitHub streak API doesn't support multiple usernames in one URL,
    # we'll show streak for each account separately
    streak_urls = []
    
    for i, username in enumerate(USERS):
        token = get_token_for_user(username)
        streak_url = get_streak_stats(username, token)
        streak_urls.append(streak_url)
    
    return streak_urls

def get_trophy_stats(username, token=None):
    """Get trophy statistics for a user"""
    base_url = "https://github-profile-trophy.vercel.app"
    
    params = {
        'username': username,
        'theme': 'gradient',
        'no-frame': 'true',
        'no-bg': 'false',
        'margin-w': '4'
    }
    
    response = requests.get(base_url, params=params)
    return response.url

def get_combined_trophies():
    """Get combined trophies from all accounts"""
    # Since GitHub trophy API doesn't support multiple usernames in one URL,
    # we'll show trophies for each account separately
    trophy_urls = []
    
    for i, username in enumerate(USERS):
        token = get_token_for_user(username)
        trophy_url = get_trophy_stats(username, token)
        trophy_urls.append(trophy_url)
    
    return trophy_urls

def get_organization_stats(org_name):
    """Get organization statistics"""
    base_url = "https://github-readme-stats.vercel.app/api"
    
    # Determine theme based on organization position
    if ORGANIZATIONS and org_name == ORGANIZATIONS[0]:
        theme = 'merko'
    else:
        theme = 'tokyonight'
    
    params = {
        'username': org_name,
        'show_icons': 'true',
        'theme': theme,
        'hide_border': 'true',
        'hide_title': 'true'
    }
    
    response = requests.get(base_url, params=params)
    return response.url

def generate_readme_content():
    """Generate the complete README content"""
    
    # Load config for profile info
    try:
        with open('.github/scripts/config.json', 'r') as f:
            config = json.load(f)
        profile_name = config.get('profile', {}).get('name', '[Your Name]')
        profile_title = config.get('profile', {}).get('title', 'A passionate [Your Title]')
        profile_linkedin = config.get('profile', {}).get('linkedin', '[YOUR_LINKEDIN_URL]')
    except:
        profile_name = '[Your Name]'
        profile_title = 'A passionate [Your Title]'
        profile_linkedin = '[YOUR_LINKEDIN_URL]'
    
    # Header
    content = f"""<h1 align="center">Hi, I'm {profile_name}</h1>
<h3 align="center">{profile_title}</h3>

<p align="left"> <img src="https://komarev.com/ghpvc/?username={USERS[0] if USERS else '[YOUR_USERNAME]'}&label=Profile%20views&color=0e75b6&style=flat" alt="{USERS[0] if USERS else '[YOUR_USERNAME]'}" /> </p>

<h3 align="left">Connect with me:</h3>
<p align="left">
<a href="{profile_linkedin}" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="{USERS[0] if USERS else '[YOUR_USERNAME]'}" height="30" width="40" /></a>
</p>

<h3 align="left">📊 GitHub Statistics:</h3>

"""
    
    # Individual Account Statistics
    if len(USERS) > 1:
        content += "<h4 align=\"left\">📈 Individual Account Stats:</h4>\n\n"
        
        for i, username in enumerate(USERS):
            token = get_token_for_user(username)
            
            # GitHub Stats for this account
            stats_url = get_github_stats(username, token)
            content += f"<p align=\"left\">\n"
            content += f'  <img src="{stats_url}" alt="GitHub Stats - {username}" />\n'
            content += "</p>\n\n"
            
            # Streak Stats for this account
            streak_url = get_streak_stats(username, token)
            content += f"<p align=\"left\">\n"
            content += f'  <img src="{streak_url}" alt="GitHub Streak - {username}" />\n'
            content += "</p>\n\n"
            
            # Trophy Stats for this account
            trophy_url = get_trophy_stats(username, token)
            content += f"<p align=\"left\">\n"
            content += f'  <img src="{trophy_url}" alt="GitHub Trophies - {username}" />\n'
            content += "</p>\n\n"
    else:
        # Single account - show unified stats
        username = USERS[0] if USERS else '[YOUR_USERNAME]'
        token = get_token_for_user(username)
        
        # GitHub Stats
        stats_url = get_github_stats(username, token)
        content += f"<p align=\"left\">\n"
        content += f'  <img src="{stats_url}" alt="GitHub Stats" />\n'
        content += "</p>\n\n"
        
        # Streak Stats
        streak_url = get_streak_stats(username, token)
        content += f"<p align=\"left\">\n"
        content += f'  <img src="{streak_url}" alt="GitHub Streak" />\n'
        content += "</p>\n\n"
        
        # Trophy Stats
        trophy_url = get_trophy_stats(username, token)
        content += f"<p align=\"left\">\n"
        content += f'  <img src="{trophy_url}" alt="GitHub Trophies" />\n'
        content += "</p>\n\n"
    
    # Organization Statistics (if configured)
    if ORGANIZATIONS and ORGANIZATIONS != ['org1', 'org2']:
        content += "<h4 align=\"left\">🏢 Organization Contributions:</h4>\n\n"
        
        for org_name in ORGANIZATIONS:
            if org_name and org_name not in ['org1', 'org2']:
                org_stats_url = get_organization_stats(org_name)
                content += f"<p align=\"left\">\n"
                content += f'  <img src="{org_stats_url}" alt="{org_name} Stats" />\n'
                content += "</p>\n\n"
    
    # Languages and Tools
    content += """<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://aws.amazon.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" alt="aws" width="40" height="40"/> </a> <a href="https://azure.microsoft.com/en-in/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/microsoft_azure/microsoft_azure-icon.svg" alt="azure" width="40" height="40"/> </a> <a href="https://www.gnu.org/software/bash/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/gnu_bash/gnu_bash-icon.svg" alt="bash" width="40" height="40"/> </a> <a href="https://cassandra.apache.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/apache_cassandra/apache_cassandra-icon.svg" alt="cassandra" width="40" height="40"/> </a> <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a> <a href="https://www.elastic.co" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/elastic/elastic-icon.svg" alt="elasticsearch" width="40" height="40"/> </a> <a href="https://cloud.google.com" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/google_cloud/google_cloud-icon.svg" alt="gcp" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://grafana.com" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/grafana/grafana-icon.svg" alt="grafana" width="40" height="40"/> </a> <a href="https://www.jenkins.io" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/jenkins/jenkins-icon.svg" alt="jenkins" width="40" height="40"/> </a> <a href="https://kafka.apache.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/apache_kafka/apache_kafka-icon.svg" alt="kafka" width="40" height="40"/> </a> <a href="https://www.elastic.co/kibana" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/elasticco_kibana/elasticco_kibana-icon.svg" alt="kibana" width="40" height="40"/> </a> <a href="https://kubernetes.io" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/kubernetes/kubernetes-icon.svg" alt="kubernetes" width="40" height="40"/> </a> <a href="https://www.linux.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="40" height="40"/> </a> <a href="https://mariadb.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/mariadb/mariadb-icon.svg" alt="mariadb" width="40" height="40"/> </a> <a href="https://www.mysql.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" alt="mysql" width="40" height="40"/> </a> <a href="https://www.nginx.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nginx/nginx-original.svg" alt="nginx" width="40" height="40"/> </a> <a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> <a href="https://postman.com" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/getpostman/getpostman-icon.svg" alt="postman" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://redis.io" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/redis/redis-original-wordmark.svg" alt="redis" width="40" height="40"/> </a> <a href="https://www.scala-lang.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/scala/scala-original.svg" alt="scala" width="40" height="40"/> </a> </p>

"""
    
    # Footer with last update
    content += f"""
---

<p align="center">
  <i>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</i>
</p>
"""
    
    return content

def main():
    """Main function to generate and write README"""
    try:
        print("🚀 Generating README with GitHub statistics...")
        
        # Validate configuration
        if not PERSONAL_TOKEN_A or not PERSONAL_TOKEN_B:
            print("⚠️  Warning: One or both tokens are not configured")
        
        if len(USERS) < 2:
            print("⚠️  Warning: USERS should contain at least 2 users")
        
        if len(ORGANIZATIONS) < 1:
            print("⚠️  Warning: ORGANIZATIONS should contain at least 1 organization")
        
        # Generate content
        content = generate_readme_content()
        
        # Write to README.md
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ README.md generated successfully!")
        if len(USERS) > 1:
            print("📊 Generated individual statistics for each account")
        else:
            print("📊 Generated unified statistics")
        print("🔑 Using separate tokens for each account")
        print(f"👤 Accounts: {', '.join(USERS)}")
        print(f"🏢 Organizations: {', '.join(ORGANIZATIONS)}")
        
    except Exception as e:
        print(f"❌ Error generating README: {str(e)}")
        raise

if __name__ == "__main__":
    main() 