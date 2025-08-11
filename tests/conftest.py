import pytest
import os
import logging

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium import webdriver


BASE_URL = "https://qaplayground.dev/apps/popup/"
SELENIUM_GRID_URL = os.getenv("SELENIUM_GRID_URL", "http://localhost:4444") 
SUPPORTED_BROWSERS = ["chrome", "firefox", "edge"]
DEFAULT_TO_RUN_BROWSERS = ["chrome", "firefox"] # in case browser wasn't specified

logging.basicConfig(level=logging.INFO)

def pytest_addoption(parser):
    """
        Adds option --browser for pytest launch from CLI
    """
    parser.addoption(
        "--browser", action="store", default="chrome", help="browser to run tests on (chrome, firefox, edge)"
    )

def pytest_generate_tests(metafunc):
    """
        Parametrizes fixture "driver" dependendly on the --browser provided.
        By default launches on Chrome & Firefox
    """
    if "driver" in metafunc.fixturenames:
        browser_from_cli = metafunc.config.getoption("--browser")
        browsers_to_run = []

        # If a specific browser is provided, use only that one
        if browser_from_cli and browser_from_cli in SUPPORTED_BROWSERS:
            browsers_to_run.append(browser_from_cli)
        else:
            browsers_to_run = DEFAULT_TO_RUN_BROWSERS

    metafunc.parametrize("driver", browsers_to_run, scope="function", indirect=True)


@pytest.fixture(scope="function") # No params here, handled by pytest_generate_tests
def driver(request):
    """
        Fixture for a remote Selenium Grid launch
    """
    browser = request.param # This now comes from pytest_generate_tests based on CLI option
    logging.info(f"\n--- Running tests on: {browser.upper()} ---")

    if browser == "chrome":
        options = ChromeOptions()
    elif browser == "firefox":
        options = FirefoxOptions()
    elif browser == "edge":
        options = EdgeOptions()
    else:
        raise Exception(f"Unsupported browser: {browser}")

    options.add_argument("--start-maximized")

    if os.getenv('CI'):
        options.add_argument("--headless")

    try:
        # driver = webdriver.Remote(
        #     command_executor=f"{SELENIUM_GRID_URL}/wd/hub",
        #     options=options
        # )
        webdriver.Remote(command_executor="http://localhost:4444/wd/hub")

    except Exception as e:
        logging.error(f"Connection Error to Selenium Grid: {e}")
        raise


    driver.get(BASE_URL)
    yield driver
    driver.quit()
