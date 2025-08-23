from src.utils.config import get_settings
from supabase import create_client, Client


class SupabaseClient:
    _client: Client = None

    @staticmethod
    def get_client() -> Client:
        if SupabaseClient._client is None:
            app_settings = get_settings()
            url = app_settings.SUPABASE_URL
            key = app_settings.SUPABASE_KEY

            if not url or not key:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

            SupabaseClient._client = create_client(url, key)

        return SupabaseClient._client
