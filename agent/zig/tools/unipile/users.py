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
    account_id: str = None,
    raw: bool = False
) -> Any:
    """
    Get the profile of the authenticated LinkedIn user
    
    Args:
        account_id: Optional account ID (will use env var if not provided)
        raw: Whether to return the raw API response
    
    Returns:
        The LinkedIn account owner profile
    """
    id = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/users/me?account_id={id}"
    
    response = make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_account_owner_profile(response)

async def get_user_profile_by_identifier(
    identifier: str,
    account_id: str = None,
    raw: bool = False
) -> Any:
    """
    Get a LinkedIn user's profile by their public identifier
    
    Args:
        identifier: The LinkedIn user's public identifier (e.g., "johndoe")
        account_id: Optional account ID (will use env var if not provided)
        raw: Whether to return the raw API response
    
    Returns:
        The LinkedIn user profile
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
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_user_profile(response)

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
    Get the user's LinkedIn connections
    
    Args:
        account_id: Optional account ID (will use env var if not provided)
        cursor: Optional cursor for pagination
        limit: Optional limit for the number of results
        raw: Whether to return the raw API response
    
    Returns:
        The user's LinkedIn connections
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
    Send a LinkedIn connection request
    
    Args:
        recipient_provider_id: The LinkedIn provider ID of the person to invite
        message: Optional message to include with the invitation
        account_id: Optional account ID (will use env var if not provided)
        raw: Whether to return the raw API response
    
    Returns:
        The result of the invitation request
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