from typing import List, Dict, Optional


class ProductSearchService:

    def __init__(self):

        # ---------------------------------------------------------
        # Temporary product catalogue
        #
        # Later this can be replaced by:
        # - Product database
        # - Marketplace API
        # - Retailer API
        # ---------------------------------------------------------

        self.products = [

            {
                "id": "PROD001",
                "name": "Hyaluronic Acid Hydrating Serum",
                "brand": "Generic",
                "category": "Serum",
                "ingredients": [
                    "Hyaluronic Acid"
                ],
                "price": 799,
                "currency": "INR",
                "rating": 4.5,
                "available_pincodes": "ALL",
                "marketplace": "StyleSense",
            },

            {
                "id": "PROD002",
                "name": "Ceramide Barrier Moisturizer",
                "brand": "Generic",
                "category": "Moisturizer",
                "ingredients": [
                    "Ceramides"
                ],
                "price": 699,
                "currency": "INR",
                "rating": 4.4,
                "available_pincodes": "ALL",
                "marketplace": "StyleSense",
            },

            {
                "id": "PROD003",
                "name": "Broad Spectrum SPF 50 Sunscreen",
                "brand": "Generic",
                "category": "Sunscreen",
                "ingredients": [
                    "SPF 50",
                    "Broad Spectrum"
                ],
                "price": 599,
                "currency": "INR",
                "rating": 4.6,
                "available_pincodes": "ALL",
                "marketplace": "StyleSense",
            },

            {
                "id": "PROD004",
                "name": "Gentle Hydrating Cleanser",
                "brand": "Generic",
                "category": "Cleanser",
                "ingredients": [
                    "Gentle Cleanser"
                ],
                "price": 499,
                "currency": "INR",
                "rating": 4.3,
                "available_pincodes": "ALL",
                "marketplace": "StyleSense",
            },

            {
                "id": "PROD005",
                "name": "Niacinamide Serum",
                "brand": "Generic",
                "category": "Serum",
                "ingredients": [
                    "Niacinamide"
                ],
                "price": 649,
                "currency": "INR",
                "rating": 4.4,
                "available_pincodes": "ALL",
                "marketplace": "StyleSense",
            },
        ]

    # =========================================================
    # SEARCH PRODUCTS
    # =========================================================

    def search_products(
        self,
        category: Optional[str] = None,
        ingredient: Optional[str] = None,
        budget: Optional[float] = None,
        location: Optional[str] = None,
        pincode: Optional[str] = None,
        limit: int = 5,
    ) -> List[Dict]:

        results = []

        for product in self.products:

            # -------------------------------------------------
            # Category filter
            # -------------------------------------------------

            if category:

                if (
                    product["category"].lower()
                    != category.lower()
                ):
                    continue

            # -------------------------------------------------
            # Ingredient filter
            # -------------------------------------------------

            if ingredient:

                ingredient_lower = ingredient.lower()

                product_ingredients = [
                    item.lower()
                    for item in product.get(
                        "ingredients",
                        [],
                    )
                ]

                if not any(
                    ingredient_lower in item
                    for item in product_ingredients
                ):
                    continue

            # -------------------------------------------------
            # Budget filter
            # -------------------------------------------------

            if budget is not None:

                if product["price"] > budget:
                    continue

            # -------------------------------------------------
            # Location / pincode
            # -------------------------------------------------

            if pincode:

                available_pincodes = product.get(
                    "available_pincodes"
                )

                if (
                    available_pincodes != "ALL"
                    and pincode not in available_pincodes
                ):
                    continue

            results.append(product)

            if len(results) >= limit:
                break

        return results

    # =========================================================
    # SEARCH BY INGREDIENTS
    # =========================================================

    def search_by_ingredients(
        self,
        ingredients: List[str],
        pincode: Optional[str] = None,
        location: Optional[str] = None,
        budget: Optional[float] = None,
        limit_per_ingredient: int = 3,
    ) -> List[Dict]:

        results = []

        for ingredient in ingredients:

            products = self.search_products(
                ingredient=ingredient,
                pincode=pincode,
                budget=budget,
                limit=limit_per_ingredient,
            )

            results.extend(products)

        # -----------------------------------------------------
        # Remove duplicates
        # -----------------------------------------------------

        unique_products = {}

        for product in results:

            unique_products[
                product["id"]
            ] = product

        return list(
            unique_products.values()
        )