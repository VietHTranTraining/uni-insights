from watson_developer_cloud import PersonalityInsightsV3;
from json import *;
import os

personality_insights = PersonalityInsightsV3(
        version='2017-10-13',
        username='ae988efb-4838-48df-ba48-030886ab441e',
        password='Fo0OlxVEnPcM',
        url='https://gateway.watsonplatform.net/personality-insights/api'
)

def anaylyze_user(file_name):
    with open(file_name) as profile:
        profile = personality_insights.profile(
                profile.read(),
                content_type='text/plain',
                consumption_preferences=True,
                raw_scores=True
                )
        return profile

def anaylyze_user_json(file_name):
    with open(file_name) as profile:
        profile = personality_insights.profile(
                profile.read(),
                content_type='application/json',
                consumption_preferences=True,
                raw_scores=True
                )
        return profile

def anaylyze_user_text(text):
    file_name = './essay.tmp'
    with open(file_name, 'w') as f:
        f.write(text)
    with open(file_name) as profile:
        profile = personality_insights.profile(
                profile.read(),
                content_type='text/plain',
                consumption_preferences=True,
                raw_scores=True
                )
        os.remove(file_name)
        return profile

