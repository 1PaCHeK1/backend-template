import pkgutil

import pytest
from pytest_archon import archrule

import app.adapters
import app.core.di._modules.domain
import app.core.domain


def test_core_cant_import_adapters() -> None:
    (
        archrule("core_imports")
        .match("app.core.**")
        .should_not_import("app.adapters.*")
        .check("app.core")
    )


def test_adapters_dont_import_repositories() -> None:
    exclude_adapters: list[str] = ["cli"]
    rule = archrule("adapters_dont_import_services").match("app.adapters.*")

    for module in exclude_adapters:
        rule.exclude(f"app.adapters.{module}.*")

    (
        rule.should_not_import(
            "app.core.*.repositories",
            "app.core.*.repository",
        ).check("app.adapters")
    )


def test_adapters_dont_import_each_other() -> None:
    adapter_modules = [
        module.name for module in pkgutil.iter_modules(app.adapters.__path__)
    ]

    exclude: dict[str, list[str]] = {}
    for adapter in adapter_modules:
        rule = (
            archrule(f"adapter_{adapter}")
            .match("app.adapters.*")
            .should_not_import("app.adapters.*")
            .may_import(f"app.adapters.{adapter}.*")
        )
        for may_import in exclude.get(adapter, []):
            rule = rule.may_import(f"app.adapters.{may_import}")

        rule.check(f"app.adapters.{adapter}")


def test_connectors_dont_import_other() -> None:
    (
        archrule("connectors")
        .match("app.connectors.*")
        .should_not_import(
            "app.adapters.*",
            "app.core.*",
            "app.storages.*",
        )
        .check("app.connectors")
    )


def test_only_imports_lib() -> None:
    (
        archrule("lib")
        .match("lib.*")
        .should_not_import("app.*", "alembic.*")
        .check("lib")
    )


def test_forbidden_libraries() -> None:
    (
        archrule("forbidden-libraries")
        .match("app.adapters.*")
        .should_not_import("sqlalchemy.*")
        .check("app.adapters", only_direct_imports=True)
    )


def test_dependency_injection_imports() -> None:
    target = app.core.di._modules.domain  # noqa: SLF001
    rule = archrule("incorrect-di-domain-import")

    for module in pkgutil.walk_packages(target.__path__, f"{target.__name__}."):
        relative_name = module.name.removeprefix(f"{target.__name__}.")
        (
            rule.match(module.name)
            .should_not_import("app.core.domain.*")
            .may_import(f"app.core.domain.{relative_name}.*")
            .check(target.__name__, only_direct_imports=True)
        )


@pytest.mark.xfail(strict=True, reason="Remove mark later")
def test_domain_constraints() -> None:
    target = app.core.domain
    rule = archrule("domain-constraints")
    shared_domains = [
        "app.core.domain.shared.*",
    ]
    for module in pkgutil.iter_modules(target.__path__, f"{target.__name__}."):
        (
            rule.match(f"{module.name}.*")
            .should_not_import("app.core.domain.*")
            .may_import(f"{module.name}.*", *shared_domains)
            .check("app.core.domain", only_direct_imports=True)
        )
