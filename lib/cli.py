import argparse

parser = argparse.ArgumentParser(
    description="Check if repositories are up to date with remote."
)


parser.add_argument(
    "-f",
    "--file",
    type=str,
    default="repos.yaml",
    help="specify path to yaml file with repositories configuration",
)


parser.add_argument(
    "--delay", type=int, default=10, help="amount of seconds between checks"
)


args = parser.parse_args()
