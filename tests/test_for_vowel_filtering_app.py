import pytest
import pyperclip
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By


# locators for used elements
LOCATOR_INPUT_TEXT_FIELD = (By.NAME, 'text_input')
LOCATOR_ONLY_VOWELS_BUTTON = (By.XPATH, '//button[contains(text(), "Оставить только гласные")]')
LOCATOR_VOWELS_AND_SPACES_BUTTON = (By.XPATH, '//button[contains(text(), "Ну и ещё пробелы")]')
LOCATOR_VOWELS_AND_SIGNS_BUTTON = (By.XPATH, '//button[contains(text(), "Оставить ещё и .,-!?")]')
LOCATOR_SELECT_RESULT_BUTTON = (By.XPATH, '//button[contains(text(), "Выделить результат")]')
LOCATOR_RESULT_OUTPUT = (By.ID, 'text_output')

# test data
CUSTOM_INPUT = '№C;u%s@t*o(m)!Проверка_ ?для, -ввода.+=юБ<э>АОЕИЮЭЯУ'
FILTERED_ONLY_VOWELS_FOR_CUSTOM_INPUT = 'оеаяоаюэаоеиюэяу'
FILTERED_VOWELS_AND_SPACES_FOR_CUSTOM_INPUT = 'оеа я оаюэаоеиюэяу'
FILTERED_VOWELS_AND_SIGNS_FOR_CUSTOM_INPUT = '!оеа ?я, -оа.юэаоеиюэяу'
FILTERED_ONLY_VOWELS_FOR_DEFAULT_INPUT = 'еяиееауоои\nияеоауаыееи\nоеоиееуиеи\nаиоыиоыуееи\n\nауияоеиаа'
FILTERED_VOWELS_AND_SPACES_FOR_DEFAULT_INPUT = 'еяи ее ауо ои\nияе оа уаые еи\nо еои е еу и е и\nаи оы и оы уееи\n\nауи яоеи аа'
FILTERED_VOWELS_AND_SIGNS_FOR_DEFAULT_INPUT = 'еяи ее ауо ои,\nияе оа уаые еи.\nо еои е еу и е и\nаи оы и оы уееи.\n\nауи яоеи аа'

buttons = (LOCATOR_ONLY_VOWELS_BUTTON,
           LOCATOR_VOWELS_AND_SPACES_BUTTON,
           LOCATOR_VOWELS_AND_SIGNS_BUTTON,
           LOCATOR_SELECT_RESULT_BUTTON,
           )


# 3 cases for each filter button: default value, empty input and custom input
@pytest.mark.parametrize('button,custom_input,expected_output', (
    (LOCATOR_ONLY_VOWELS_BUTTON, None, FILTERED_ONLY_VOWELS_FOR_DEFAULT_INPUT),
    (LOCATOR_ONLY_VOWELS_BUTTON, '', ''),
    (LOCATOR_ONLY_VOWELS_BUTTON, CUSTOM_INPUT, FILTERED_ONLY_VOWELS_FOR_CUSTOM_INPUT),
    (LOCATOR_VOWELS_AND_SPACES_BUTTON, None, FILTERED_VOWELS_AND_SPACES_FOR_DEFAULT_INPUT),
    (LOCATOR_VOWELS_AND_SPACES_BUTTON, '', ''),
    (LOCATOR_VOWELS_AND_SPACES_BUTTON, CUSTOM_INPUT, FILTERED_VOWELS_AND_SPACES_FOR_CUSTOM_INPUT),
    (LOCATOR_VOWELS_AND_SIGNS_BUTTON, None, FILTERED_VOWELS_AND_SIGNS_FOR_DEFAULT_INPUT),
    (LOCATOR_VOWELS_AND_SIGNS_BUTTON, '', ''),
    (LOCATOR_VOWELS_AND_SIGNS_BUTTON, CUSTOM_INPUT, FILTERED_VOWELS_AND_SIGNS_FOR_CUSTOM_INPUT),
))
def test_filter_button(new_tab, button, custom_input, expected_output):
    new_tab.maximize_window()

    # set text for input field only if it needed (not cases with default value)
    if custom_input is not None:
        input_field = new_tab.find_element(*LOCATOR_INPUT_TEXT_FIELD)
        input_field.clear()
        input_field.send_keys(custom_input)
    new_tab.find_element(*button).click()
    assert new_tab.find_element(*LOCATOR_RESULT_OUTPUT).text == expected_output


# idea is to copy selected text with CTRL+C and compare it with expected text
def test_selection_button(new_tab):
    expected_text = new_tab.find_element(*LOCATOR_RESULT_OUTPUT).text
    check_for_not_selected_text = 'no copy'

    pyperclip.copy(check_for_not_selected_text)
    ActionChains(new_tab).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
    # if button for selection isn't clicked, no text will be copied
    assert pyperclip.paste() == check_for_not_selected_text

    new_tab.find_element(*LOCATOR_SELECT_RESULT_BUTTON).click()
    # ActionChains(new_tab).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
    ActionChains(new_tab).key_down(Keys.COMMAND).send_keys('c').key_up(Keys.COMMAND).perform()
    # if button for selection is clicked, text will be copied
    assert pyperclip.paste() == expected_text


@pytest.mark.parametrize('elements,layout_type', (
    (buttons, 'vertical'),
    (buttons, 'horizontal'),
))
# opened devtools panel is a way to make window size small enough to get vertical row of buttons
# because chrome's minimum width is 500 on Win
def test_elements_are_layout_in_row(new_tab_with_devtools, elements, layout_type):
    if layout_type == 'horizontal':
        new_tab_with_devtools.maximize_window()
    elif layout_type == 'vertical':
        new_tab_with_devtools.set_window_size(600, 900)
    else:
        raise ValueError('Only "horizontal" and "vertical" types are accepted.')

    buttons_location = []
    for btn in elements:
        buttons_location.append(new_tab_with_devtools.find_element(*btn).location)

    if layout_type == 'horizontal':
        # for buttons located in a row horizontally y coordinate should be equal
        assert all(coord['y'] == buttons_location[0]['y'] for coord in buttons_location) is True
    elif layout_type == 'vertical':
        # for buttons located in a row vertically x coordinate should be equal
        assert all(coord['x'] == buttons_location[0]['x'] for coord in buttons_location) is True
