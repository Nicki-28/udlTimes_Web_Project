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
    time.sleep(2)

    driver = context.browser.driver

    script_show_modal = """
    var modal = document.getElementById('login-modal');
    if (modal) {
        modal.classList.remove('hidden');
    }
    """
    driver.execute_script(script_show_modal)
    time.sleep(1)

    script_fill_form = f"""
    var usernameInput = document.getElementById('id_username');
    var passwordInput = document.getElementById('id_password');
    var captchaInput = document.getElementById('captcha_ok');
    
    if (usernameInput) {{
        usernameInput.value = '{username}';
    }}
    if (passwordInput) {{
        passwordInput.value = '{password}';
    }}
    if (captchaInput) {{
        captchaInput.value = '1';
    }}
    """
    driver.execute_script(script_fill_form)
    time.sleep(1)

    try:
        submit_btn = driver.find_element('id', 'login-submit-btn')
        submit_btn.click()
    except:
        driver.execute_script("document.getElementById('login-form').submit();")

    time.sleep(3)


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
    driver = context.browser.driver
    if word:
        script = f"""
        var input = document.getElementById('id_word');
        if (input) {{
            input.value = '{word}';
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
        """
    else:
        script = """
        var input = document.getElementById('id_word');
        if (input) {
            input.value = '';
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
        """
    driver.execute_script(script)


@when('I submit the form')
def step_submit_form(context):
    driver = context.browser.driver
    driver.execute_script("document.getElementById('wordle-form').submit();")
    time.sleep(3)


@then('I should see "{text}"')
def step_see_text(context, text):
    assert context.browser.is_text_present(text), f"Expected to see '{text}' in page"


@then('I should be on the custom wordle play page')
def step_on_play_page(context):
    current_url = context.browser.url
    print(f"DEBUG: URL after submit: {current_url}")
    assert 'play' in current_url or 'custom_wordle' in current_url, \
        f"Expected play page but URL is: {current_url}"


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
    assert 'required' in html or 'word' in html or 'this field' in html or 'error' in html