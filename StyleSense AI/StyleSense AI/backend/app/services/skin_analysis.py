from typing import Any, Dict, Optional
from datetime import datetime, timezone
from io import BytesIO
from app.services.concern_service import ConcernService
from app.services.ollama_service import OllamaService
from app.services.product_recommendation_service import (
    ProductRecommendationService,
)
from app.models.user_profile import UserProfile

from PIL import Image
from sqlalchemy.orm import Session

from app.integrations.youcam import (
    YouCamSkinAnalysis,
    YouCamAPIError,
)

import requests

from app.models.skin_analysis import SkinAnalysis


class SkinAnalysisService:

    def __init__(self):
        self.youcam = YouCamSkinAnalysis()
        self.concern_service = ConcernService()
        self.ollama_service = OllamaService()

        self.product_recommendation_service = (
            ProductRecommendationService()
        )

    # ============================================================
    # START SKIN ANALYSIS
    # ============================================================

    def start_analysis(
        self,
        db: Session,
        user_id: int,
        file_name: str,
        content_type: str,
        file_bytes: bytes,
        city: Optional[str] = None,
        state: Optional[str] = None,
        pincode: Optional[str] = None,
        budget: Optional[float] = None,
    ):

        # --------------------------------------------------------
        # Validate uploaded file
        # --------------------------------------------------------

        if not file_bytes:
            raise ValueError(
                "Uploaded image is empty."
            )

        original_size = len(file_bytes)

        print("\n========== ORIGINAL FILE ==========")
        print(f"File name: {file_name}")
        print(f"Content type: {content_type}")
        print(f"Size: {original_size} bytes")
        print("===================================\n")

        # --------------------------------------------------------
        # Resize / normalize image
        # --------------------------------------------------------

        file_bytes = self.resize_image(
            file_bytes=file_bytes,
            min_width=2560,
            min_height=2560,
        )

        file_size = len(file_bytes)

        # --------------------------------------------------------
        # Validate final file size
        # --------------------------------------------------------

        if file_size == 0:
            raise ValueError(
                "Processed image is empty."
            )

        if file_size > 10 * 1024 * 1024:
            raise ValueError(
                "Image size cannot exceed 10 MB."
            )

        # --------------------------------------------------------
        # We always convert the processed image to JPEG
        # --------------------------------------------------------

        file_name = "skin_analysis.jpg"
        content_type = "image/jpeg"

        print("\n========== FINAL IMAGE ==========")
        print(f"File name: {file_name}")
        print(f"Content type: {content_type}")
        print(f"Size: {file_size} bytes")
        print("=================================\n")

        # --------------------------------------------------------
        # 1. Request signed upload URL from YouCam
        # --------------------------------------------------------

        upload_response = self.youcam.create_file_upload(
            file_name=file_name,
            content_type=content_type,
            file_size=file_size,
        )

        print("\n========== FILE UPLOAD RESPONSE ==========")
        print(upload_response)
        print("===========================================\n")

        # --------------------------------------------------------
        # 2. Extract file information
        # --------------------------------------------------------

        data = upload_response.get(
            "data",
            {},
        )

        files = data.get(
            "files",
            [],
        )

        if not files:
            raise ValueError(
                "YouCam did not return upload information."
            )

        file_info = files[0]

        # --------------------------------------------------------
        # File ID
        # --------------------------------------------------------

        file_id = file_info.get(
            "file_id"
        )

        if not file_id:
            raise ValueError(
                "YouCam did not return file_id."
            )

        # --------------------------------------------------------
        # Signed upload request
        # --------------------------------------------------------

        upload_requests = file_info.get(
            "requests",
            [],
        )

        if not upload_requests:
            raise ValueError(
                "YouCam did not return upload URL."
            )

        upload_request = upload_requests[0]

        upload_url = upload_request.get(
            "url"
        )

        upload_headers = upload_request.get(
            "headers",
            {},
        )

        if not upload_url:
            raise ValueError(
                "YouCam did not return signed upload URL."
            )

        # --------------------------------------------------------
        # IMPORTANT:
        # The signed URL contains Content-Length and Content-Type.
        # Use the exact values returned by YouCam.
        # --------------------------------------------------------

        print("\n========== UPLOAD HEADERS ==========")
        print(upload_headers)
        print("====================================\n")

        # --------------------------------------------------------
        # 3. Upload image to YouCam S3
        # --------------------------------------------------------

        try:

            response = requests.put(
                upload_url,
                headers=upload_headers,
                data=file_bytes,
                timeout=120,
            )

        except requests.exceptions.ConnectTimeout as e:

            raise YouCamAPIError(
                f"Connection to YouCam storage timed out: {str(e)}"
            )

        except requests.exceptions.ConnectionError as e:

            raise YouCamAPIError(
                f"Could not connect to YouCam storage: {str(e)}"
            )

        except requests.exceptions.RequestException as e:

            raise YouCamAPIError(
                f"Image upload request failed: {str(e)}"
            )

        if response.status_code not in (
            200,
            201,
        ):

            raise YouCamAPIError(
                f"Image upload failed: "
                f"{response.status_code} "
                f"{response.text}"
            )

        print("\n========== IMAGE UPLOADED ==========")
        print(f"File ID: {file_id}")
        print(f"Status: {response.status_code}")
        print("====================================\n")

        # --------------------------------------------------------
        # 4. Create YouCam skin analysis task
        # --------------------------------------------------------

        task_response = self.youcam.create_analysis_task(
            file_id=file_id,
        )

        print("\n========== ANALYSIS TASK RESPONSE ==========")
        print(task_response)
        print("============================================\n")

        task_data = task_response.get(
            "data",
            {},
        )

        task_id = task_data.get(
            "task_id"
        )

        if not task_id:
            raise ValueError(
                "YouCam did not return task_id."
            )

        # --------------------------------------------------------
        # 5. Save analysis in local database
        # --------------------------------------------------------

        analysis = SkinAnalysis(
            user_id=user_id,
            youcam_task_id=task_id,
            analysis_status="running",
            image_url=None,
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        print("\n========== DATABASE RECORD CREATED ==========")
        print(
            f"Analysis ID: {analysis.id}"
        )
        print(
            f"YouCam Task ID: {analysis.youcam_task_id}"
        )
        print(
            f"Status: {analysis.analysis_status}"
        )
        print("=============================================\n")

        # --------------------------------------------------------
        # Return
        # --------------------------------------------------------

        return {
            "analysis_id": analysis.id,
            "youcam_task_id": task_id,
            "status": "running",
        }

    # ============================================================
    # CHECK ANALYSIS
    # ============================================================

    def check_analysis(
        self,
        db: Session,
        analysis: SkinAnalysis,
    ):

        # --------------------------------------------------------
        # Validate task ID
        # --------------------------------------------------------

        if not analysis.youcam_task_id:

            raise ValueError(
                "Analysis does not have a YouCam task ID."
            )

        # --------------------------------------------------------
        # Ask YouCam for current task status
        # --------------------------------------------------------

        response = self.youcam.get_analysis_task(
            analysis.youcam_task_id
        )

        print("\n========== ANALYSIS STATUS RESPONSE ==========")
        print(response)
        print("===============================================\n")

        # --------------------------------------------------------
        # Extract data
        # --------------------------------------------------------

        data = response.get(
            "data",
            {},
        )

        task_status = data.get(
            "task_status"
        )

        if not task_status:

            raise ValueError(
                "YouCam did not return task status."
            )

        print(
            f"YouCam Task Status: {task_status}"
        )

        # --------------------------------------------------------
        # Update local status
        # --------------------------------------------------------

        analysis.analysis_status = task_status

        # --------------------------------------------------------
        # Still processing
        # --------------------------------------------------------

        if task_status not in (
            "success",
            "error",
        ):

            db.commit()
            db.refresh(analysis)

            return {
                "status": task_status,
                "analysis": analysis,
            }

        # --------------------------------------------------------
        # Analysis failed
        # --------------------------------------------------------

        if task_status == "error":

            error_message = (
                data.get("error_message")
                or data.get("error")
                or "Skin analysis failed."
            )

            analysis.ai_summary = error_message
            analysis.analysis_status = "error"

            # Store the error response too
            analysis.raw_result = data

            db.commit()
            db.refresh(analysis)

            print("\n========== YOUCAM ANALYSIS ERROR ==========")
            print(error_message)
            print("===========================================\n")

            return {
                "status": "error",
                "analysis": analysis,
            }

        # --------------------------------------------------------
        # Analysis successful
        # --------------------------------------------------------

        result = data.get(
            "results"
        )

        print("\n========== SKIN ANALYSIS RESULT ==========")
        print(result)
        print("===========================================\n")

        # --------------------------------------------------------
        # Process result
        # --------------------------------------------------------

        frontend_result = self.process_result(
            db=db,
            analysis=analysis,
            result=result,
        )

        return {
            "status": "success",
            "analysis": analysis,
            "result": frontend_result,
        }

    # ============================================================
    # PROCESS RESULT
    # ============================================================

    def process_result(
        self,
        db: Session,
        analysis: SkinAnalysis,
        result: Any,
    ):

        # --------------------------------------------------------
        # Store complete YouCam result
        # --------------------------------------------------------

        if isinstance(result, dict):
            analysis.raw_result = result
        else:
            analysis.raw_result = None

        # ========================================================
        # EXTRACT SCORES
        # ========================================================

        scores = self.extract_scores(result)

        print("\n========== EXTRACTED SCORES ==========")
        print(scores)
        print("======================================\n")

        # --------------------------------------------------------
        # Individual scores
        # --------------------------------------------------------

        analysis.hydration_score = scores.get(
            "hydration"
        )

        analysis.texture_score = scores.get(
            "texture"
        )

        analysis.brightness_score = scores.get(
            "brightness"
        )

        analysis.acne_score = scores.get(
            "acne"
        )

        # --------------------------------------------------------
        # Overall health score
        # --------------------------------------------------------

        analysis.skin_health_score = (
            self.calculate_health_score(scores)
        )

        # ========================================================
        # DETECT SKIN CONCERNS
        # ========================================================

        concerns = self.concern_service.detect_concerns(
            scores
        )

        print("\n========== DETECTED CONCERNS ==========")
        print(concerns)
        print("=======================================\n")

        # ========================================================
        # OLLAMA PERSONALIZED SKINCARE PLAN
        # ========================================================

        ai_result = (
            self.ollama_service.generate_skin_recommendation(
                scores=scores,
                concerns=concerns,
            )
        )
        user_profile = db.query(UserProfile).filter(
            UserProfile.user_id == analysis.user_id
        ).first()

    
        user_location = user_profile.location if user_profile else None

        city = None
        state = None
        pincode = None

        if user_location:
            city = user_location.split(",")[0].strip()
            state = user_location.split(",")[1].strip()

        product_result = self.product_recommendation_service.get_recommendations(
            concerns=concerns,
            ingredients=ai_result.get("ingredients", []),
            location=user_location,
        )

        print("\n========== OLLAMA RESULT ==========")
        print(ai_result)
        print(product_result)
        print("===================================\n")

        # --------------------------------------------------------
        # AI Summary
        # --------------------------------------------------------

        analysis.ai_summary = ai_result.get(
            "summary",
            "Your skin analysis has been completed."
        )

        # --------------------------------------------------------
        # AI Recommendation
        # --------------------------------------------------------

        analysis.ai_recommendation = ai_result.get(
            "recommendation",
            ""
        )

        # --------------------------------------------------------
        # Recommended Routine
        # --------------------------------------------------------

        analysis.recommended_routine = ai_result.get(
            "routine",
            {
                "morning": [],
                "night": []
            }
        )

        # --------------------------------------------------------
        # Recommended Ingredients
        # --------------------------------------------------------

        analysis.recommended_ingredients = ai_result.get(
            "ingredients",
            []
        )

        # --------------------------------------------------------
        # Recommended Products
        # --------------------------------------------------------

        analysis.recommended_products = ai_result.get(
            "products",
            []
        )

        # --------------------------------------------------------
        # Real product recommendations
        # --------------------------------------------------------

        product_recommendations = (
            self.product_recommendation_service.recommend_products(
                ingredients=analysis.recommended_ingredients,
                location={
                    "city": city,
                    "state": state,
                    "pincode": pincode,
                    "country": "India",
                },
                budget=None,
            )
        )

        analysis.recommended_products = (
            product_recommendations
        )

        # ========================================================
        # MARK SUCCESSFUL
        # ========================================================

        analysis.analysis_status = "success"

        analysis.analyzed_at = datetime.now(timezone.utc)

        # --------------------------------------------------------
        # Save
        # --------------------------------------------------------

        db.commit()
        db.refresh(analysis)

        frontend_result = {
            "analysis_id": analysis.id,

            "status": analysis.analysis_status,

            "scores": {
                "health": analysis.skin_health_score,
                "hydration": analysis.hydration_score,
                "texture": analysis.texture_score,
                "brightness": analysis.brightness_score,
                "acne": analysis.acne_score,
            },

            "concerns": concerns,

            "ai": {
                "summary": analysis.ai_summary,
                "recommendation": analysis.ai_recommendation,
                "routine": analysis.recommended_routine,
                "ingredients": analysis.recommended_ingredients,
            },

            "location": {
                "country": "India",
                "state": state,
                "city": city,
                "pincode": pincode,
            },

            "products": product_recommendations,

            "analyzed_at": (
                analysis.analyzed_at.isoformat()
                if analysis.analyzed_at
                else None
            ),
        }

        return frontend_result

        print("\n========== ANALYSIS SAVED ==========")

        print(
            f"Analysis ID: "
            f"{analysis.id}"
        )

        print(
            f"Health Score: "
            f"{analysis.skin_health_score}"
        )

        print(
            f"Hydration: "
            f"{analysis.hydration_score}"
        )

        print(
            f"Texture: "
            f"{analysis.texture_score}"
        )

        print(
            f"Brightness: "
            f"{analysis.brightness_score}"
        )

        print(
            f"Acne: "
            f"{analysis.acne_score}"
        )

        print(
            f"AI Summary: "
            f"{analysis.ai_summary}"
        )

        print(
            f"Routine: "
            f"{analysis.recommended_routine}"
        )

        print(
            f"Ingredients: "
            f"{analysis.recommended_ingredients}"
        )

        print(
            f"Products: "
            f"{analysis.recommended_products}"
        )

        print("====================================\n")

    # ============================================================
    # EXTRACT SCORES
    # ============================================================

    def extract_scores(
        self,
        result: Any,
    ) -> Dict[str, float]:

        scores: Dict[str, float] = {}

        if not isinstance(result, dict):
            return scores

        output = result.get("output", [])

        if not isinstance(output, list):
            return scores

        for item in output:

            if not isinstance(item, dict):
                continue

            result_type = str(
                item.get("type", "")
            ).lower()

            # Prefer ui_score because it is the user-facing score
            score = item.get("ui_score")

            if score is None:
                score = item.get("score")

            if score is None:
                continue

            try:
                score = float(score)
            except (TypeError, ValueError):
                continue

            # ========================================================
            # HYDRATION / MOISTURE
            # ========================================================

            if "moisture" in result_type:
                scores["hydration"] = score

            # ========================================================
            # TEXTURE
            # ========================================================

            elif "texture" in result_type:
                scores["texture"] = score

            # ========================================================
            # RADIANCE / BRIGHTNESS
            # ========================================================

            elif "radiance" in result_type:
                scores["brightness"] = score

            # ========================================================
            # ACNE
            # ========================================================

            elif "acne" in result_type:
                scores["acne"] = score

        return scores

    # ============================================================
    # RECURSIVE SCORE SEARCH
    # ============================================================

    def _recursive_score_search(
        self,
        obj: Any,
        scores: Dict[str, float],
    ):

        # --------------------------------------------------------
        # Dictionary
        # --------------------------------------------------------

        if isinstance(obj, dict):

            # ----------------------------------------------------
            # YouCam result item
            #
            # Example:
            #
            # {
            #     "ui_score": 66,
            #     "raw_score": 38.39,
            #     "type": "hd_moisture"
            # }
            # ----------------------------------------------------

            result_type = obj.get("type")

            if isinstance(result_type, str):

                normalized_type = (
                    result_type
                    .lower()
                    .replace("-", "_")
                    .replace(" ", "_")
                )

                # -----------------------------------------------
                # Use raw_score when available
                # -----------------------------------------------

                score = obj.get("raw_score")

                # Fallback to ui_score
                if score is None:
                    score = obj.get("ui_score")

                if isinstance(
                    score,
                    (int, float),
                ):

                    # -------------------------------------------
                    # Moisture / Hydration
                    # -------------------------------------------

                    if (
                        "moisture"
                        in normalized_type
                        or
                        "hydration"
                        in normalized_type
                    ):

                        scores.setdefault(
                            "hydration",
                            float(score),
                        )

                    # -------------------------------------------
                    # Texture
                    # -------------------------------------------

                    elif "texture" in normalized_type:

                        # Prefer whole-face texture
                        region = obj.get("region")

                        if (
                            "texture"
                            not in scores
                            or
                            region == "whole"
                        ):

                            scores["texture"] = float(score)

                    # -------------------------------------------
                    # Radiance / Brightness
                    # -------------------------------------------

                    elif (
                        "radiance"
                        in normalized_type
                        or
                        "brightness"
                        in normalized_type
                    ):

                        scores.setdefault(
                            "brightness",
                            float(score),
                        )

                    # -------------------------------------------
                    # Acne
                    # -------------------------------------------

                    elif "acne" in normalized_type:

                        scores.setdefault(
                            "acne",
                            float(score),
                        )

            # ----------------------------------------------------
            # Recursively inspect nested values
            # ----------------------------------------------------

            for key, value in obj.items():

                if isinstance(
                    value,
                    (
                        dict,
                        list,
                    ),
                ):

                    self._recursive_score_search(
                        value,
                        scores,
                    )

        # --------------------------------------------------------
        # List
        # --------------------------------------------------------

        elif isinstance(obj, list):

            for item in obj:

                self._recursive_score_search(
                    item,
                    scores,
                )

    # ============================================================
    # CALCULATE HEALTH SCORE
    # ============================================================

    def calculate_health_score(
        self,
        scores: Dict[str, float],
    ) -> Optional[float]:

        available = []

        for key in [
            "hydration",
            "texture",
            "brightness",
        ]:

            value = scores.get(
                key
            )

            if value is not None:

                available.append(
                    value
                )

        if not available:

            return None

        return round(
            sum(available)
            / len(available),
            2,
        )

    # ============================================================
    # GENERATE SUMMARY
    # ============================================================

    def generate_summary(
        self,
        scores: Dict[str, float],
    ) -> str:

        if not scores:

            return (
                "Your skin analysis has been completed."
            )

        parts = []

        # --------------------------------------------------------
        # Hydration
        # --------------------------------------------------------

        if "hydration" in scores:

            parts.append(
                f"Hydration score: "
                f"{scores['hydration']:.1f}"
            )

        # --------------------------------------------------------
        # Texture
        # --------------------------------------------------------

        if "texture" in scores:

            parts.append(
                f"Texture score: "
                f"{scores['texture']:.1f}"
            )

        # --------------------------------------------------------
        # Brightness
        # --------------------------------------------------------

        if "brightness" in scores:

            parts.append(
                f"Radiance score: "
                f"{scores['brightness']:.1f}"
            )

        # --------------------------------------------------------
        # Acne
        # --------------------------------------------------------

        if "acne" in scores:

            parts.append(
                f"Acne score: "
                f"{scores['acne']:.1f}"
            )

        return " | ".join(
            parts
        )

    # ============================================================
    # GENERATE RECOMMENDATION
    # ============================================================

    def generate_recommendation(
        self,
        scores: Dict[str, float],
    ) -> str:

        recommendations = []

        hydration = scores.get(
            "hydration"
        )

        texture = scores.get(
            "texture"
        )

        acne = scores.get(
            "acne"
        )

        # --------------------------------------------------------
        # Hydration
        # --------------------------------------------------------

        if (
            hydration is not None
            and hydration < 50
        ):

            recommendations.append(
                "Consider adding hydrating "
                "skincare products to your routine."
            )

        # --------------------------------------------------------
        # Texture
        # --------------------------------------------------------

        if (
            texture is not None
            and texture < 50
        ):

            recommendations.append(
                "Consider a gentle routine focused "
                "on improving skin texture."
            )

        # --------------------------------------------------------
        # Acne
        # --------------------------------------------------------

        if (
            acne is not None
            and acne < 50
        ):

            recommendations.append(
                "Consider products formulated for "
                "blemish-prone skin."
            )

        # --------------------------------------------------------
        # Everything looks balanced
        # --------------------------------------------------------

        if not recommendations:

            recommendations.append(
                "Your detected skin metrics look "
                "generally balanced. Continue with "
                "a consistent skincare routine."
            )

        return " ".join(
            recommendations
        )

    # ============================================================
    # RESIZE / NORMALIZE IMAGE
    # ============================================================

    def resize_image(
        self,
        file_bytes: bytes,
        min_width: int = 1024,
        min_height: int = 1024,
    ) -> bytes:

        try:

            # ----------------------------------------------------
            # Open image
            # ----------------------------------------------------

            image = Image.open(
                BytesIO(file_bytes)
            )

            # ----------------------------------------------------
            # Force PIL to actually load image
            # ----------------------------------------------------

            image.load()

            print(
                "\n========== ORIGINAL IMAGE =========="
            )

            print(
                f"Width: {image.width}"
            )

            print(
                f"Height: {image.height}"
            )

            print(
                f"Format: {image.format}"
            )

            print(
                f"Mode: {image.mode}"
            )

            print(
                "====================================\n"
            )

            width = image.width
            height = image.height

            # ----------------------------------------------------
            # Calculate scale
            #
            # IMPORTANT:
            # We use max() so BOTH dimensions reach the minimum.
            # ----------------------------------------------------

            scale = max(
                min_width / width,
                min_height / height,
                1.0,
            )

            new_width = int(
                round(width * scale)
            )

            new_height = int(
                round(height * scale)
            )

            # ----------------------------------------------------
            # Resize if required
            # ----------------------------------------------------

            if (
                new_width != width
                or
                new_height != height
            ):

                image = image.resize(
                    (
                        new_width,
                        new_height,
                    ),
                    Image.Resampling.LANCZOS,
                )

            # ----------------------------------------------------
            # Convert image to RGB
            #
            # JPEG does not support RGBA / P / LA.
            # ----------------------------------------------------

            if image.mode != "RGB":

                if image.mode in (
                    "RGBA",
                    "LA",
                ):

                    background = Image.new(
                        "RGB",
                        image.size,
                        "white",
                    )

                    alpha = image.getchannel(
                        "A"
                    )

                    background.paste(
                        image,
                        mask=alpha,
                    )

                    image = background

                else:

                    image = image.convert(
                        "RGB"
                    )

            # ----------------------------------------------------
            # Save as JPEG
            # ----------------------------------------------------

            output = BytesIO()

            image.save(
                output,
                format="JPEG",
                quality=95,
                optimize=True,
            )

            resized_bytes = (
                output.getvalue()
            )

            # ----------------------------------------------------
            # Verify resulting image
            # ----------------------------------------------------

            verify_image = Image.open(
                BytesIO(resized_bytes)
            )

            verify_width = (
                verify_image.width
            )

            verify_height = (
                verify_image.height
            )

            print(
                "\n========== PROCESSED IMAGE =========="
            )

            print(
                f"Width: {verify_width}"
            )

            print(
                f"Height: {verify_height}"
            )

            print(
                f"Format: {verify_image.format}"
            )

            print(
                f"Size: {len(resized_bytes)} bytes"
            )

            print(
                "=====================================\n"
            )

            # ----------------------------------------------------
            # Final safety validation
            # ----------------------------------------------------

            if (
                verify_width < min_width
                or
                verify_height < min_height
            ):

                raise ValueError(
                    "Unable to resize image to the "
                    "required minimum resolution."
                )

            return resized_bytes

        except Exception as e:

            raise ValueError(
                f"Unable to process uploaded image: {str(e)}"
            )