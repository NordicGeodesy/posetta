from posetta.lib import plugins


@plugins.register
def test_func(file_path, cset):
    print(f"{file_path} written by {__name__}! ♣")
