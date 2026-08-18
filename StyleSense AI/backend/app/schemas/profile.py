from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# ============================================================
# MASTER / DISPLAY SCHEMAS
# ============================================================

class MasterItem(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# SKIN PROFILE
# ============================================================

class SkinProfileUpdate(BaseModel):
    skin_tone_id: Optional[int] = None
    skin_type_id: Optional[int] = None
    skin_concern_ids: List[int] = []


class SkinProfileResponse(BaseModel):
    skin_tone: Optional[MasterItem] = None
    skin_type: Optional[MasterItem] = None
    skin_concerns: List[MasterItem] = []

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# USER PROFILE UPDATE
# ============================================================

class ProfileUpdate(BaseModel):
    phone: Optional[str] = None
    location: Optional[str] = None
    date_of_birth: Optional[date] = None

    # Body
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    body_type_id: Optional[int] = None
    fit_preference_id: Optional[int] = None

    # Shopping
    budget: Optional[float] = None
    shopping_frequency: Optional[str] = None
    preferred_shopping: Optional[str] = None
    sustainable_fashion: Optional[str] = None

    # Measurements
    chest_cm: Optional[float] = None
    waist_cm: Optional[float] = None
    hip_cm: Optional[float] = None
    shoulder_cm: Optional[float] = None
    sleeve_length_cm: Optional[float] = None
    shoe_size: Optional[float] = None

    # Skin
    skin_tone_id: Optional[int] = None
    skin_type_id: Optional[int] = None
    skin_concern_ids: List[int] = []


# ============================================================
# PROFILE RESPONSE
# ============================================================

class ProfileResponse(BaseModel):
    # User information
    id: int
    full_name: str
    email: EmailStr
    profile_image: Optional[str] = None
    gender: Optional[str] = None
    is_active: bool

    # Personal information
    phone: Optional[str] = None
    location: Optional[str] = None
    date_of_birth: Optional[date] = None

    # Body profile
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None

    body_type: Optional[MasterItem] = None
    fit_preference: Optional[MasterItem] = None

    # Skin profile
    skin_profile: Optional[SkinProfileResponse] = None

    # Shopping preferences
    budget: Optional[float] = None
    shopping_frequency: Optional[str] = None
    preferred_shopping: Optional[str] = None
    sustainable_fashion: Optional[str] = None

    # Measurements
    chest_cm: Optional[float] = None
    waist_cm: Optional[float] = None
    hip_cm: Optional[float] = None
    shoulder_cm: Optional[float] = None
    sleeve_length_cm: Optional[float] = None
    shoe_size: Optional[float] = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)