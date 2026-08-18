from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.user_skin_profile import UserSkinProfile
from app.models.user_skin_concern import UserSkinConcern

from app.schemas.profile import ProfileResponse, ProfileUpdate

from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


# ============================================================
# GET PROFILE
# ============================================================

@router.get(
    "",
    response_model=ProfileResponse,
)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == current_user.id)
        .first()
    )

    skin_profile = (
        db.query(UserSkinProfile)
        .filter(UserSkinProfile.user_id == current_user.id)
        .first()
    )

    if not profile:
        profile = UserProfile(
            user_id=current_user.id
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

    if not skin_profile:
        skin_profile = UserSkinProfile(
            user_id=current_user.id
        )

        db.add(skin_profile)
        db.commit()
        db.refresh(skin_profile)

    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "profile_image": current_user.profile_image,
        "gender": current_user.gender,
        "is_active": current_user.is_active,

        "phone": profile.phone,
        "location": profile.location,
        "date_of_birth": profile.date_of_birth,

        "height_cm": profile.height_cm,
        "weight_kg": profile.weight_kg,

        "body_type": profile.body_type,
        "fit_preference": profile.fit_preference,

        "skin_profile": skin_profile,

        "budget": profile.budget,
        "shopping_frequency": profile.shopping_frequency,
        "preferred_shopping": profile.preferred_shopping,
        "sustainable_fashion": profile.sustainable_fashion,

        "chest_cm": profile.chest_cm,
        "waist_cm": profile.waist_cm,
        "hip_cm": profile.hip_cm,
        "shoulder_cm": profile.shoulder_cm,
        "sleeve_length_cm": profile.sleeve_length_cm,
        "shoe_size": profile.shoe_size,

        "created_at": profile.created_at,
        "updated_at": profile.updated_at,
    }


# ============================================================
# UPDATE PROFILE
# ============================================================

@router.put(
    "",
    response_model=ProfileResponse,
)
def update_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == current_user.id)
        .first()
    )

    if not profile:
        profile = UserProfile(
            user_id=current_user.id
        )

        db.add(profile)

    # --------------------------------------------------------
    # USER FIELDS
    # --------------------------------------------------------

    # We deliberately keep full_name in users.
    # Profile does NOT contain first_name / last_name.

    # --------------------------------------------------------
    # PROFILE FIELDS
    # --------------------------------------------------------

    profile.phone = data.phone
    profile.location = data.location
    profile.date_of_birth = data.date_of_birth

    profile.height_cm = data.height_cm
    profile.weight_kg = data.weight_kg

    profile.body_type_id = data.body_type_id
    profile.fit_preference_id = data.fit_preference_id

    profile.budget = data.budget
    profile.shopping_frequency = data.shopping_frequency
    profile.preferred_shopping = data.preferred_shopping
    profile.sustainable_fashion = data.sustainable_fashion

    profile.chest_cm = data.chest_cm
    profile.waist_cm = data.waist_cm
    profile.hip_cm = data.hip_cm
    profile.shoulder_cm = data.shoulder_cm
    profile.sleeve_length_cm = data.sleeve_length_cm
    profile.shoe_size = data.shoe_size

    # --------------------------------------------------------
    # SKIN PROFILE
    # --------------------------------------------------------

    skin_profile = (
        db.query(UserSkinProfile)
        .filter(UserSkinProfile.user_id == current_user.id)
        .first()
    )

    if not skin_profile:
        skin_profile = UserSkinProfile(
            user_id=current_user.id
        )
        db.add(skin_profile)

    skin_profile.skin_tone_id = data.skin_tone_id
    skin_profile.skin_type_id = data.skin_type_id

    # --------------------------------------------------------
    # SKIN CONCERNS
    # --------------------------------------------------------

    existing_concerns = (
        db.query(UserSkinConcern)
        .filter(
            UserSkinConcern.user_id == current_user.id
        )
        .all()
    )

    for concern in existing_concerns:
        db.delete(concern)

    for concern_id in data.skin_concern_ids:

        db.add(
            UserSkinConcern(
                user_id=current_user.id,
                skin_concern_id=concern_id,
            )
        )

    db.commit()

    db.refresh(profile)
    db.refresh(skin_profile)

    return get_profile(
        current_user=current_user,
        db=db,
    )