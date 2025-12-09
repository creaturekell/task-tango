#! /usr/bin/env python3
import argparse 

def command_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Task Manager CLI."
    )

    return parser 

def main():
    args = command_parser().parse_args()
    # Just print somethign so I know it is working
    print("Parsed args:", args)


if __name__ == "__main__":
    main()
