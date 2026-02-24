import msal
from src.logger import get_logger

logger = get_logger(__name__)

def authentication(client_id, AUTHORITY, client_secret, SCOPE):
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=AUTHORITY,
        client_credential=client_secret,
    )

    token_result = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" not in token_result:
        logger.error(f"Failed to acquire access token. Error: {token_result.get('error')}, Description: {token_result.get('error_description')}")
        raise Exception("Failed to get access token")

    access_token = token_result["access_token"]

    return access_token