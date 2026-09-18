from django.shortcuts import get_object_or_404, render
from .models import Guest, Invitation


def invitation_detail(request, slug):
    invitation = get_object_or_404(Invitation, slug=slug)
    guest_token = request.GET.get("guest")
    guest = None

    if guest_token:

        guest = Guest.objects.filter(
            invitation=invitation, token=guest_token
        ).first()

    context = {
        "invitation": invitation,
        "guest": guest,
    }
    return render(request, "invitations/detail.html", context)

def home_view(request):
    invitation = Invitation.objects.last()

    if invitation and getattr(invitation, 'music', None):
        try:
            print("Музыкалык файл табылды:", invitation.music.url)
        except Exception as e:
            print("Музыкалык файлдын URL алууда ката чыкты:", e)

    return render(request, "invitations/detail.html", {"invitation": invitation})