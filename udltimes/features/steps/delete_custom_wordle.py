from behave import when, then
from udltimes.models import CustomWordle


@when('I visit the delete page for wordle "{word}"')
def step_visit_delete_page(context, word):
    wordle = CustomWordle.objects.get(word=word.upper())
    context.browser.visit(context.get_url('wordle_delete', pk=wordle.pk))


@when('I click the delete button')
def step_click_delete(context):
    context.browser.find_by_css('[type="submit"]').first.click()


@then('I should be on the home page')
def step_on_home_page(context):
    assert context.browser.url.endswith('/') or 'home' in context.browser.url


@then('The wordle "{word}" should not exist')
def step_wordle_not_exists(context, word):
    assert not CustomWordle.objects.filter(word=word.upper()).exists(), f"Wordle {word} should not exist"