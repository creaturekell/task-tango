#! /usr/bin/env python3
import argparse 

def command_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Task Manager CLI.",
        usage="%(prog)s <command> [inputs/options]"   
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # add 
    p_add = subparsers.add_parser("add", help="Add a new task")
    p_add.add_argument("description", help="Description of the task")

    # update
    p_update = subparsers.add_parser("update", help="Update an existing task")
    p_update.add_argument("id", help="ID of the task to update")
    p_update.add_argument("description", help="New description")

    # delete
    p_delete = subparsers.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", help="ID of the task to delete")

    # mark-in-progress
    p_mip = subparsers.add_parser("mark-in-progress", help="Mark task as in progress")
    p_mip.add_argument("id", help="ID of the task")

    # mark-done
    p_md = subparsers.add_parser("mark-done", help="Mark task as done")
    p_md.add_argument("id", help="ID of the task")

    # list
    p_list = subparsers.add_parser("list", help="List tasks")
    p_list.add_argument("status", nargs="?", help="Optional status filter: todo, in-progress, done")

    return parser 

def main():
    args = command_parser().parse_args()
    print("Parsed args:", args)

if __name__ == "__main__":
    main()
