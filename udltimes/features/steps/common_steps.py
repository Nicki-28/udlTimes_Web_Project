from behave import given, when, then
from django.contrib.auth.models import User
from udltimes.models import CustomWordle
import time


@given('Exists a user "{username}" with password "{password}"')
def step_create_user(context, username, password):
    User.objects.create_user(username=username, password=password)


@given('Exists a custom wordle "{word}" created by user "{username}"')
def step_create_wordle(context, word, username):
    user = User.objects.get(username=username)
    CustomWordle.objects.create(word=word.upper(), author=user)


@given('I login as user "{username}" with password "{password}"')
def step_login(context, username, password):
    context.browser.visit(context.get_url('home'))
    time.sleep(1)

    try:
        context.browser.fill('id_username', username)
        time.sleep(0.5)
        context.browser.fill('id_password', password)
        time.sleep(0.5)
    except:
        context.browser.fill('username', username)
        context.browser.fill('password', password)

    time.sleep(0.5)

    try:
        btn = context.browser.find_by_id('login-submit-btn')
        if btn:
            btn.first.click()
    except:
        context.browser.find_by_css('button[type="submit"]').first.click()


@given('I am not logged in')
def step_not_logged_in(context):
    try:
        logout_links = context.browser.find_by_link('Logout')
        if logout_links:
            logout_links.first.click()
    except:
        pass


@when('I fill in the word field with "{word}"')
def step_fill_word(context, word):
    context.browser.fill('word', word)


@when('I submit the form')
def step_submit_form(context):
    context.browser.find_by_css('[type="submit"]').first.click()


@then('I should see "{text}"')
def step_see_text(context, text):
    assert context.browser.is_text_present(text), f"Expected to see '{text}' in page"


@then('I should be on the custom wordle play page')
def step_on_play_page(context):
    assert 'play' in context.browser.url or 'custom_wordle' in context.browser.url


@then('I should be redirected to the login page')
def step_redirect_login(context):
    html_lower = context.browser.html.lower()
    assert 'login' in context.browser.url or 'username' in html_lower or 'password' in html_lower


@then('I should see an access denied message')
def step_access_denied(context):
    html = context.browser.html.lower()
    assert 'denied' in html or 'forbidden' in html or '403' in html or 'not authorized' in html


@then('I should see an error message about the word')
def step_error_word(context):
    html = context.browser.html.lower()
    assert 'required' in html or 'word' in html or 'this field' in html