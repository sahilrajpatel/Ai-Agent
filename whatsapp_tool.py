import json

from langchain_core.tools import tool

from src.browser import get_page


@tool
def fill_form(url: str, field_values: str) -> str:
    """Fill out a form on a webpage.
    url: the page that has the form.
    field_values: a JSON string mapping each field's placeholder/name/label
    to the value to type, for example:
    '{"Name": "Rahul Sharma", "Email": "rahul@email.com", "Phone": "9876543210"}'
    """
    page = get_page()
    page.goto(url)
    page.wait_for_timeout(1500)

    try:
        values = json.loads(field_values)
    except json.JSONDecodeError:
        return 'field_values must be valid JSON, like {"Name": "Rahul"}'

    filled, not_found = [], []

    for field_label, value in values.items():
        # try the most common ways a field might be identified on a page
        possible_selectors = [
            f"input[placeholder='{field_label}']",
            f"textarea[placeholder='{field_label}']",
            f"input[name='{field_label}']",
            f"input[aria-label='{field_label}']",
        ]

        found = False
        for selector in possible_selectors:
            locator = page.locator(selector)
            if locator.count() > 0:
                locator.first.fill(str(value))
                filled.append(field_label)
                found = True
                break

        if not found:
            not_found.append(field_label)

    result = f"Filled fields: {filled}."
    if not_found:
        result += f" Could not find these fields on the page: {not_found}."
    return result
