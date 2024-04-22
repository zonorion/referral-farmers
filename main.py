# This is a sample Python script.
import asyncio
import random

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import paramgaming


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    p = paramgaming.ParamGaming()
    # init farmers
    farmer_list = []
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        p.batching_signup(random.choice(farmer_list), concurrency=3, from_number=240, to_number=2000)
    )

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
