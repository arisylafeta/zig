"""
Unipile API - LinkedIn Posts

This file contains functions for interacting with LinkedIn posts via the Unipile API.
"""

import json
from typing import List, Dict, Any, Optional, Union, Literal
from .config import get_base_url, get_headers, make_request, ensure_account_id, PaginatedResponse

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

async def get_user_posts(
    user_id: str,
    account_id: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: Optional[int] = None
) -> Any:
    """Retrieves posts published by a specific LinkedIn user.

    This function fetches the posts created by a particular LinkedIn user identified by their provider ID.
    The results include original posts, articles, and shared content. Results can be paginated using a cursor
    and limited to control the number of returned items.

    See https://docs.unipile.com/reference/linkedin-get-user-posts

    Args:
        user_id (str): The LinkedIn provider ID of the user whose posts you want to retrieve.
                      This is typically obtained from user profile information.
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.
        cursor (Optional[str]): A pagination cursor for retrieving the next set of posts.
                               This value is typically obtained from a previous API response.
        limit (Optional[int]): Maximum number of posts to return in a single request.

    Returns:
        Any: The raw API response containing a paginated list of LinkedIn post objects.

    Raises:
        Exception: If no user_id is provided or if there's an API error.
    """
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
    
    return response

async def get_user_comments(
    user_id: str,
    account_id: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: Optional[int] = None
) -> Any:
    """Retrieves comments made by a specific LinkedIn user.

    This function fetches the comments posted by a particular LinkedIn user identified by their provider ID.
    Results can be paginated using a cursor and limited to control the number of returned items.

    See https://docs.unipile.com/reference/linkedin-get-user-comments

    Args:
        user_id (str): The LinkedIn provider ID of the user whose comments you want to retrieve.
                      This is typically obtained from user profile information.
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.
        cursor (Optional[str]): A pagination cursor for retrieving the next set of comments.
                               This value is typically obtained from a previous API response.
        limit (Optional[int]): Maximum number of comments to return in a single request.

    Returns:
        Any: The raw API response containing a paginated list of LinkedIn comment objects.

    Raises:
        Exception: If no user_id is provided or if there's an API error.
    """
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
    
    return response

"""
Creates and publishes a new post on LinkedIn.

This function allows you to create and publish a new post on LinkedIn with specified text content
and visibility settings. The post will be published on behalf of the authenticated user.

Args:
    text (str): The content of the LinkedIn post. This can include text, hashtags, and mentions.
               LinkedIn may have character limits that apply to post content.
    visibility (Literal['connections', 'public']): Controls who can see the post:
                                                 - 'connections': Only your LinkedIn connections can see the post
                                                 - 'public': Anyone on LinkedIn can see the post
                                                 Default is 'connections'.
    account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                               the function will use the UNIPILE_ACCOUNT_ID environment variable.
    raw (bool): If True, returns the raw API response without cleaning. Default is False.

Returns:
    LinkedInPost: An object containing information about the created post:
        - Post ID and share URL
        - Post content
        - Publication timestamp
        - Initial engagement metrics (typically all zero)
        - Author information
        - Other post metadata

Raises:
    Exception: If no text is provided for the post or if there's an API error.

Example:
    ```python
    # Create a post visible to connections only
    new_post = await create_post("Excited to share my latest project! #innovation")
    
    # Create a public post
    public_post = await create_post(
        "Check out our company's new product launch!",
        visibility="public"
    )
    ```
"""
async def create_post(
    text: str,
    visibility: Literal['connections', 'public'] = 'connections',
    account_id: Optional[str] = None
) -> Any:
    """Creates and publishes a new post on LinkedIn.

    This function allows you to create and publish a new post on LinkedIn with specified text content
    and visibility settings. The post will be published on behalf of the authenticated user.

    See https://docs.unipile.com/reference/linkedin-create-post

    Args:
        text (str): The content of the LinkedIn post. This can include text, hashtags, and mentions.
                   LinkedIn may have character limits that apply to post content.
        visibility (Literal['connections', 'public']): Controls who can see the post:
                                                     - 'connections': Only your LinkedIn connections can see the post
                                                     - 'public': Anyone on LinkedIn can see the post
                                                     Default is 'connections'.
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.

    Returns:
        Any: The raw API response containing information about the created post.

    Raises:
        Exception: If no text is provided for the post or if there's an API error.
    """
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
    
    return response

