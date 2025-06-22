"""
Unipile API - LinkedIn Messages

This file contains functions for interacting with LinkedIn messages via the Unipile API.
"""

import json
from typing import List, Dict, Any, Optional, Union
from .config import get_base_url, get_headers, make_request, ensure_account_id, PaginatedResponse
from .cleaners.messages import (
    clean_chats,
    clean_chat_messages,
    clean_create_chat_response,
    clean_send_message_response
)

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

"""
Get the user's LinkedIn conversations

@param account_id - Optional account ID (will use env var if not provided)
@param cursor - Optional cursor for pagination
@param limit - Optional limit for the number of results
@returns The user's LinkedIn chats
"""
async def get_chats(
    account_id: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    raw: bool = False
) -> Any:
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
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_chats(response)

"""
Get messages from a specific LinkedIn chat

@param chat_id - The LinkedIn chat ID
@param account_id - Optional account ID (will use env var if not provided)
@param cursor - Optional cursor for pagination
@param limit - Optional limit for the number of results
@returns Messages from the LinkedIn chat
"""
async def get_chat_messages(
    chat_id: str,
    account_id: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: Optional[int] = None,
    raw: bool = False
) -> Any:
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
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_chat_messages(response)

"""
Send a message in a LinkedIn chat

@param chat_id - The LinkedIn chat ID
@param content - The content of the message
@param account_id - Optional account ID (will use env var if not provided)
@param options - Optional message options
@returns The sent message
"""
async def send_message(
    chat_id: str,
    content: str,
    account_id: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    raw: bool = False
) -> Any:
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
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_send_message_response(response)

"""
Create a new chat with a LinkedIn user

@param recipient_id - The LinkedIn user's provider ID
@param text - The text of the message to be sent in the new chat
@param account_id - Optional account ID (will use env var if not provided)
@returns The created chat
"""
async def create_chat(
    recipient_id: str,
    text: str,
    account_id: Optional[str] = None,
    raw: bool = False
) -> Any:
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
    
    # Return raw response if raw is true, otherwise clean and return
    return response if raw else clean_create_chat_response(response)