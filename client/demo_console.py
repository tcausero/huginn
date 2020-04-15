#############################
#FOR THE DEMO FROM THE CONSOLE

from .interest import get_keyword, get_mid
from .client import Client

def demo_console():
    keyword = get_keyword()
    mid = get_mid(keyword)
    cl = Client(keyword, mid)
    return cl

if __name__ == "__main__":
    demo_console()
