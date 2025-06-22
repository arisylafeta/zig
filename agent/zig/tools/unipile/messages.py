"""
Unipile API - LinkedIn Messages

This file contains functions for interacting with LinkedIn messages via the Unipile API.
"""

import json
from typing import List, Dict, Any, Optional, Union
from .config import get_base_url, get_headers, make_request, ensure_account_id, PaginatedResponse
from langchain_core.tools import tool

# Types
class LinkedInChat:
    object: str
    name: Optional[str]
    type: int
    folder: List[str]
    unread: int
    archived: int
    read_only: int
    timestamp: str
    account_id: str
    muted_until: Optional[str]
    provider_id: str
    account_type: str
    unread_count: int
    disabledFeatures: List[str]
    attendee_provider_id: str
    id: str

class LinkedInMessage:
    object: str
    seen: int
    text: str
    edited: int
    hidden: int
    chat_id: str
    deleted: int
    seen_by: Dict[str, Any]
    subject: Optional[str]
    behavior: Optional[str]
    is_event: int
    original: str
    delivered: int
    is_sender: int
    reactions: List[Any]
    sender_id: str
    timestamp: str
    account_id: str
    attachments: List[Any]
    provider_id: str
    message_type: str
    attendee_type: str
    chat_provider_id: str
    attendee_distance: int
    sender_attendee_id: str
    id: str

class LinkedInMessageAttachment:
    type: str
    url: str
    name: Optional[str]
    size: Optional[int]
    mime_type: Optional[str]
    thumbnail_url: Optional[str]


@tool
async def get_chats(
    account_id: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: Optional[int] = None
) -> Any:
    """Retrieves all LinkedIn conversations (chats) for the authenticated user.

    This function fetches the list of conversations the user has on LinkedIn, including
    both individual and group chats. Results can be paginated using a cursor and limited
    to control the number of returned items.

    See https://docs.unipile.com/reference/linkedin-get-chats

    Args:
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.
        cursor (Optional[str]): A pagination cursor for retrieving the next set of results.
                               This value is typically obtained from a previous API response.
        limit (Optional[int]): Maximum number of chats to return in a single request.

    Returns:
        Any: The raw API response containing a paginated list of LinkedIn chat objects.

    Raises:
        Exception: If there's an API error during the request.
    """
    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    
    url = f"{base_url}/api/v1/chats?account_id={id_to_use}"
    if cursor:
        url += f"&cursor={cursor}"
    if limit:
        url += f"&limit={limit}"
    
    response = await make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    return response

@tool
async def get_chat_messages(
    chat_id: str,
    account_id: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: Optional[int] = None
) -> Any:
    """Retrieves messages from a specific LinkedIn conversation (chat).

    This function fetches the messages from a particular LinkedIn chat identified by its ID.
    Messages are returned in chronological order, and results can be paginated using a cursor
    and limited to control the number of returned items.

    See https://docs.unipile.com/reference/linkedin-get-chat-messages

    Args:
        chat_id (str): The unique identifier for the LinkedIn chat. This is typically obtained
                      from a previous call to get_chats().
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.
        cursor (Optional[str]): A pagination cursor for retrieving the next set of messages.
                               This value is typically obtained from a previous API response.
        limit (Optional[int]): Maximum number of messages to return in a single request.

    Returns:
        Any: The raw API response containing a paginated list of LinkedIn message objects.

    Raises:
        Exception: If no chat_id is provided or if there's an API error.
    """
    if not chat_id:
        raise Exception('Chat ID is required')
    
    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    
    url = f"{base_url}/api/v1/chats/{chat_id}/messages?account_id={id_to_use}"
    if cursor:
        url += f"&cursor={cursor}"
    if limit:
        url += f"&limit={limit}"
    
    response = await make_request(url, {
        'method': 'GET',
        'headers': get_headers()
    })
    
    return response

@tool
async def send_message(
    chat_id: str,
    content: str,
    account_id: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None
) -> Any:
    """Sends a message in an existing LinkedIn chat.

    This function sends a new message to a specific LinkedIn chat identified by its ID.
    The message can be plain text or include attachments if specified in the options.

    See https://docs.unipile.com/reference/linkedin-send-message

    Args:
        chat_id (str): The unique identifier for the LinkedIn chat where the message will be sent.
        content (str): The text content of the message to send.
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.
        options (Optional[Dict[str, Any]]): Additional options for the message, such as:
            - type (str): The type of message (default is "text")
            - attachments (List[Dict]): Any attachments to include with the message

    Returns:
        Any: The raw API response containing information about the sent message.

    Raises:
        Exception: If chat_id or content is not provided, or if there's an API error.
    """
    if not chat_id:
        raise Exception('Chat ID is required')
    
    if not content:
        raise Exception('Message content is required')
    
    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/chats/{chat_id}/messages"
    
    body: Dict[str, Any] = {
        'account_id': id_to_use,
        'content': content,
        'type': options.get('type', 'text') if options else 'text'
    }
    
    if options and 'attachments' in options and options['attachments']:
        body['attachments'] = options['attachments']
    
    response = await make_request(url, {
        'method': 'POST',
        'headers': get_headers(),
        'body': json.dumps(body)
    })
    
    return response

@tool
async def create_chat(
    recipient_id: str,
    text: str,
    account_id: Optional[str] = None
) -> Any:
    """Creates a new LinkedIn conversation (chat) with a specific user and sends an initial message.

    This function initiates a new conversation with a LinkedIn user identified by their provider ID
    and sends an initial message to start the conversation. The function returns the newly created
    chat object along with confirmation of the sent message.

    See https://docs.unipile.com/reference/linkedin-create-chat

    Args:
        recipient_id (str): The LinkedIn provider ID of the user to start a conversation with.
                           This is typically obtained from user profile information.
        text (str): The content of the initial message to send in the new conversation.
        account_id (Optional[str]): The Unipile account ID to use for this request. If not provided,
                                   the function will use the UNIPILE_ACCOUNT_ID environment variable.

    Returns:
        Any: The raw API response containing information about the created chat and the sent message.

    Raises:
        Exception: If recipient_id or text is not provided, or if there's an API error.
    """
    if not recipient_id:
        raise Exception('Recipient ID is required')

    if not text:
        raise Exception('Message text is required')

    id_to_use = ensure_account_id(account_id)
    base_url = get_base_url()
    url = f"{base_url}/api/v1/chats"

    response = await make_request(url, {
        'method': 'POST',
        'headers': get_headers(),
        'body': json.dumps({
            'account_id': id_to_use,
            'attendees_ids': [recipient_id],
            'text': text
        })
    })
    
    return response