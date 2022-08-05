import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


APP_ADRR = 'https://rioran.github.io/ru_vowels_filter/main.html'


@pytest.fixture(scope='module')
def module_driver():
    chrome_driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
    )
    yield chrome_driver
    chrome_driver.quit()


@pytest.fixture(scope='module')
def module_driver_with_devtools():
    options = webdriver.ChromeOptions()
    options.add_argument('auto-open-devtools-for-tabs')
    chrome_driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        chrome_options=options
    )
    yield chrome_driver
    chrome_driver.quit()


# not to reopen browser everytime, only tab is provided for each test
@pytest.fixture()
def new_tab(module_driver):
    initial_tab = module_driver.current_window_handle
    module_driver.switch_to.new_window('tab')
    module_driver.get(APP_ADRR)
    yield module_driver
    module_driver.close()
    module_driver.switch_to.window(initial_tab)


@pytest.fixture()
def new_tab_with_devtools(module_driver_with_devtools):
    initial_tab = module_driver_with_devtools.current_window_handle
    module_driver_with_devtools.switch_to.new_window('tab')
    module_driver_with_devtools.get(APP_ADRR)
    yield module_driver_with_devtools
    module_driver_with_devtools.close()
    module_driver_with_devtools.switch_to.window(initial_tab)
