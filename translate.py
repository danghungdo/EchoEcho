import requests, os, uuid, pyperclip, keyboard

from win10toast import ToastNotifier
from dotenv import load_dotenv

# Load .env
load_dotenv()

api_key = os.environ['KEY']
endpoint = os.environ['ENDPOINT']
location = os.environ['LOCATION']

target_language = 'en'
path = '/translate?api-version=3.0'
target_language_parameter = '&to=' + target_language
url = endpoint + path + target_language_parameter

# Header information
headers = {
    'Ocp-Apim-Subscription-Key': api_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}
# Window notification
toaster = ToastNotifier()


def main():
    while True:
        try:
            # Wait for keys press
            key = keyboard.read_event()
            if key.name == 'esc':
                break
            if key.name == 'f2':
                original_text = pyperclip.paste()
                body = [{'text': original_text}]
                # POST to Azure Translator
                translator_request = requests.post(url, headers=headers, json=body)
                translator_response = translator_request.json()
                translated_text = translator_response[0]['translations'][0]['text']
                # Display the result
                toaster.show_toast(title='DE to EN', msg=translated_text, duration=10)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
    print('Exiting the program!')