from posetta.lib import plugins


@plugins.register
def test_func(file_path):
    print(f"{file_path} read by {__name__}! ♣".format(file_path))
