"""
Unipile API - LinkedIn Users Response Cleaners

This file contains functions for cleaning and formatting LinkedIn user responses
from the Unipile API to make them suitable for feeding to an LLM.
"""

from typing import Any, Dict, List, Optional

def clean_user_profile(user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format a user profile response
    
    Args:
        user_profile: The raw user profile response from the API
    
    Returns:
        A cleaned and formatted user profile
    """
    if not user_profile:
        return None

    return {
        "firstName": user_profile.get("first_name"),
        "lastName": user_profile.get("last_name"),
        "fullName": f"{user_profile.get('first_name')} {user_profile.get('last_name')}",
        "headline": user_profile.get("headline"),
        "location": user_profile.get("location"),
        "profilePictureUrl": user_profile.get("profile_picture_url_large") or user_profile.get("profile_picture_url"),
        "publicIdentifier": user_profile.get("public_identifier"),
        "providerId": user_profile.get("provider_id"),
        "memberUrn": user_profile.get("member_urn"),
        "followerCount": user_profile.get("follower_count"),
        "connectionsCount": user_profile.get("connections_count"),
        "isPremium": user_profile.get("is_premium"),
        "isInfluencer": user_profile.get("is_influencer"),
        "isCreator": user_profile.get("is_creator")
    }

def clean_account_owner_profile(account_owner_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format account owner profile response
    
    Args:
        account_owner_profile: The raw account owner profile response from the API
    
    Returns:
        A cleaned and formatted account owner profile
    """
    if not account_owner_profile:
        return None
    
    base_profile = clean_user_profile(account_owner_profile)
    
    return {
        **base_profile,
        "providerId": account_owner_profile.get("provider_id"),
        "entityUrn": account_owner_profile.get("entity_urn")
    }

def clean_user_relations(relations: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format user relations response
    
    Args:
        relations: The raw user relations response from the API
    
    Returns:
        Cleaned and formatted user relations
    """
    if not relations or not relations.get("items"):
        return {"connections": []}

    return {
        "connections": [
            {
                "firstName": connection.get("first_name"),
                "lastName": connection.get("last_name"),
                "fullName": f"{connection.get('first_name')} {connection.get('last_name')}",
                "headline": connection.get("headline"),
                "profilePictureUrl": connection.get("profile_picture_url"),
                "publicIdentifier": connection.get("public_identifier"),
                "publicProfileUrl": connection.get("public_profile_url"),
                "connectionDegree": connection.get("connection_degree"),
                # Important identifiers for API calls
                "memberId": connection.get("member_id"),
                "memberUrn": connection.get("member_urn"),
                "connectionUrn": connection.get("connection_urn"),
                "createdAt": connection.get("created_at")
            }
            for connection in relations.get("items", [])
        ]
    }

def clean_invitations_received(invitations: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format invitations received response
    
    Args:
        invitations: The raw invitations received response from the API
    
    Returns:
        Cleaned and formatted invitations received
    """
    if not invitations or not invitations.get("items"):
        return {"invitations": []}

    return {
        "invitations": [
            {
                "id": invitation.get("id"),
                "sharedSecret": invitation.get("shared_secret"),
                "message": invitation.get("message"),
                "sentAt": invitation.get("sent_at"),
                "sender": {
                    "firstName": invitation.get("sender", {}).get("first_name"),
                    "lastName": invitation.get("sender", {}).get("last_name"),
                    "fullName": f"{invitation.get('sender', {}).get('first_name')} {invitation.get('sender', {}).get('last_name')}",
                    "headline": invitation.get("sender", {}).get("headline"),
                    "profilePictureUrl": invitation.get("sender", {}).get("profile_picture_url")
                } if invitation.get("sender") else None
            }
            for invitation in invitations.get("items", [])
        ]
    }

def clean_invitations_sent(invitations: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format invitations sent response
    
    Args:
        invitations: The raw invitations sent response from the API
    
    Returns:
        Cleaned and formatted invitations sent
    """
    if not invitations or not invitations.get("items"):
        return {"invitations": []}

    return {
        "invitations": [
            {
                "id": invitation.get("id"),
                "sharedSecret": invitation.get("shared_secret"),
                "message": invitation.get("message"),
                "sentAt": invitation.get("sent_at"),
                "recipient": {
                    "firstName": invitation.get("recipient", {}).get("first_name"),
                    "lastName": invitation.get("recipient", {}).get("last_name"),
                    "fullName": f"{invitation.get('recipient', {}).get('first_name')} {invitation.get('recipient', {}).get('last_name')}",
                    "headline": invitation.get("recipient", {}).get("headline"),
                    "profilePictureUrl": invitation.get("recipient", {}).get("profile_picture_url")
                } if invitation.get("recipient") else None
            }
            for invitation in invitations.get("items", [])
        ]
    }

def clean_send_invitation_response(send_invitation_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format send invitation response
    
    Args:
        send_invitation_response: The raw send invitation response from the API
    
    Returns:
        Cleaned and formatted send invitation response
    """
    if not send_invitation_response:
        return None

    return {
        "success": True,
        "object": send_invitation_response.get("object"),
        "invitationId": send_invitation_response.get("invitation_id")
    }