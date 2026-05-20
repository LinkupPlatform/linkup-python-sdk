import linkup


def test_linkup_exports_have_prefix_stripped_aliases() -> None:
    prefix = "Linkup"
    for name in linkup.__all__:
        if not name.startswith(prefix):
            continue

        alias = name.removeprefix(prefix)

        assert alias in linkup.__all__
        assert getattr(linkup, alias) is getattr(linkup, name)
