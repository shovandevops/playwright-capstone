import pytest
import utils.json_utils as json_utils
from pages.login_page import LoginPage

data = json_utils.load_json_data('login_data.json')
valid_data = [d for d in data if d["username"] == "standard_user"]
locked_out_data = [d for d in data if d["username"] == "locked_out_user"]
invalid_data = [d for d in data if d["username"] == "invalid_user"]

@pytest.mark.parametrize('login_data', valid_data)
def test_valid_login(page, env, login_data):
    login_page = LoginPage(page)
    login_page.goto(env.saucedemo_url)
    assert login_page.url == env.saucedemo_url
    login_page.login(login_data['username'], login_data['password'])  
    assert login_page.url == env.saucedemo_url + 'inventory.html'

@pytest.mark.parametrize('login_data', invalid_data)
def test_invalid_login(page, env, login_data):
    login_page = LoginPage(page)
    login_page.goto(env.saucedemo_url)
    assert login_page.url == env.saucedemo_url
    login_page.login(login_data['username'], login_data['password']) 
    assert login_page.locator('.error-message-container').inner_text() == 'Epic sadface: Username and password do not match any user in this service'
    

@pytest.mark.parametrize('login_data', locked_out_data)
def test_locked_out_user_login(page, env, login_data):
    login_page = LoginPage(page)
    login_page.goto(env.saucedemo_url)
    assert login_page.url == env.saucedemo_url
    login_page.login(login_data['username'], login_data['password'])
    assert login_page.locator('.error-message-container').inner_text() == 'Epic sadface: Sorry, this user has been locked out.'
    