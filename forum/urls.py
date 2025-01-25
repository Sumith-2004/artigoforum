from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', home, name='home'),# Home Page
    path('category/<str:category_name>/', filter_artwork, name='category_filter'),# Path for filtering artworks based on category
    path('tag/<str:tag_name>/', filter_artwork, name='tag_filter'),# Path for filtering artworks based on tag
    path('category/<str:category_name>/tag/<str:tag_name>/', filter_artwork, name='category_tag_filter'),# Path for filtering artworks based on category and tag
    path('like_artwork/<int:artwork_id>/', like_artwork, name='like_artwork'),# Path for liking a artwork
    path('like_comment/<int:comment_id>/', like_comment, name=' like_comment'),# Path for liking a comment`
    path('signup/', signup, name='signup'),# Path for signup
    path('login/', login_view, name='login'),# Path for login
    path('logout/',logout_view, name='logout'),# Path for logout
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/<int:user_id>/', profile, name='profile'),# Path for user profile

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    