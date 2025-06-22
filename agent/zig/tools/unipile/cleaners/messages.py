"""
Unipile API - LinkedIn Messages Response Cleaners

This file contains functions for cleaning and formatting LinkedIn message responses
from the Unipile API to make them suitable for feeding to an LLM.
"""

from typing import Any, Dict, List, Optional

def clean_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format a single message
    
    Args:
        message: The raw message data from the API
    
    Returns:
        A cleaned and formatted message
    """
    if not message:
        return None

    return {
        "id": message.get("id"),
        "text": message.get("text"),
        "timestamp": message.get("timestamp"),
        "isSender": message.get("is_sender"),
        "senderId": message.get("sender_id"),
        "senderAttendeeId": message.get("sender_attendee_id"),
        "chatId": message.get("chat_id"),
        "chatProviderId": message.get("chat_provider_id"),
        "seen": message.get("seen"),
        "delivered": message.get("delivered"),
        "edited": message.get("edited"),
        "deleted": message.get("deleted"),
        "attachments": message.get("attachments") or []
    }

def clean_chats(chats_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format chats response
    
    Args:
        chats_response: The raw chats response from the API
    
    Returns:
        Cleaned and formatted chats
    """
    if not chats_response or not chats_response.get("items"):
        return {"chats": []}

    return {
        "chats": [
            {
                "id": chat.get("id"),
                "name": chat.get("name"),
                "lastActivity": chat.get("timestamp"),
                "unreadCount": chat.get("unread_count"),
                "attendeeProviderId": chat.get("attendee_provider_id"),
                "providerId": chat.get("provider_id"),
                "attendees": [
                    {
                        "id": attendee.get("id"),
                        "name": f"{attendee.get('first_name')} {attendee.get('last_name')}",
                        "profilePictureUrl": attendee.get("profile_picture_url")
                    }
                    for attendee in chat.get("attendees", [])
                ] if chat.get("attendees") else [],
                "lastMessage": {
                    "text": chat.get("last_message", {}).get("text"),
                    "timestamp": chat.get("last_message", {}).get("timestamp"),
                    "senderId": chat.get("last_message", {}).get("sender_id")
                } if chat.get("last_message") else None
            }
            for chat in chats_response.get("items", [])
        ]
    }

def clean_chat_messages(messages_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format chat messages response
    
    Args:
        messages_response: The raw chat messages response from the API
    
    Returns:
        Cleaned and formatted chat messages
    """
    if not messages_response or not messages_response.get("items"):
        return {"messages": []}

    return {
        "messages": [clean_message(message) for message in messages_response.get("items", [])],
        "cursor": messages_response.get("cursor")
    }

def clean_create_chat_response(create_chat_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format create chat response
    
    Args:
        create_chat_response: The raw create chat response from the API
    
    Returns:
        Cleaned and formatted create chat response
    """
    if not create_chat_response:
        return None

    return {
        "success": True,
        "object": create_chat_response.get("object"),
        "chatId": create_chat_response.get("chat_id"),
        "messageId": create_chat_response.get("message_id")
    }

def clean_send_message_response(send_message_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format send message response
    
    Args:
        send_message_response: The raw send message response from the API
    
    Returns:
        Cleaned and formatted send message response
    """
    if not send_message_response:
        return None

    return {
        "success": True,
        "object": send_message_response.get("object"),
        "messageId": send_message_response.get("message_id") or send_message_response.get("id")
    }