from .models import Genre


def sidebar(request):
    genre = Genre.objects.all()
    context = {
        "gen": genre
    }
    return context
