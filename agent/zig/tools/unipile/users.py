"""
Unipile API - LinkedIn Users

This file contains functions for interacting with LinkedIn users via the Unipile API.
"""

from .config import get_base_url, get_headers, make_request, ensure_account_id
from .cleaners.users import (
    clean_user_profile, 
    clean_account_owner_profile, 
    clean_user_relations, 
    clean_invitations_received, 
    clean_invitations_sent,
    clean_send_invitation_response
)
from typing import Dict, Any, List, Optional

# Types
class LinkedInUserProfile:
    object: str
    provider: str
    provider_id: str
    public_identifier: str
    member_urn: str
    first_name: str
    last_name: str
    headline: str
    primary_locale: Optional[Dict[str, str]]
    is_open_profile: bool
    is_premium: bool
    is_influencer: bool
    is_creator: bool
    is_relationship: bool
    is_self: bool
    websites: Optional[List[str]]
    follower_count: Optional[int]
    connections_count: Optional[int]
    location: Optional[str]
    contact_info: Optional[Dict[str, List[str]]]
    profile_picture_url: Optional[str]
    profile_picture_url_large: Optional[str]
    background_picture_url: Optional[str]

class LinkedInAccountOwnerProfile:
    object: str
    provider: str
    provider_id: str
    entity_urn: str
    object_urn: str
    first_name: str
    last_name: str
    profile_picture_url: str
    public_identifier: str
    occupation: str
    premium: bool
    open_profile: bool
    location: str
    email: str
    organizations: Optional[List[Dict[str, str]]]
    recruiter: Any
    sales_navigator: Any

class LinkedInUserRelation:
    object: str
    connection_urn: str
    created_at: int
    first_name: str
    last_name: str
    member_id: str
    member_urn: str
    headline: str
    public_identifier: str
    public_profile_url: str
    profile_picture_url: Optional[str]

class LinkedInInvitation:
    object: str
    id: str
    invited_user: str
    invited_user_id: Optional[str]
    invited_user_public_id: Optional[str]
    invited_user_description: Optional[str]
    date: str
    parsed_datetime: str
    invitation_text: Optional[str]
    inviter: Optional[Dict[str, str]]
    specifics: Optional[Dict[str, str]]

class LinkedInSearchResult:
    type: str
    industry: Optional[str]
    id: str
    name: str
    member_urn: str
    public_identifier: str
    profile_url: str
    public_profile_url: str
    profile_picture_url: Optional[str]
    profile_picture_url_large: Optional[str]
    network_distance: Optional[str]
    location: Optional[str]
    headline: Optional[str]
    verified: Optional[bool]

class LinkedInSearchResponse:
    object: str
    items: List[LinkedInSearchResult]
    config: Dict[str, Any]
    paging: Dict[str, int]
    cursor: Optional[str]

async def get_account_owner_profile(
    account_id: str = None
) -> Any:
    """Retrieves the LinkedIn profile of the currently authenticated user.
    
    This function fetches comprehensive profile information about the user who is currently
    authenticated with the provided account ID. This is useful for getting details about
    the user on whose behalf API calls are being made.
    
    See https://docs.unipile.com/reference/linkedin-get-account-owner-profile
    
    Args:
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.
    
    Returns:
        Any: The raw API response containing the authenticated user's profile information.
    
    Raises:
        Exception: If there's an API error during the request.
    """
    id = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/users/me?account_id={id}"
    
    response = make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    return response

async def get_user_profile_by_identifier(
    identifier: str,
    account_id: str = None
) -> Any:
    """Retrieves a LinkedIn user's profile by their public identifier.
    
    This function fetches comprehensive profile information about a LinkedIn user identified
    by their public identifier (the part of their LinkedIn profile URL after "linkedin.com/in/").
    The amount of information available may depend on the user's privacy settings and your
    connection level with them.
    
    See https://docs.unipile.com/reference/linkedin-get-user-profile
    
    Args:
        identifier (str): The LinkedIn user's public identifier (e.g., "johndoe" from 
                         linkedin.com/in/johndoe) or their provider ID.
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.
    
    Returns:
        Any: The raw API response containing the user's profile information.
    
    Raises:
        Exception: If no identifier is provided or if there's an API error.
    """
    if not identifier:
        raise Exception('User identifier is required')
    
    id = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/users/{identifier}?account_id={id}"
    
    response = make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    return response

async def search_linkedin(
    keywords: str,
    account_id: str = None,
    options: Dict[str, Any] = None
) -> LinkedInSearchResponse:
    """
    Search for LinkedIn users
    
    Args:
        keywords: The search keywords
        account_id: Optional account ID (will use env var if not provided)
        options: Optional search options
    
    Returns:
        LinkedIn search results
    """
    if not keywords:
        raise Exception('Search keywords are required')
    
    if options is None:
        options = {}
    
    id = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/linkedin/search?account_id={id}"
    
    return make_request(url, {
        'method': 'POST',
        'headers': get_headers(),
        'body': json.dumps({
            'api': options.get('api', 'classic'),
            'category': options.get('category', 'people'),
            'keywords': keywords,
            'account_id': id,
            'limit': options.get('limit', 10)
        })
    })

