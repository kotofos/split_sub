from django.shortcuts import render

from split import split_subs
from .forms import SplitForm


def get_split(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SplitForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            clean_sub = split_subs.run(
                form.cleaned_data['sub_text']
            )
            form = SplitForm(
                data={'sub_text': clean_sub})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SplitForm()

    return render(request, 'index.html', {'form': form})
