class RecommendationService:

    def __init__(
        self,
        concern_service,
        ollama_service,
        product_service,
    ):
        self.concern_service = concern_service
        self.ollama_service = ollama_service
        self.product_service = product_service

    def generate_recommendations(
        self,
        db,
        scores,
        location,
    ):

        concerns = (
            self.concern_service
            .detect_concerns(scores)
        )

        ai_result = (
            self.ollama_service
            .generate_skin_recommendation(
                scores=scores,
                concerns=concerns,
            )
        )

        ingredients = ai_result.get(
            "recommended_ingredients",
            [],
        )

        products = (
            self.product_service
            .find_products(
                db=db,
                ingredients=ingredients,
                location=location,
            )
        )

        return {
            "concerns": concerns,
            "summary": ai_result.get(
                "summary"
            ),
            "recommended_ingredients": ingredients,
            "routine": ai_result.get(
                "routine",
                {},
            ),
            "products": products,
        }