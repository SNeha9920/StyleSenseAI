from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Login Page dataabse
class user_login(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    email = models.EmailField(null=False, blank=False)
    created_at = models.DateTimeField(null=False)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "user_login"

# Tokens
class Tokens(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=255)
    valid_upto = models.DateTimeField(blank=True, null=True)
    login_at = models.DateTimeField(default=timezone.now)
    logged_out_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(user_login, related_name='TOKEN', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tokens'

# ==========================================
# PROFILE & USER SETTINGS
# ==========================================

class UserProfile(models.Model):
    user = models.OneToOneField(user_login, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profiles/avatars/', blank=True, null=True)
    tagline = models.CharField(max_length=100, default="AI Fashion Enthusiast")
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # Body Profile
    height_cm = models.FloatField(blank=True, null=True)
    weight_kg = models.FloatField(blank=True, null=True)
    body_type = models.CharField(max_length=50, blank=True)
    fit_preference = models.CharField(max_length=50, blank=True)

    # Skin Profile
    skin_tone = models.CharField(max_length=50, blank=True)
    skin_type = models.CharField(max_length=50, blank=True)
    skin_concerns = models.TextField(blank=True)

    # Style & Shopping Preferences
    style_preferences = models.JSONField(default=list, blank=True)
    shopping_budget = models.CharField(max_length=50, blank=True)
    shopping_frequency = models.CharField(max_length=50, blank=True)
    preferred_shopping = models.CharField(max_length=50, blank=True)
    sustainable_fashion = models.BooleanField(default=False)
    favorite_brands = models.JSONField(default=list, blank=True)

    # Body Measurements (cm / size)
    chest_cm = models.FloatField(blank=True, null=True)
    waist_cm = models.FloatField(blank=True, null=True)
    hip_cm = models.FloatField(blank=True, null=True)
    shoulder_cm = models.FloatField(blank=True, null=True)
    sleeve_length_cm = models.FloatField(blank=True, null=True)
    shoe_size = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'user_profiles'


class UserSettings(models.Model):
    user = models.OneToOneField(user_login, on_delete=models.CASCADE, related_name='settings')

    # Appearance Settings
    theme = models.CharField(max_length=10, default='Light', choices=[('Light', 'Light'), ('Dark', 'Dark'), ('System', 'System')])
    accent_color = models.CharField(max_length=20, default='Purple')

    # Notification Toggles
    notify_ai_analysis = models.BooleanField(default=True)
    notify_weekly_report = models.BooleanField(default=True)
    notify_product_recommendations = models.BooleanField(default=True)
    notify_wardrobe_suggestions = models.BooleanField(default=True)
    notify_new_features = models.BooleanField(default=True)

    # Privacy Options
    save_uploaded_photos = models.BooleanField(default=True)
    ai_personalization = models.BooleanField(default=True)
    anonymous_analytics = models.BooleanField(default=True)
    face_detection_permission = models.BooleanField(default=True)
    location_access = models.BooleanField(default=False)

    # AI Preferences
    ai_personality = models.CharField(max_length=50, default='Fashion Expert')
    response_length = models.CharField(max_length=20, default='Short')
    creativity_level = models.IntegerField(default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])

    # Security Options
    two_factor_auth = models.BooleanField(default=False)
    login_alerts = models.BooleanField(default=True)
    show_active_sessions = models.BooleanField(default=True)
    remember_trusted_devices = models.BooleanField(default=True)
    biometric_authentication = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_settings'


# ==========================================
# WARDROBE & OUTFIT COLLECTIONS
# ==========================================

class WardrobeItem(models.Model):
    user = models.ForeignKey(user_login, on_delete=models.CASCADE, related_name='wardrobe_items')
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50)
    season = models.CharField(max_length=50, blank=True)
    occasion = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='wardrobe/')
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wardrobe_items'


class OutfitCollection(models.Model):
    user = models.ForeignKey(user_login, on_delete=models.CASCADE, related_name='outfit_collections')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    items = models.ManyToManyField(WardrobeItem, related_name='collections')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'outfit_collections'


# ==========================================
# SKIN ANALYSIS & VIRTUAL TRY-ON
# ==========================================

class SkinAnalysis(models.Model):
    user_id = models.IntegerField()
    youcam_task_id = models.CharField(max_length=255, null=True, blank=True)
    analysis_status = models.CharField(max_length=50, default='pending')
    skin_health_score = models.IntegerField(null=True, blank=True)
    hydration_score = models.IntegerField(null=True, blank=True)
    texture_score = models.IntegerField(null=True, blank=True)
    brightness_score = models.IntegerField(null=True, blank=True)
    acne_score = models.IntegerField(null=True, blank=True)
    ai_summary = models.TextField(null=True, blank=True)
    ai_recommendation = models.TextField(null=True, blank=True)
    recommended_routine = models.TextField(null=True, blank=True)
    recommended_ingredients = models.JSONField(null=True, blank=True)
    recommended_products = models.JSONField(null=True, blank=True)
    raw_result = models.JSONField(null=True, blank=True)
    analyzed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skin_analyses'  # Verify this matches your SQLAlchemy __tablename__
        managed = False


class VirtualTryOn(models.Model):
    user = models.ForeignKey(user_login, on_delete=models.CASCADE, related_name='virtual_tryons')
    original_photo = models.ImageField(upload_to='try_on/originals/')
    result_photo = models.ImageField(upload_to='try_on/results/', blank=True, null=True)

    outfit_source = models.CharField(max_length=50, default='My Wardrobe')
    outfit_name = models.CharField(max_length=100, blank=True)
    match_score = models.IntegerField(default=0)

    # Score breakdown
    skin_tone_score = models.IntegerField(default=0)
    body_shape_score = models.IntegerField(default=0)
    occasion_score = models.IntegerField(default=0)
    season_score = models.IntegerField(default=0)

    ai_feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'virtual_try_ons'


# ==========================================
# AI STYLIST CHAT HISTORY
# ==========================================

class AIStylistSession(models.Model):
    user = models.ForeignKey(user_login, on_delete=models.CASCADE, related_name='stylist_sessions')
    title = models.CharField(max_length=150, default="New Conversation")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_stylist_sessions'


class ChatMessage(models.Model):
    session = models.ForeignKey(AIStylistSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('ai', 'AI Stylist')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_messages'