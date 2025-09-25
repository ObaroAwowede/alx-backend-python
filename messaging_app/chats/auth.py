from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

get_token = TokenObtainPairView.as_view()
refresh_token = TokenRefreshView.as_view()

__all__ = ["get_token","refresh_token"]