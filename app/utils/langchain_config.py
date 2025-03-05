from langchain.globals import set_verbose, get_verbose

def configure_langchain(verbose: bool = False):
    set_verbose(verbose)
    return get_verbose()
