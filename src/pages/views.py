import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from django.shortcuts import redirect, render
from django.conf import settings


# Create your views here.



def google_authenticate(request):
    # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow steps
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=settings.GOOGLE_SCOPES
    )

    # Generate the authorization URL
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    # Save the state in the session to verify the callback later
    request.session['oauth_state'] = state

    return redirect(authorization_url)

def oauth2callback(request):
    state = request.session['oauth_state']
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=settings.GOOGLE_SCOPES,
        state=state
    )

    # Exchange the authorization code for credentials
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    return redirect('list_reviews')  # Redirect to a view that lists reviews

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
