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
    if not UNIPILE_DSN:
        raise Exception('UNIPILE_DNS environment variable is not set')
    return UNIPILE_DSN if UNIPILE_DSN.startswith('http') else f"https://{UNIPILE_DSN}"

# Common request headers
def get_headers() -> Dict[str, str]:
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
    id_to_use = account_id or UNIPILE_ACCOUNT_ID
    if not id_to_use:
        raise Exception('Account ID is required but not provided')
    return id_to_use