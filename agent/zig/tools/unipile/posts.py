"""
Unipile API - LinkedIn Posts

This file contains functions for interacting with LinkedIn posts via the Unipile API.
"""

import json
from typing import List, Dict, Any, Optional, Union, Literal
from .config import get_base_url, get_headers, make_request, ensure_account_id, PaginatedResponse
from .cleaners.posts import (
    clean_user_posts,
    clean_post_comments,
    clean_create_post_response,
    clean_comment_on_post_response
)

# Types
class LinkedInPostAuthor:
    public_identifier: str
    id: str
    name: str
    is_company: bool
    headline: Optional[str]

class LinkedInPostAttachment:
    type: str
    url: Optional[str]
    thumbnail_url: Optional[str]
    title: Optional[str]
    description: Optional[str]

class LinkedInPost:
    object: str
    provider: str
    social_id: str
    share_url: str
    date: str
    parsed_datetime: str
    comment_counter: int
    impressions_counter: int
    reaction_counter: int
    repost_counter: int
    permissions: Dict[str, bool]
    text: str
    attachments: List[LinkedInPostAttachment]
    author: LinkedInPostAuthor
    is_repost: Optional[bool]
    id: str
    repost_id: Optional[str]
    reposted_by: Optional[LinkedInPostAuthor]
    repost_content: Optional[Dict[str, Any]]

class LinkedInComment:
    object: str
    id: str
    post_id: str
    post_urn: str
    date: str
    author: str
    author_details: Dict[str, Any]
    text: str
    reaction_counter: int
    reply_counter: int

"""
Get posts from a specific LinkedIn user

@param user_id - The LinkedIn user's provider ID
@param account_id - Optional account ID (will use env var if not provided)
@param cursor - Optional cursor for pagination
@param limit - Optional limit for the number of results
@returns The user's LinkedIn posts
"""
async def get_user_posts(
    user_id: str,
    account_id: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    raw: bool = False
) -> Any:
    if not user_id:
        raise Exception('User ID is required')
    
    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    
    url = f"{base_url}/api/v1/users/{user_id}/posts?account_id={id_to_use}"
    if cursor:
        url += f"&cursor={cursor}"
    if limit:
        url += f"&limit={limit}"
    
    response = await make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_user_posts(response)

"""
Get comments from a specific LinkedIn user

@param user_id - The LinkedIn user's provider ID
@param account_id - Optional account ID (will use env var if not provided)
@param cursor - Optional cursor for pagination
@param limit - Optional limit for the number of results
@returns The user's LinkedIn comments
"""
async def get_user_comments(
    user_id: str,
    account_id: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    raw: bool = False
) -> Any:
    if not user_id:
        raise Exception('User ID is required')
    
    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    
    url = f"{base_url}/api/v1/users/{user_id}/comments?account_id={id_to_use}"
    if cursor:
        url += f"&cursor={cursor}"
    if limit:
        url += f"&limit={limit}"
    
    response = await make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_post_comments(response)

"""
Create a new LinkedIn post

@param text - The text of the post
@param visibility - The visibility of the post (connections or public)
@param account_id - Optional account ID (will use env var if not provided)
@returns The created post
"""
async def create_post(
    text: str,
    visibility: Literal['connections', 'public'] = 'connections',
    account_id: Optional[str] = None,
    raw: bool = False
) -> Any:
    if not text:
        raise Exception('Post text is required')
    
    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/posts"
    
    response = await make_request(url, {
        'method': 'POST',
        'headers': get_headers(),
        'body': json.dumps({
            'account_id': id_to_use,
            'text': text,
            'visibility': visibility
        })
    })
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_create_post_response(response)

"""
Get a specific LinkedIn post

@param post_id - The LinkedIn post ID
@param account_id - Optional account ID (will use env var if not provided)
@returns The LinkedIn post
"""
async def get_post(
    post_id: str,
    account_id: Optional[str] = None,
    raw: bool = False
) -> Any:
    if not post_id:
        raise Exception('Post ID is required')
    
    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/posts/{post_id}?account_id={id_to_use}"
    
    response = await make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    # Return raw response if raw is true
    if raw:
        return response
    
    # Otherwise clean and return
    # Using clean_post function which is internal to posts.py cleaner
    # We'll use a simplified version here
    return {
        'id': response.get('id'),
        'text': response.get('text'),
        'date': response.get('date'),
        'parsedDateTime': response.get('parsed_datetime'),
        'shareUrl': response.get('share_url'),
        'stats': {
            'comments': response.get('comment_counter'),
            'reactions': response.get('reaction_counter'),
            'reposts': response.get('repost_counter'),
            'impressions': response.get('impressions_counter')
        },
        'author': {
            'name': response.get('author', {}).get('name'),
            'headline': response.get('author', {}).get('headline'),
            'publicIdentifier': response.get('author', {}).get('public_identifier'),
            'isCompany': response.get('author', {}).get('is_company')
        } if response.get('author') else None
    }

"""
Get comments on a specific LinkedIn post

@param post_id - The LinkedIn post ID
@param account_id - Optional account ID (will use env var if not provided)
@param cursor - Optional cursor for pagination
@param limit - Optional limit for the number of results
@returns Comments on the LinkedIn post
"""
async def get_post_comments(
    post_id: str,
    account_id: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    raw: bool = False
) -> Any:
    if not post_id:
        raise Exception('Post ID is required')
    
    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    
    url = f"{base_url}/api/v1/posts/{post_id}/comments?account_id={id_to_use}"
    if cursor:
        url += f"&cursor={cursor}"
    if limit:
        url += f"&limit={limit}"
    
    response = await make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_post_comments(response)

"""
Comment on a LinkedIn post

@param post_id - The LinkedIn post ID
@param text - The content of the comment
@param account_id - Optional account ID (will use env var if not provided)
@returns The created comment
"""
async def comment_on_post(
    post_id: str,
    text: str,
    account_id: Optional[str] = None,
    raw: bool = False
) -> Any:
    if not post_id:
        raise Exception('Post ID is required')
    
    if not text:
        raise Exception('Comment text is required')
    
    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/posts/{post_id}/comments"
    
    response = await make_request(url, {
        'method': 'POST',
        'headers': get_headers(),
        'body': json.dumps({
            'account_id': id_to_use,
            'text': text
        })
    })
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_comment_on_post_response(response)