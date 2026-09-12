import requests

from bs4 import BeautifulSoup


def fetch_job_description(job_url):

    response = requests.get(
        job_url,
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    # Remove unnecessary HTML

    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header"
    ]):

        element.decompose()


    text = soup.get_text(
        separator=" ",
        strip=True
    )


    return text