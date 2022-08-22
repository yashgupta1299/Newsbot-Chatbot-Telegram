import os
from gnewsclient import gnewsclient
from google.cloud import dialogflow_v2beta1 as dialogflow

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client.json"
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "news-bot-oosg"

client = gnewsclient.NewsClient()

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result


def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)

    if response.intent.display_name == 'get_news':
        return "get_news", dict(response.parameters)
    else:
        return "small_talk", response.fulfillment_text


def fetch_news(parameters):
    client.language = parameters.get('language')
    client.location = parameters.get('geo-country')
    client.topic = parameters.get('topic')
    if client.language=="" :
        client.language = 'English'
    
    if client.location=="" :
        client.location = 'India'
    
    if client.topic=="" or client.topic.lower()=="news" or \
        client.topic=="Top Stories":
        client.topic = 'Science'
    
    return client.get_news()[:5]

topics_keyboard = [
    ['Top Stories', 'World', 'Nation'], 
    ['Business', 'Technology', 'Entertainment'], 
    ['Sports', 'Science', 'Health']
]