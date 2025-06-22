"""
Unipile API - LinkedIn Posts Response Cleaners

This file contains functions for cleaning and formatting LinkedIn post responses
from the Unipile API to make them suitable for feeding to an LLM.
"""

from typing import Any, Dict, List, Optional

def clean_post(post: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format a single post
    
    Args:
        post: The raw post data from the API
    
    Returns:
        A cleaned and formatted post
    """
    if not post:
        return None

    attachments = []
    if post.get("attachments"):
        for attachment in post.get("attachments", []):
            cleaned_attachment = {
                "type": attachment.get("type"),
                "url": attachment.get("url")
            }
            
            if attachment.get("type") == "file":
                cleaned_attachment["fileName"] = attachment.get("file_name")
                cleaned_attachment["mimeType"] = attachment.get("mimetype")
            elif attachment.get("type") in ["img", "video"] and attachment.get("size"):
                cleaned_attachment["width"] = attachment.get("size", {}).get("width")
                cleaned_attachment["height"] = attachment.get("size", {}).get("height")
                
            attachments.append(cleaned_attachment)

    return {
        "id": post.get("id"),
        "text": post.get("text"),
        "date": post.get("date"),
        "parsedDateTime": post.get("parsed_datetime"),
        "shareUrl": post.get("share_url"),
        "stats": {
            "comments": post.get("comment_counter"),
            "reactions": post.get("reaction_counter"),
            "reposts": post.get("repost_counter"),
            "impressions": post.get("impressions_counter")
        },
        "author": {
            "name": post.get("author", {}).get("name"),
            "headline": post.get("author", {}).get("headline"),
            "publicIdentifier": post.get("author", {}).get("public_identifier"),
            "isCompany": post.get("author", {}).get("is_company")
        } if post.get("author") else None,
        "attachments": attachments,
        "isRepost": post.get("is_repost")
    }

def clean_user_posts(posts_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format user posts response
    
    Args:
        posts_response: The raw user posts response from the API
    
    Returns:
        Cleaned and formatted user posts
    """
    if not posts_response or not posts_response.get("items"):
        return {"posts": []}

    return {
        "posts": [clean_post(post) for post in posts_response.get("items", [])]
    }

def clean_post_comments(comments_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format post comments response
    
    Args:
        comments_response: The raw post comments response from the API
    
    Returns:
        Cleaned and formatted post comments
    """
    if not comments_response or not comments_response.get("items"):
        return {"comments": []}

    return {
        "comments": [
            {
                "id": comment.get("id"),
                "text": comment.get("text"),
                "date": comment.get("date"),
                "parsedDateTime": comment.get("parsed_datetime"),
                "author": {
                    "name": comment.get("author", {}).get("name"),
                    "headline": comment.get("author", {}).get("headline"),
                    "publicIdentifier": comment.get("author", {}).get("public_identifier"),
                    "isCompany": comment.get("author", {}).get("is_company")
                } if comment.get("author") else None,
                "stats": {
                    "reactions": comment.get("reaction_counter") or 0
                }
            }
            for comment in comments_response.get("items", [])
        ]
    }

def clean_create_post_response(create_post_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format create post response
    
    Args:
        create_post_response: The raw create post response from the API
    
    Returns:
        Cleaned and formatted create post response
    """
    if not create_post_response:
        return None

    return {
        "success": True,
        "postId": create_post_response.get("post_id"),
        "object": create_post_response.get("object")
    }

def clean_comment_on_post_response(comment_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and format comment on post response
    
    Args:
        comment_response: The raw comment on post response from the API
    
    Returns:
        Cleaned and formatted comment on post response
    """
    if not comment_response:
        return None

    return {
        "success": True,
        "object": comment_response.get("object")
    }