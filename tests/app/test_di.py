from aioinject.validation import rules, validate

from app.di import create_container


def test_validate_container() -> None:
    container = create_container()
    validate.validate_or_err(
        container,
        rules.DEFAULT_RULES,
    )
