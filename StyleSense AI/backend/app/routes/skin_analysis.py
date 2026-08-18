from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db

from app.integrations.youcam import (
    YouCamAPIError,
)

from app.models.user import User
from app.models.skin_analysis import SkinAnalysis

from app.schemas.skin_analysis import (
    SkinAnalysisStartResponse,
)

from app.services.skin_analysis import (
    SkinAnalysisService,
)


router = APIRouter(
    prefix="/skin-analysis",
    tags=["Skin Analysis"],
)

service = SkinAnalysisService()


# =====================================================
# START ANALYSIS
# =====================================================

@router.post(
    "",
    response_model=SkinAnalysisStartResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def start_skin_analysis(
    file: UploadFile = File(...),
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    # -----------------------------------------------
    # Validate content type
    # -----------------------------------------------

    allowed_types = {
        "image/jpeg",
        "image/jpg",
        "image/png",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=(
                "Only JPEG and PNG images "
                "are supported."
            ),
        )

    try:

        file_bytes = file.file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty.",
            )

        result = service.start_analysis(
            db=db,
            user_id=current_user.id,
            file_name=file.filename
            or "skin_analysis.jpg",
            content_type=file.content_type
            or "image/jpeg",
            file_bytes=file_bytes,
        )

        return result

    except YouCamAPIError as e:

        raise HTTPException(
            status_code=502,
            detail={
                "message": e.message,
                "youcam_status": e.status_code,
                "response": e.response_data,
            },
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# =====================================================
# CHECK ANALYSIS STATUS / RESULT
# =====================================================

@router.get(
    "/{analysis_id}",
)
def get_skin_analysis(
    analysis_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    analysis = (
        db.query(SkinAnalysis)
        .filter(
            SkinAnalysis.id == analysis_id,
            SkinAnalysis.user_id
            == current_user.id,
        )
        .first()
    )

    if not analysis:

        raise HTTPException(
            status_code=404,
            detail="Skin analysis not found.",
        )

    try:

        result = service.check_analysis(
            db=db,
            analysis=analysis,
        )

        return {
            "analysis_id": analysis.id,

            # NEW MODEL FIELD
            "youcam_task_id":
                analysis.youcam_task_id,

            # CURRENT STATUS
            "status":
                result["status"],

            # NEW MODEL FIELD
            "analysis_status":
                analysis.analysis_status,

            "skin_health_score":
                analysis.skin_health_score,

            "hydration_score":
                analysis.hydration_score,

            "texture_score":
                analysis.texture_score,

            "brightness_score":
                analysis.brightness_score,

            "acne_score":
                analysis.acne_score,

            "ai_summary":
                analysis.ai_summary,

            "ai_recommendation":
                analysis.ai_recommendation,

            "recommended_routine":
                analysis.recommended_routine,

            "recommended_ingredients":
                analysis.recommended_ingredients,

            "recommended_products":
                analysis.recommended_products,

            "raw_result":
                analysis.raw_result,

            "analyzed_at":
                analysis.analyzed_at,

            "created_at":
                analysis.created_at,

            "updated_at":
                analysis.updated_at,
        }

    except YouCamAPIError as e:

        raise HTTPException(
            status_code=502,
            detail={
                "message": e.message,
                "youcam_status": e.status_code,
                "response": e.response_data,
            },
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# =====================================================
# ANALYSIS HISTORY
# =====================================================

@router.get("")
def get_skin_analysis_history(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    analyses = (
        db.query(SkinAnalysis)
        .filter(
            SkinAnalysis.user_id
            == current_user.id
        )
        .order_by(
            SkinAnalysis.analyzed_at.desc()
        )
        .all()
    )

    return {
        "total": len(analyses),

        "analyses": [

            {
                "id": analysis.id,

                "youcam_task_id":
                    analysis.youcam_task_id,

                "status":
                    analysis.analysis_status,

                "skin_health_score":
                    analysis.skin_health_score,

                "hydration_score":
                    analysis.hydration_score,

                "texture_score":
                    analysis.texture_score,

                "brightness_score":
                    analysis.brightness_score,

                "acne_score":
                    analysis.acne_score,

                "ai_summary":
                    analysis.ai_summary,

                "ai_recommendation":
                    analysis.ai_recommendation,

                "raw_result":
                    analysis.raw_result,

                "analyzed_at":
                    analysis.analyzed_at,

                "created_at":
                    analysis.created_at,

                "updated_at":
                    analysis.updated_at,
            }

            for analysis in analyses
        ],
    }