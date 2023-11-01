from prefect import task, flow


@task
def print_an_integer(x):
    print(f"The input number was {x}")


@flow
def my_flow():
    print_an_integer(1)
    print_an_integer(2)


if __name__ == "__main__":
    my_flow()