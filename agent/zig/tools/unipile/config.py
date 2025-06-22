"""
Unipile API Configuration

This file contains the configuration for the Unipile API client.
"""

import os
import json
from typing import Dict, TypeVar, Generic, List, Any, Optional

# Environment variables
UNIPILE_DSN = os.environ.get('UNIPILE_DNS', '')
UNIPILE_API_KEY = os.environ.get('UNIPILE_API_KEY', '')
UNIPILE_ACCOUNT_ID = os.environ.get('UNIPILE_ACCOUNT_ID', '')

# Base URL
def get_base_url() -> str:
    """
    Retrieves the base URL for the Unipile API.
    
    This function returns the base URL for making API requests to Unipile, using the
    UNIPILE_DNS environment variable. It ensures the URL has the proper HTTP/HTTPS prefix.
    
    Returns:
        str: The complete base URL for the Unipile API.
    
    Raises:
        Exception: If the UNIPILE_DNS environment variable is not set.
    """
    if not UNIPILE_DSN:
        raise Exception('UNIPILE_DNS environment variable is not set')
    return UNIPILE_DSN if UNIPILE_DSN.startswith('http') else f"https://{UNIPILE_DSN}"

# Common request headers
def get_headers() -> Dict[str, str]:
    """
    Generates the standard HTTP headers required for Unipile API requests.
    
    This function creates a dictionary of HTTP headers that should be included with
    all requests to the Unipile API. It includes content type specifications and
    the API key for authentication.
    
    Returns:
        Dict[str, str]: A dictionary of HTTP headers including:
            - accept: application/json
            - content-type: application/json
            - X-API-KEY: The API key from environment variables
    
    Raises:
        Exception: If the UNIPILE_API_KEY environment variable is not set.
    """
    if not UNIPILE_API_KEY:
        raise Exception('UNIPILE_API_KEY environment variable is not set')
    
    return {
        'accept': 'application/json',
        'content-type': 'application/json',
        'X-API-KEY': UNIPILE_API_KEY
    }

# Error handling
class UnipileError(Exception):
    def __init__(self, status: int, body: str, message: Optional[str] = None):
        super().__init__(message or f"Unipile API error: {status}")
        self.status = status
        self.body = body
        self.name = 'UnipileError'

# Helper function to make API requests
T = TypeVar('T')

async def make_request(url: str, options: Dict[str, Any]) -> T:
    """
    Makes an HTTP request to the Unipile API with error handling.
    
    This function is a wrapper around HTTP requests to the Unipile API that handles
    common error cases and provides a consistent interface for all API calls.
    
    Args:
        url (str): The complete URL for the API endpoint to call.
        options (Dict[str, Any]): A dictionary of request options including:
            - method (str): HTTP method (GET, POST, etc.). Defaults to 'GET'.
            - headers (Dict[str, str]): HTTP headers to include in the request.
            - body (str): Request body for POST/PUT requests, typically JSON-encoded.
    
    Returns:
        T: The JSON response from the API, parsed into the appropriate type.
    
    Raises:
        UnipileError: If the API returns an error response (non-2xx status code).
        Exception: If there's a network error or other issue with the request.
    
    Example:
        ```python
        response = await make_request(
            "https://api.unipile.com/v1/users/me",
            {
                "method": "GET",
                "headers": get_headers()
            }
        )
        ```
    """
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=options.get('method', 'GET'),
                url=url,
                headers=options.get('headers', {}),
                data=options.get('body')
            ) as response:
                if not response.ok:
                    error_text = await response.text()
                    raise UnipileError(response.status, error_text)
                
                return await response.json()
    except UnipileError:
        raise
    except Exception as error:
        raise Exception(f"Failed to make request: {str(error)}")

# Types
class PaginatedResponse(Generic[T]):
    items: List[T]
    cursor: Optional[str] = None
    object: Optional[str] = None

class AccountInfo:
    id: str
    provider: str
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.provider = kwargs.get('provider')
        for key, value in kwargs.items():
            setattr(self, key, value)

# Helper function to ensure account_id is provided
def ensure_account_id(account_id: Optional[str] = None) -> str:
    """
    Ensures that a valid account ID is available for API requests.
    
    This function checks if an account ID is provided as an argument, and if not,
    falls back to the UNIPILE_ACCOUNT_ID environment variable. It ensures that
    all API requests have a valid account ID to identify the LinkedIn account
    being used.
    
    Args:
        account_id (Optional[str]): An explicit account ID to use, if provided.
    
    Returns:
        str: The account ID to use for the API request.
    
    Raises:
        Exception: If no account ID is provided as an argument and the
                  UNIPILE_ACCOUNT_ID environment variable is not set.
    
    Example:
        ```python
        # Use the account ID from environment variables
        default_id = ensure_account_id()
        
        # Use an explicitly provided account ID
        custom_id = ensure_account_id("custom-account-123")
        ```
    """
    id_to_use = account_id or UNIPILE_ACCOUNT_ID
    if not id_to_use:
        raise Exception('Account ID is required but not provided')
    return id_to_use