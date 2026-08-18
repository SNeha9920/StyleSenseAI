from typing import Any, Dict, Optional

import httpx

from app.core.config import settings


class YouCamAPIError(Exception):
    """Raised when the YouCam API returns an error."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Any] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data

        super().__init__(message)


class YouCamClient:
    """
    Low-level HTTP client for Perfect Corp / YouCam API.
    """

    def __init__(self):
        self.base_url = settings.YOUCAM_BASE_URL.rstrip("/")
        self.api_key = settings.YOUCAM_API_KEY

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        self.timeout = httpx.Timeout(
            connect=30.0,
            read=120.0,
            write=120.0,
            pool=30.0,
        )

    def _handle_response(
        self,
        response: httpx.Response,
    ) -> Dict[str, Any]:

        try:
            data = response.json()
        except Exception:
            data = response.text

        if response.status_code >= 400:
            raise YouCamAPIError(
                message=f"YouCam API request failed: {response.status_code}",
                status_code=response.status_code,
                response_data=data,
            )

        return data

    def post(
        self,
        endpoint: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:

        url = f"{self.base_url}{endpoint}"

        print("\n========== YOUCAM REQUEST ==========")
        print("URL:", url)
        print("PAYLOAD:", payload)
        print("====================================\n")

        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                url,
                headers=self.headers,
                json=payload,
            )

        print("\n========== YOUCAM RESPONSE =========")
        print("STATUS:", response.status_code)
        print("BODY:", response.text)
        print("====================================\n")

        response.raise_for_status()

        return response.json()

        """url = f"{self.base_url}{endpoint}"
                        
                                with httpx.Client(
                                    timeout=self.timeout
                                ) as client:
                        
                                    response = client.post(
                                        url,
                                        headers=self.headers,
                                        json=payload,
                                    )
                        
                                return self._handle_response(response)"""

    def get(
        self,
        endpoint: str,
    ) -> Dict[str, Any]:

        url = f"{self.base_url}{endpoint}"

        with httpx.Client(
            timeout=self.timeout
        ) as client:

            response = client.get(
                url,
                headers=self.headers,
            )

        return self._handle_response(response)

    def put_presigned_url(
        self,
        url: str,
        file_bytes: bytes,
        content_type: str,
    ):

        headers = {
            "Content-Type": content_type,
            "Content-Length": str(len(file_bytes)),
        }

        with httpx.Client(
            timeout=self.timeout
        ) as client:

            response = client.put(
                url,
                headers=headers,
                content=file_bytes,
            )

        if response.status_code >= 400:
            raise YouCamAPIError(
                message=(
                    "Failed to upload image to "
                    "YouCam presigned URL"
                ),
                status_code=response.status_code,
                response_data=response.text,
            )

        return True