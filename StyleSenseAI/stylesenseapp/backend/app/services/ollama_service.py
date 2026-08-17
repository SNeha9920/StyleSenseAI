import json
import requests

from app.core.config import settings


class OllamaService:

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

    # ============================================================
    # GENERATE PERSONALIZED SKINCARE RECOMMENDATION
    # ============================================================

    def generate_skin_recommendation(
        self,
        scores,
        concerns,
    ):

        prompt = f"""
You are an AI skincare routine recommendation assistant.

Your job is to create a simple, personalized skincare routine
based ONLY on the skin-analysis scores and detected concerns
provided below.

IMPORTANT:
- Do not diagnose medical conditions.
- Do not invent skin conditions.
- Do not assume information that is not provided.
- Do not invent product brands.
- Do not invent commercial product names.
- Recommend product TYPES and suitable ACTIVE INGREDIENTS.
- Keep the routine practical and easy to follow.
- Do not recommend too many active ingredients at the same time.
- Prefer gentle skincare.
- If a concern is mild, use gentle language.
- If there are no major concerns, provide a maintenance routine.
- Sunscreen should generally be included in a daytime routine.
- Do not make medical claims.
- Do not claim that an ingredient will cure a condition.

============================================================
SKIN ANALYSIS SCORES
============================================================

{json.dumps(scores, indent=2)}

============================================================
DETECTED CONCERNS
============================================================

{json.dumps(concerns, indent=2)}

============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "summary": "Short explanation of the overall skin condition based only on the supplied scores.",

    "recommendation": "Short personalized recommendation explaining the main skincare priorities.",

    "routine": {{
        "morning": [
            {{
                "step": 1,
                "product_type": "Gentle Cleanser",
                "ingredient": "Suitable ingredient or None",
                "reason": "Short reason for this step."
            }}
        ],

        "night": [
            {{
                "step": 1,
                "product_type": "Gentle Cleanser",
                "ingredient": "Suitable ingredient or None",
                "reason": "Short reason for this step."
            }}
        ]
    }},

    "ingredients": [
        {{
            "name": "Ingredient name",
            "purpose": "What this ingredient is intended to support."
        }}
    ],

    "products": [
        {{
            "product_type": "Product category/type",
            "recommended_ingredient": "Ingredient",
            "reason": "Why this type of product may fit the detected concerns."
        }}
    ]
}}

============================================================
ROUTINE RULES
============================================================

1. Morning routine should normally contain:
   - Cleanser
   - One appropriate treatment/serum if needed
   - Moisturizer if needed
   - Sunscreen

2. Night routine should normally contain:
   - Cleanser
   - Appropriate treatment/serum if needed
   - Moisturizer

3. Do not recommend every possible active ingredient.

4. Select only ingredients that logically correspond to the
   provided scores and detected concerns.

5. If hydration is a concern:
   consider ingredients such as:
   - Hyaluronic Acid
   - Glycerin
   - Ceramides

6. If acne/blemish concerns are detected:
   consider gentle acne-supporting ingredients such as:
   - Niacinamide
   - Salicylic Acid

7. If brightness/radiance is a concern:
   consider:
   - Vitamin C
   - Niacinamide

8. If texture is a concern:
   consider:
   - Niacinamide
   - gentle exfoliating ingredients

9. Do not combine too many exfoliating or potentially irritating
   ingredients in the same routine.

10. Sunscreen should be represented as:
    product_type = "Sunscreen"
    recommended_ingredient = "Broad-spectrum SPF 30+"

11. Never generate:
    - brand names
    - fake product names
    - prices
    - URLs
    - medical diagnoses

12. Keep the number of recommended products between 4 and 6.

13. Keep the ingredient list between 3 and 6 ingredients.

14. Morning and night routines should each contain approximately
    3 to 5 steps.

15. Use simple language suitable for a skincare application.

============================================================
IMPORTANT
============================================================

The supplied scores are the only evidence available.

Do not create additional concerns that are not present in the
"Detected concerns" section.

Return JSON only.
"""

        try:

            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                },
                timeout=600,
            )

            response.raise_for_status()

        except requests.exceptions.RequestException as e:

            raise RuntimeError(
                f"Ollama request failed: {str(e)}"
            )

        # --------------------------------------------------------
        # Parse Ollama response
        # --------------------------------------------------------

        data = response.json()

        raw_response = data.get("response")

        if not raw_response:
            raise RuntimeError(
                "Ollama returned an empty response."
            )

        try:

            result = json.loads(
                raw_response
            )

        except json.JSONDecodeError as e:

            raise RuntimeError(
                f"Ollama returned invalid JSON: {str(e)}"
            )

        # --------------------------------------------------------
        # Validate expected structure
        # --------------------------------------------------------

        result = self._validate_result(
            result
        )

        return result

    # ============================================================
    # VALIDATE OLLAMA RESULT
    # ============================================================

    def _validate_result(
        self,
        result,
    ):

        if not isinstance(result, dict):
            raise RuntimeError(
                "Ollama response is not a JSON object."
            )

        # --------------------------------------------------------
        # Summary
        # --------------------------------------------------------

        if not isinstance(
            result.get("summary"),
            str,
        ):

            result["summary"] = (
                "Your skin analysis has been completed."
            )

        # --------------------------------------------------------
        # Recommendation
        # --------------------------------------------------------

        if not isinstance(
            result.get("recommendation"),
            str,
        ):

            result["recommendation"] = (
                "Follow a consistent and gentle skincare routine."
            )

        # --------------------------------------------------------
        # Routine
        # --------------------------------------------------------

        if not isinstance(
            result.get("routine"),
            dict,
        ):

            result["routine"] = {}

        if not isinstance(
            result["routine"].get("morning"),
            list,
        ):

            result["routine"]["morning"] = []

        if not isinstance(
            result["routine"].get("night"),
            list,
        ):

            result["routine"]["night"] = []

        # --------------------------------------------------------
        # Ingredients
        # --------------------------------------------------------

        if not isinstance(
            result.get("ingredients"),
            list,
        ):

            result["ingredients"] = []

        # --------------------------------------------------------
        # Products
        # --------------------------------------------------------

        if not isinstance(
            result.get("products"),
            list,
        ):

            result["products"] = []

        return result