# region `pytest` hooks
def pytest_addoption(parser):
    parser.addoption("--slow", action="store_true", dest="slow", default=False,
                     help="Specify this flag to run slow tests.")
    parser.addoption("--holistic", action="store_true", dest="holistic", default=False,
                     help="Specify this flag to run holistic tests.")
    parser.addoption("--all", action="store_true", dest="all", default=False,
                     help="Specify this flag to run all tests, "
                          "including the one that is either marked as `slow` or `holistic`.")


def pytest_configure(config):
    if not config.option.all:
        marks = []

        if not config.option.slow:
            marks.append("not slow")
        if not config.option.holistic:
            marks.append("not holistic")

        setattr(config.option, "markexpr", (getattr(config.option, "markexpr", "") + " and ".join(marks)).strip())
# endregion
