import pytest

from pages.manual_test_case_page import ManualTestCasePage


TEST_CASE_DESCRIPTION = "{test_case_description}"
URL = "{url}"
STEPS = "{steps}"
EXPECTED_RESULT = "{expected_result}"


pytestmark = [
    pytest.mark.guest,
    pytest.mark.skip(
        reason="Manual test case scaffold still contains placeholders and is not runnable yet."
    ),
]


@pytest.mark.parametrize(
    "test_case_description, url, steps, expected_result",
    [
        (
            TEST_CASE_DESCRIPTION,
            URL,
            STEPS,
            EXPECTED_RESULT,
        )
    ],
)
def test_manual_test_case_to_pom(
    page,
    test_case_description: str,
    url: str,
    steps: str,
    expected_result: str,
) -> None:
    manual_test_page = ManualTestCasePage(page)

    manual_test_page.open(url)
    manual_test_page.perform_test_steps()
    manual_test_page.verify_expected_result()
