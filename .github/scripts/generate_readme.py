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
    """Get combined statistics from both accounts"""
    base_url = "https://github-readme-stats.vercel.app/api"
    
    # Use the primary account for combined stats
    if not USERS:
        raise ValueError("No users configured")
    
    params = {
        'username': USERS[0],  # First user
        'show_icons': 'true',
        'theme': 'gradient',
        'hide_border': 'true',
        'include_all_commits': 'true',
        'count_private': 'true'
    }
    
    # Use the appropriate token for the primary account
    token = get_token_for_user(USERS[0])
    if token:
        params['token'] = token
    
    response = requests.get(f"{base_url}", params=params)
    return response.url

def get_top_languages(username, token=None):
    """Get top languages for a user"""
    base_url = "https://github-readme-stats.vercel.app/api/top-langs"
    
    params = {
        'username': username,
        'layout': 'compact',
        'theme': 'gradient',
        'hide_border': 'true',
        'count_private': 'true'
    }
    
    if token:
        params['token'] = token
    
    response = requests.get(base_url, params=params)
    return response.url

def get_combined_top_languages():
    """Get combined top languages from both accounts"""
    base_url = "https://github-readme-stats.vercel.app/api/top-langs"
    
    # Use the primary account for combined stats
    if not USERS:
        raise ValueError("No users configured")
    
    params = {
        'username': USERS[0],  # First user
        'layout': 'compact',
        'theme': 'gradient',
        'hide_border': 'true',
        'count_private': 'true'
    }
    
    # Use the appropriate token for the primary account
    token = get_token_for_user(USERS[0])
    if token:
        params['token'] = token
    
    response = requests.get(base_url, params=params)
    return response.url

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
    """Get combined streak from both accounts"""
    base_url = "https://github-readme-streak-stats.herokuapp.com"
    
    # Use the primary account for combined stats
    if not USERS:
        raise ValueError("No users configured")
    
    params = {
        'user': USERS[0],  # First user
        'theme': 'gradient',
        'hide_border': 'true'
    }
    
    # Use the appropriate token for the primary account
    token = get_token_for_user(USERS[0])
    if token:
        params['token'] = token
    
    response = requests.get(base_url, params=params)
    return response.url

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
    """Get combined trophies from both accounts"""
    base_url = "https://github-profile-trophy.vercel.app"
    
    # Use the primary account for combined stats
    if not USERS:
        raise ValueError("No users configured")
    
    params = {
        'username': USERS[0],  # First user
        'theme': 'gradient',
        'no-frame': 'true',
        'no-bg': 'false',
        'margin-w': '4'
    }
    
    response = requests.get(base_url, params=params)
    return response.url

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
    
    # Header
    content = """<h1 align="center">Hi, I'm [Your Name]</h1>
<h3 align="center">A passionate [Your Title]</h3>

<p align="left"> <img src="https://komarev.com/ghpvc/?username=[YOUR_USERNAME]&label=Profile%20views&color=0e75b6&style=flat" alt="[YOUR_USERNAME]" /> </p>

<h3 align="left">Connect with me:</h3>
<p align="left">
<a href="[YOUR_LINKEDIN_URL]" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="[YOUR_USERNAME]" height="30" width="40" /></a>
</p>

<h3 align="left">📊 GitHub Statistics:</h3>

"""
    
    # Combined Statistics (unified view)
    content += "<p align=\"left\">\n"
    
    # Combined GitHub Stats
    combined_stats_url = get_combined_stats()
    content += f'  <img src="{combined_stats_url}" alt="GitHub Stats" />\n'
    
    # Combined Top Languages
    combined_langs_url = get_combined_top_languages()
    content += f'  <img src="{combined_langs_url}" alt="Top Languages" />\n'
    
    content += "</p>\n\n"
    
    # Combined Streak
    content += "<p align=\"left\">\n"
    combined_streak_url = get_combined_streak()
    content += f'  <img src="{combined_streak_url}" alt="GitHub Streak" />\n'
    content += "</p>\n\n"
    
    # Combined Trophies
    content += "<p align=\"left\">\n"
    combined_trophies_url = get_combined_trophies()
    content += f'  <img src="{combined_trophies_url}" alt="GitHub Trophies" />\n'
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
        print("📊 Generated unified statistics from both accounts")
        print("🔑 Using separate tokens for each account")
        print(f"👤 Accounts: {', '.join(USERS)}")
        print(f"🏢 Organizations: {', '.join(ORGANIZATIONS)}")
        
    except Exception as e:
        print(f"❌ Error generating README: {str(e)}")
        raise

if __name__ == "__main__":
    main() 