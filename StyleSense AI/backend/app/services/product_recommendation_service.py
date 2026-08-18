from typing import List, Dict, Optional

from app.services.product_search_service import (
    ProductSearchService,
)

from app.services.location_service import (
    LocationService,
)


class ProductRecommendationService:

    def __init__(self):

        self.product_search_service = (
            ProductSearchService()
        )

        self.location_service = (
            LocationService()
        )

    # =========================================================
    # RECOMMEND PRODUCTS
    # =========================================================

    def recommend_products(
        self,
        ingredients: List[Dict],
        location: Optional[Dict] = None,
        budget: Optional[float] = None,
    ) -> List[Dict]:

        # -----------------------------------------------------
        # Normalize location
        # -----------------------------------------------------

        location = location or {}

        normalized_location = (
            self.location_service.normalize_location(
                city=location.get("city"),
                state=location.get("state"),
                pincode=location.get("pincode"),
                country=location.get(
                    "country",
                    "India",
                ),
            )
        )

        pincode = normalized_location.get(
            "pincode"
        )

        # -----------------------------------------------------
        # Extract ingredient names
        # -----------------------------------------------------

        ingredient_names = []

        for ingredient in ingredients:

            if isinstance(
                ingredient,
                dict,
            ):

                name = ingredient.get(
                    "name"
                )

                if name:
                    ingredient_names.append(
                        name
                    )

            elif isinstance(
                ingredient,
                str,
            ):

                ingredient_names.append(
                    ingredient
                )

        # -----------------------------------------------------
        # Search products
        # -----------------------------------------------------

        products = (
            self.product_search_service.search_by_ingredients(
                ingredients=ingredient_names,
                pincode=pincode,
                budget=budget,
            )
        )

        # -----------------------------------------------------
        # Add recommendation metadata
        # -----------------------------------------------------

        recommendations = []

        for product in products:

            recommendations.append({

                "product_id": product.get(
                    "id"
                ),

                "name": product.get(
                    "name"
                ),

                "brand": product.get(
                    "brand"
                ),

                "category": product.get(
                    "category"
                ),

                "ingredients": product.get(
                    "ingredients",
                    [],
                ),

                "price": product.get(
                    "price"
                ),

                "currency": product.get(
                    "currency",
                    "INR",
                ),

                "rating": product.get(
                    "rating"
                ),

                "marketplace": product.get(
                    "marketplace"
                ),

                "available": True,

                "location": normalized_location,

                "reason": self.generate_reason(
                    product=product,
                    ingredients=ingredient_names,
                ),
            })

        return recommendations

    # =========================================================
    # GENERATE PRODUCT REASON
    # =========================================================

    def generate_reason(
        self,
        product: Dict,
        ingredients: List[str],
    ) -> str:

        matched = []

        product_ingredients = [
            item.lower()
            for item in product.get(
                "ingredients",
                [],
            )
        ]

        for ingredient in ingredients:

            if any(
                ingredient.lower() in item
                for item in product_ingredients
            ):
                matched.append(
                    ingredient
                )

        if matched:

            return (
                "Recommended because it contains "
                + ", ".join(matched)
                + ", which matches your "
                "AI-generated skincare requirements."
            )

        return (
            "Recommended based on your "
            "personalized skincare routine."
        )



    def get_recommendations(
        self,
        concerns,
        ingredients,
        location=None,
    ):
        """
        Generate product recommendations based on:
        - detected skin concerns
        - recommended ingredients
        - user's saved location
        """

        recommendations = []

        # ---------------------------------------------------------
        # Normalize location
        # ---------------------------------------------------------

        if not location:
            location = "India"

        # ---------------------------------------------------------
        # Search products for each recommended ingredient
        # ---------------------------------------------------------

        for ingredient in ingredients or []:

            if isinstance(ingredient, dict):
                ingredient_name = ingredient.get("name")
            else:
                ingredient_name = str(ingredient)

            if not ingredient_name:
                continue

            products = self.product_search_service.search_products(
                ingredient=ingredient_name,
                location=location,
            )

            if products:
                recommendations.extend(products)

        # ---------------------------------------------------------
        # Remove duplicates
        # ---------------------------------------------------------

        unique_products = []

        seen = set()

        for product in recommendations:

            if not isinstance(product, dict):
                continue

            key = (
                product.get("name")
                or product.get("product_name")
                or product.get("url")
            )

            if key and key not in seen:
                seen.add(key)
                unique_products.append(product)

        return unique_products