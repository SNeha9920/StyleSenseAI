def build_recommendation_prompt(
    scores,
    concerns,
    ingredients,
):

    return f"""
Based on the following skin analysis:

Scores:
{scores}

Concerns:
{concerns}

Recommended ingredients:
{ingredients}

Explain how these ingredients can support
the identified skin concerns.

Do not generate product names.
Do not generate brands.
Do not invent clinical diagnoses.

Return JSON.
"""