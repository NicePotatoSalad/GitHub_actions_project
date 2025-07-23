import pytest
import os

from selenium.webdriver.chrome import options as ChromeOptions
from selenium.webdriver.edge import options as EdgeOptions
from selenium.webdriver.firefox import options as FirefoxOptions

from selenium import webdriver

def pytest_addoption(parser):
    parser.add_option(
        "--browser", action="store", default="chrome", help="browser to run tests on (chrome, firefox, edge)"
    )

def pytest_generate_tests(metafunc):
    if "driver" in metafunc.fixturenames:
        browser_from_cli = metafunc.config.getoption("--browser")

        # If a specific browser is provided, use only that one
        if browser_from_cli and browser_from_cli in ["chrome", "firefox", "edge"]:
            metafunc.parametrize("driver", [browser_from_cli], scope="function", indirect=True)
        else:
            # Fallback to running both if no valid browser is specified via CLI
            # Or you could raise an error, or set a default like "chrome"
            metafunc.parametrize("driver", ["chrome", "firefox"], scope="function", indirect=True)


@pytest.fixture(scope="function") # No params here, handled by pytest_generate_tests
def driver(request):
    browser = request.param # This now comes from pytest_generate_tests based on CLI option

    if browser == "chrome":
        options = ChromeOptions()
    elif browser == "firefox":
        options = FirefoxOptions()
    elif browser == "edge":
        options = EdgeOptions()
        # raise Exception("Edge browser support not fully implemented in fixture.") # Placeholder
    else:
        raise Exception(f"Unsupported browser: {browser}")

    if os.getenv('CI'):
        options.add_argument("--headless")

    options.add_argument("--start-maximized")

    if browser == "chrome":
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        driver = webdriver.Firefox(options=options)
    elif browser == "edge":
        driver = webdriver.Edge(options=options) # Actual Edge driver creation
        # raise Exception("Edge browser driver not created.") # Placeholder

    driver.get("https://qaplayground.dev/apps/popup/")
    yield driver
    driver.quit()
