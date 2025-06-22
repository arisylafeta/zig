"""
This file contains functions to clean and format the raw data from the Apollo API
into a more readable and LLM-friendly format.
"""

from .helpers import clean_person, clean_organization

def clean_people_search(response):
    """
    Cleans the response from the peopleSearch API call.
    
    Args:
        response: The raw JSON response from the peopleSearch API.
    
    Returns:
        A formatted string summarizing the people found.
    """
    if not response or not response.get("people") or len(response.get("people", [])) == 0:
        return {"people": []}
    return {
        "people": [clean_person(person) for person in response["people"]]
    }

def clean_organization_search(response):
    """
    Cleans the response from the organizationSearch API call.
    
    Args:
        response: The raw JSON response from the organizationSearch API.
    
    Returns:
        A formatted string summarizing the organizations found.
    """
    if not response or not response.get("organizations") or len(response.get("organizations", [])) == 0:
        return {"organizations": []}
    return {
        "organizations": [clean_organization(org) for org in response["organizations"]]
    }

def clean_organization_job_postings(response):
    """
    Cleans the response from the organizationJobPostings API call.
    
    Args:
        response: The raw JSON response from the organizationJobPostings API.
    
    Returns:
        A formatted string summarizing the job postings found.
    """
    if not response or not response.get("organization_job_postings") or len(response.get("organization_job_postings", [])) == 0:
        return {"job_postings": []}

    cleaned_jobs = []
    for job in response["organization_job_postings"]:
        cleaned_job = {
            "title": job.get("title"),
            "url": job.get("url"),
            "location": job.get("location"),
            "content": job.get("content"),
            "posted_date": job.get("posted_date")
        }
        # remove None fields
        cleaned_job = {k: v for k, v in cleaned_job.items() if v is not None}
        cleaned_jobs.append(cleaned_job)

    return {"job_postings": cleaned_jobs}