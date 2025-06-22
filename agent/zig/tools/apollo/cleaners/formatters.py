def person_to_markdown(person):
    summary = f"### {person['name']}\n"
    if person.get("title"):
        summary += f"**Title:** {person['title']}\n"
    if person.get("headline"):
        summary += f"**Headline:** {person['headline']}\n"
    if person.get("linkedin_url"):
        summary += f"**LinkedIn:** {person['linkedin_url']}\n"
    if person.get("location"):
        summary += f"**Location:** {person['location']}\n"

    if person.get("current_organization"):
        summary += f"\n**Current Organization:**\n"
        summary += organization_to_markdown(person["current_organization"], True)

    if person.get("employment_history") and len(person.get("employment_history", [])) > 0:
        summary += f"\n**Employment History:**\n"
        for job in person["employment_history"]:
            summary += f"- **{job['title']}** at {job['organization_name']}"
            if job.get("start_date"):
                summary += f" ({job['start_date']} - {job.get('end_date', 'Present')})\n"
            else:
                summary += f"\n"

    return summary

def organization_to_markdown(org, is_sub=False):
    summary = ""

    if is_sub:
        summary += f"- **Name:** {org['name']}\n"
        if org.get("website_url"):
            summary += f"- **Website:** {org['website_url']}\n"
        if org.get("industry"):
            summary += f"- **Industry:** {org['industry']}\n"
        if org.get("employees"):
            summary += f"- **Employees:** {org['employees']}\n"
    else:
        summary += f"### {org['name']}\n"
        if org.get("website_url"):
            summary += f"**Website:** {org['website_url']}\n"
        if org.get("linkedin_url"):
            summary += f"**LinkedIn:** {org['linkedin_url']}\n"
        if org.get("domain"):
            summary += f"**Domain:** {org['domain']}\n"
        if org.get("founded_year"):
            summary += f"**Founded:** {org['founded_year']}\n"
        if org.get("revenue"):
            summary += f"**Revenue:** {org['revenue']}\n"
        if org.get("employees"):
            summary += f"**Employees:** {org['employees']}\n"
        if org.get("industry"):
            summary += f"**Industry:** {org['industry']}\n"
        if org.get("latest_funding"):
            summary += f"**Latest Funding:** {org['latest_funding']}\n"
        if org.get("total_funding"):
            summary += f"**Total Funding:** {org['total_funding']}\n"
        if org.get("description"):
            summary += f"\n**Description:**\n{org['description']}\n"
        if org.get("keywords") and len(org.get("keywords", [])) > 0:
            summary += f"\n**Keywords:**\n{', '.join(org['keywords'])}\n"

    return summary

def job_posting_to_markdown(job):
    summary = f"### {job['title']}\n"
    if job.get("location"):
        summary += f"**Location:** {job['location']}\n"
    if job.get("posted_date"):
        summary += f"**Posted:** {job['posted_date']}\n"
    if job.get("url"):
        summary += f"**URL:** {job['url']}\n"
    if job.get("content"):
        summary += f"\n{job['content']}\n"
    return summary

def people_search_json_to_markdown(data):
    if not data.get("people") or len(data.get("people", [])) == 0:
        return "No people found."
    summaries = [person_to_markdown(person) for person in data["people"]]
    return f"## People Search Results\n\n{'\\n---\\n'.join(summaries)}"

def organization_search_json_to_markdown(data):
    if not data.get("organizations") or len(data.get("organizations", [])) == 0:
        return "No organizations found."
    summaries = [organization_to_markdown(org) for org in data["organizations"]]
    return f"## Organization Search Results\n\n{'\\n---\\n'.join(summaries)}"

def organization_job_postings_json_to_markdown(data):
    if not data.get("job_postings") or len(data.get("job_postings", [])) == 0:
        return "No job postings found."
    summaries = [job_posting_to_markdown(job) for job in data["job_postings"]]
    return f"## Job Postings\n\n{'\\n---\\n'.join(summaries)}"

def people_enrichment_json_to_markdown(data):
    if not data.get("person"):
        return "No person data found for enrichment."
    return f"## Person Enrichment Result\n\n{person_to_markdown(data['person'])}"

def bulk_people_enrichment_json_to_markdown(data):
    if not data.get("matches") or len(data.get("matches", [])) == 0:
        return "No people found for bulk enrichment."
    summaries = [person_to_markdown(person) for person in data["matches"]]
    return f"## Bulk People Enrichment Results\n\n{'\\n---\\n'.join(summaries)}"

def organization_enrichment_json_to_markdown(data):
    if not data.get("organization"):
        return "No organization data found for enrichment."
    return f"## Organization Enrichment Result\n\n{organization_to_markdown(data['organization'])}"

def bulk_organization_enrichment_json_to_markdown(data):
    if not data.get("organizations") or len(data.get("organizations", [])) == 0:
        return "No organizations found for bulk enrichment."
    summaries = [organization_to_markdown(org) for org in data["organizations"]]
    return f"## Bulk Organization Enrichment Results\n\n{'\\n---\\n'.join(summaries)}"