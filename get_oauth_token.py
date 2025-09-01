# a script to get my oauth token instead of having to build a frontend for it for now

from google_auth_oauthlib.flow import Flow

def get_my_credentials():
    flow = Flow.from_client_secrets_file(
        './secrets/credentials.json',
        scopes=['https://www.googleapis.com/auth/drive'],
    )
    flow.redirect_uri = 'http://localhost:8080'

    auth_url, _ = flow.authorization_url()
    print(f"Please go to this URL: {auth_url}")

    code = input("Enter the authorization code: ")
    flow.fetch_token(code=code)

    with open('my_token.json', 'w') as f:
        f.write(flow.credentials.to_json())

if __name__ == '__main__':
    get_my_credentials()
