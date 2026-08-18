from typing import Any, Dict

from app.integrations.youcam.client import (
    YouCamClient,
)


class YouCamSkinAnalysis:

    def __init__(self):
        self.client = YouCamClient()

    # --------------------------------------------------
    # STEP 1
    # Request an upload URL from YouCam
    # --------------------------------------------------

    def create_file_upload(
        self,
        file_name: str,
        content_type: str,
        file_size: int,
    ) -> Dict[str, Any]:

        payload = {
            "files": [
                {
                    "content_type": content_type,
                    "file_name": file_name,
                    "file_size": file_size,
                }
            ]
        }

        return self.client.post(
            "/s2s/v2.1/file/skin-analysis",
            payload,
        )

    # --------------------------------------------------
    # STEP 2
    # Upload image to presigned URL
    # --------------------------------------------------

    def upload_image(
        self,
        upload_url: str,
        file_bytes: bytes,
        content_type: str,
    ):

        return self.client.put_presigned_url(
            url=upload_url,
            file_bytes=file_bytes,
            content_type=content_type,
        )

    # --------------------------------------------------
    # STEP 3
    # Create skin analysis task
    # --------------------------------------------------

    def create_analysis_task(
        self,
        file_id: str,
    ) -> Dict[str, Any]:

        payload = {
            "src_file_id": file_id,

            "dst_actions": [
                "hd_acne",
                "hd_texture",
                "hd_pore",
                "hd_wrinkle",
                "hd_redness",
                "hd_oiliness",
                "hd_radiance",
                "hd_moisture",
                "hd_dark_circle",
                "hd_eye_bag",
                "hd_age_spot",
            ],

            "miniserver_args": {
                "enable_mask_overlay": True,
            },

            "format": "json",

            "pf_camera_kit": True,
        }

        return self.client.post(
            "/s2s/v2.1/task/skin-analysis",
            payload,
        )

    # --------------------------------------------------
    # STEP 4
    # Check task status
    # --------------------------------------------------

    def get_analysis_task(
        self,
        task_id: str,
    ) -> Dict[str, Any]:

        return self.client.get(
            f"/s2s/v2.1/task/skin-analysis/{task_id}"
        )