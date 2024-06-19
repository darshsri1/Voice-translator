import requests

# Replace with your Flask server URL
BASE_URL = 'http://127.0.0.1:5000/'

def test_answer_endpoint(url, question, lang='en'):
    endpoint = f"{BASE_URL}/answer"
    params = {
        'url': url,
        'question': question,
        'lang': lang
    }
    response = requests.get(endpoint, params=params)
    return response.json()

if __name__ == '__main__':
    # Example usage
    youtube_url = 'https://www.youtube.com/watch?v=FTxsXHFhBPE'
    question = "What is this video about?"
    target_language = 'hi'  # Change to 'en' or any other supported language code

    result = test_answer_endpoint(youtube_url, question, target_language)
    print("Response:")
    print(result)
