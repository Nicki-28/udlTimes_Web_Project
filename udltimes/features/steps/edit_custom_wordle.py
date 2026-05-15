from behave import when
from udltimes.models import CustomWordle


@when('I visit the edit page for wordle "{word}"')
def step_visit_edit_page(context, word):
    wordle = CustomWordle.objects.get(word=word.upper())
    context.browser.visit(context.get_url('wordle_update', pk=wordle.pk))