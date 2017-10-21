import pytest

from capybara.node.element import Element
from capybara.tests.helpers import isselenium


@pytest.mark.requires("js")
class TestEvaluateScriptAsync:
    def test_evaluates_the_given_script_and_returns_whatever_it_produces(self, session):
        session.visit("/with_js")
        assert session.evaluate_script_async("arguments[0](4)") == 4

    def test_supports_passing_elements_as_arguments_to_the_script(self, session):
        session.visit("/with_js")
        el = session.find("css", "#drag p")
        result = session.evaluate_script_async(
            """
            arguments[2]([arguments[0].innerText, arguments[1]]);
            """,
            el, "Doodle Funk")
        assert result == ["This is a draggable element.", "Doodle Funk"]

    def test_supports_returning_elements_after_a_timeout(self, session):
        session.visit("/with_js")
        session.find("css", "#change")  # ensure page has loaded and element is available
        el = session.evaluate_script_async(
            """
            var cb = arguments[0];
            setTimeout(function() {
              cb(document.getElementById('change'));
            }, 100);
            """)
        assert isinstance(el, Element)
        assert el == session.find("css", "#change")