async def get_post(
    post_id: str,
    account_id: Optional[str] = None
) -> Any:
    """Retrieves a specific LinkedIn post by its ID.

    This function fetches detailed information about a LinkedIn post identified by its unique ID.

    See https://docs.unipile.com/reference/linkedin-get-post

    Args:
        post_id (str): The unique identifier of the LinkedIn post to retrieve.
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.

    Returns:
        Any: The raw API response containing information about the requested post.

    Raises:
        Exception: If no post_id is provided or if there's an API error.
    """
    if not post_id:
        raise Exception('Post ID is required')
    
    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/posts/{post_id}?account_id={id_to_use}"
    
    response = await make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    return response

async def get_post_comments(
    post_id: str,
    account_id: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: Optional[int] = None
) -> Any:
    """Retrieves comments on a specific LinkedIn post.

    This function fetches the comments posted on a particular LinkedIn post identified by its ID.
    Results can be paginated using a cursor and limited to control the number of returned items.

    See https://docs.unipile.com/reference/linkedin-get-post-comments

    Args:
        post_id (str): The unique identifier of the LinkedIn post whose comments you want to retrieve.
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.
        cursor (Optional[str]): A pagination cursor for retrieving the next set of comments.
                               This value is typically obtained from a previous API response.
        limit (Optional[int]): Maximum number of comments to return in a single request.

    Returns:
        Any: The raw API response containing a paginated list of comments on the specified post.

    Raises:
        Exception: If no post_id is provided or if there's an API error.
    """
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
    
    return response

"""
Creates and publishes a comment on a LinkedIn post.

This function allows you to add a comment to an existing LinkedIn post identified by its ID.
The comment will be published on behalf of the authenticated user and will be visible to
anyone who can see the original post.

Args:
    post_id (str): The unique identifier of the LinkedIn post to comment on.
                  This is typically obtained from a previous call to get_user_posts() or similar functions.
    text (str): The content of the comment. This can include text, hashtags, and mentions.
               LinkedIn may have character limits that apply to comment content.
    account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                               the function will use the UNIPILE_ACCOUNT_ID environment variable.
    raw (bool): If True, returns the raw API response without cleaning. Default is False.

Returns:
    LinkedInComment: An object containing information about the created comment:
        - Comment ID
        - Comment text
        - Publication timestamp
        - Author information
        - Post ID the comment belongs to
        - Initial engagement metrics (typically all zero)
        - Other comment metadata

Raises:
    Exception: If no post_id or text is provided, or if there's an API error.

Example:
    ```python
    # Comment on a LinkedIn post
    new_comment = await comment_on_post(
        "post123456",
        "Great insights! I particularly agree with your point about..."
    )
    
    # The comment ID can be used for future reference
    comment_id = new_comment.get("id")
    ```
"""
async def comment_on_post(
    post_id: str,
    text: str,
    account_id: Optional[str] = None
) -> Any:
    """Creates and publishes a comment on a LinkedIn post.

    This function allows you to add a comment to an existing LinkedIn post identified by its ID.
    The comment will be published on behalf of the authenticated user and will be visible to
    anyone who can see the original post.

    See https://docs.unipile.com/reference/linkedin-comment-on-post

    Args:
        post_id (str): The unique identifier of the LinkedIn post to comment on.
                      This is typically obtained from a previous call to get_user_posts() or similar functions.
        text (str): The content of the comment. This can include text, hashtags, and mentions.
                   LinkedIn may have character limits that apply to comment content.
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.

    Returns:
        Any: The raw API response containing information about the created comment.

    Raises:
        Exception: If no post_id or text is provided, or if there's an API error.
    """
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
    
    return response