async def get_relations(
    account_id: str = None,
    cursor: str = None,
    limit: int = None,
    raw: bool = False
) -> Any:
    """
    Retrieves the authenticated user's LinkedIn connections (1st-degree network).
    
    This function fetches the list of LinkedIn users who are directly connected to the
    authenticated user (1st-degree connections). Results can be paginated using a cursor
    and limited to control the number of returned items.
    
    Args:
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.
        cursor (Optional[str]): A pagination cursor for retrieving the next set of connections.
                               This value is typically obtained from a previous API response.
        limit (Optional[int]): Maximum number of connections to return in a single request.
        raw (bool): If True, returns the raw API response without cleaning. Default is False.
    
    Returns:
        PaginatedResponse[LinkedInUserRelation]: A paginated list of LinkedIn connection objects, each containing:
            - Basic user information (first name, last name, headline)
            - Profile URLs and identifiers
            - Profile picture URL (if available)
            - Connection timestamp
            - Member URN and ID
            - Other connection metadata
    
    Example:
        ```python
        # Get all connections
        all_connections = await get_relations()
        
        # Get limited number of connections
        some_connections = await get_relations(limit=50)
        
        # Get next page of connections using cursor from previous response
        next_connections = await get_relations(cursor=all_connections.cursor)
        
        # Print connection names
        for connection in all_connections.items:
            print(f"{connection.first_name} {connection.last_name} - {connection.headline}")
        ```
    """
    id = ensure_account_id(account_id)
    base_url = get_base_url()
    
    url = f"{base_url}/api/v1/users/relations?account_id={id}"
    if cursor:
        url += f"&cursor={cursor}"
    if limit:
        url += f"&limit={limit}"
    
    response = make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_user_relations(response)

async def get_invitations_sent(
    account_id: str = None,
    cursor: str = None,
    limit: int = None,
    raw: bool = False
) -> Any:
    """
    Get invitations sent by the user
    
    Args:
        account_id: Optional account ID (will use env var if not provided)
        cursor: Optional cursor for pagination
        limit: Optional limit for the number of results
        raw: Whether to return the raw API response
    
    Returns:
        Invitations sent by the user
    """
    id = ensure_account_id(account_id)
    base_url = get_base_url()
    
    url = f"{base_url}/api/v1/users/invite/sent?account_id={id}"
    if cursor:
        url += f"&cursor={cursor}"
    if limit:
        url += f"&limit={limit}"
    
    response = make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_invitations_sent(response)

async def get_invitations_received(
    account_id: str = None,
    cursor: str = None,
    limit: int = None,
    raw: bool = False
) -> Any:
    """
    Get invitations received by the user
    
    Args:
        account_id: Optional account ID (will use env var if not provided)
        cursor: Optional cursor for pagination
        limit: Optional limit for the number of results
        raw: Whether to return the raw API response
    
    Returns:
        Invitations received by the user
    """
    id = ensure_account_id(account_id)
    base_url = get_base_url()
    
    url = f"{base_url}/api/v1/users/invite/received?account_id={id}"
    if cursor:
        url += f"&cursor={cursor}"
    if limit:
        url += f"&limit={limit}"
    
    response = make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_invitations_received(response)

async def send_invitation(
    recipient_provider_id: str,
    message: str = None,
    account_id: str = None,
    raw: bool = False
) -> Any:
    """
    Sends a LinkedIn connection request to another user.
    
    This function allows you to send a connection request (invitation) to a LinkedIn user
    identified by their provider ID. You can optionally include a personalized message with
    the invitation to increase the likelihood of acceptance.
    
    Args:
        recipient_provider_id (str): The LinkedIn provider ID of the person to invite.
                                    This is typically obtained from user profile information.
        message (Optional[str]): A personalized message to include with the connection request.
                                LinkedIn limits this to 300 characters.
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.
        raw (bool): If True, returns the raw API response without cleaning. Default is False.
    
    Returns:
        Dict[str, Any]: An object containing information about the sent invitation:
            - Status of the invitation (pending, sent, etc.)
            - Timestamp of when the invitation was sent
            - Recipient information
            - Other invitation metadata
    
    Raises:
        Exception: If no recipient_provider_id is provided or if there's an API error.
    
    Example:
        ```python
        # Send a connection request with a personalized message
        invitation = await send_invitation(
            "recipient123456",
            "Hi! I enjoyed your recent post about AI developments and would love to connect."
        )
        
        # Send a connection request without a message
        simple_invitation = await send_invitation("recipient789012")
        ```
    
    Note:
        LinkedIn has rate limits and restrictions on connection requests. Sending too many
        requests in a short period may result in temporary restrictions on your account.
    """
    if not recipient_provider_id:
        raise Exception('Recipient Provider ID is required')
    
    id = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/users/invite"
    
    body = {
        'account_id': id,
        'provider_id': recipient_provider_id
    }
    
    if message:
        body['message'] = message
    
    response = make_request(url, {
        'method': 'POST',
        'headers': get_headers(),
        'body': json.dumps(body)
    })
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_send_invitation_response(response)