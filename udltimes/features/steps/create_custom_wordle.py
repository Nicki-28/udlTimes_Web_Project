from behave import when, then


@when('I visit the wordle creation page')
def step_visit_create_page(context):
    context.browser.visit(context.get_url('wordle_create'))


@then('I should see an error message about the word length')
def step_error_length(context):
    assert '5' in context.browser.html and ('letter' in context.browser.html.lower() or 'long' in context.browser.html.lower())


@then('I should see an error message about only letters allowed')
def step_error_letters(context):
    assert 'letter' in context.browser.html.lower() or 'only' in context.browser.html.lower()