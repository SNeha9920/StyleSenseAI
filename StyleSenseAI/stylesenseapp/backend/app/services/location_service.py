from typing import Optional, Dict


class LocationService:

    def normalize_location(
        self,
        city: Optional[str] = None,
        state: Optional[str] = None,
        pincode: Optional[str] = None,
        country: str = "India",
    ) -> Dict:

        return {
            "country": country.strip() if country else "India",
            "state": state.strip() if state else None,
            "city": city.strip() if city else None,
            "pincode": self.normalize_pincode(pincode),
        }

    def normalize_pincode(
        self,
        pincode: Optional[str],
    ) -> Optional[str]:

        if not pincode:
            return None

        pincode = str(pincode).strip()

        if not pincode.isdigit():
            raise ValueError(
                "Pincode must contain only numbers."
            )

        if len(pincode) != 6:
            raise ValueError(
                "Indian pincode must contain 6 digits."
            )

        return pincode

    def is_india(
        self,
        location: Dict,
    ) -> bool:

        return (
            location.get("country", "India")
            .strip()
            .lower()
            == "india"
        )