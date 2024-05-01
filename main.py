# This is a sample Python script.
import asyncio
import random

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import paramgaming
import uprock


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def param_farming():
    p = paramgaming.ParamGaming()
    # asyncio.run(p.batching_signup(concurrency=2, from_number=9191, to_number=11000))
    asyncio.run(p.batching_signup(concurrency=2, from_number=3399, to_number=5000))


def uprock_farming():
    u = uprock.Uprock()
    asyncio.run(u.signup_uprock(username='z-farmer3'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Farmer')
    param_farming()
    # uprock_farming()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
