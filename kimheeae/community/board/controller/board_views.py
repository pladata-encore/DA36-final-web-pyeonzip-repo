from django.shortcuts import render
from django.template.defaultfilters import title

from board.entity.models import Board, BoardForm


# Create your views here.


def community_main(request):
    return render(request, 'board/../../templates/community_main.html', {})


def board_list(request):
    boards = Board.objects.all()
    return render(request, 'board/board_list.html', {'boards':boards})

def board_write(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            # form.save()
            pass
        else:
            form = BoardForm()

        print(request.POST)
    return render(request, 'board/board_write.html', {'BoardForm':BoardForm})