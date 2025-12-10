#! /usr/bin/env python3
import argparse
from task_manager import TaskManager

tm = TaskManager()

def command_add(args: argparse.Namespace) -> None:
    """ Add a new task """
    t = tm.add_task(args.description)
    print(f"Task added: {t['id']} - {t['description']} - {t['status']}")

def command_list(args: argparse.Namespace) -> None:
    """ List all tasks or filtered by status """
    status = args.status # optional status filter

    try:
        tasks = tm.list_tasks(status=status)
    except ValueError as e:
        print(f"Error: {e}")
        return

    if not tasks:
        if status:
            print(f"No tasks found with status: {status}.")
        else:
            print("No tasks found.")
        return

    print(f"\nListing {len(tasks)} tasks:")
    print("-" * 40)
    for t in tasks:
        print(f"{t['id']} - {t['description']} - {t['status']}")

    print("\n")


def command_update(args: argparse.Namespace) -> None:
    """ Update an existing task """
    try: 
        task_id = int(args.id)
    except ValueError:
        print(f"Error: Invalid task ID: {args.id}")
        return
    
    try:
        t = tm.update_task(task_id, args.description)
        print(f"Task updated: {t['id']} - {t['description']} - {t['status']}")
    except ValueError as e:
        print(f"Error: {e}")
        return

def command_delete(args: argparse.Namespace) -> None:
    """ Delete an existing task """
    try:
        task_id = int(args.id)
    except ValueError:
        print(f"Error: Invalid task ID: {args.id}")
        return
    
    try:
        tm.delete_task(task_id)
        print(f"Task deleted: {task_id}")
    except ValueError as e:
        print(f"Error: {e}")
        return

def command_mark_in_progress(args: argparse.Namespace) -> None:
    """ Mark a task as in progress """
    try:
        task_id = int(args.id)
    except ValueError:
        print(f"Error: Invalid task ID: {args.id}")
        return
    
    try:
        tm.mark_in_progress(task_id)
        print(f"Task marked as in progress: {task_id}")
    except ValueError as e:
        print(f"Error: {e}")
        return


def command_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Task Manager CLI.",
        usage="%(prog)s <command> [inputs/options]"   
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # add 
    p_add = subparsers.add_parser("add", help="Add a new task")
    p_add.add_argument("description", help="Description of the task")
    p_add.set_defaults(func=command_add)

    # list
    p_list = subparsers.add_parser("list", help="List tasks")
    p_list.add_argument("status", nargs="?", help="Optional status filter: todo, in-progress, done")
    p_list.set_defaults(func=command_list)

    # update
    p_update = subparsers.add_parser("update", help="Update an existing task")
    p_update.add_argument("id", help="ID of the task to update")
    p_update.add_argument("description", help="New description")
    p_update.set_defaults(func=command_update)

    # delete
    p_delete = subparsers.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", help="ID of the task to delete")
    p_delete.set_defaults(func=command_delete)

    # mark-in-progress
    p_mip = subparsers.add_parser("mark-in-progress", help="Mark task as in progress")
    p_mip.add_argument("id", help="ID of the task")
    p_mip.set_defaults(func=command_mark_in_progress)

    # mark-done
    p_md = subparsers.add_parser("mark-done", help="Mark task as done")
    p_md.add_argument("id", help="ID of the task")

    return parser 

def main():
    args = command_parser().parse_args()
    # subparsers attach a 'func' attribute 
    args.func(args)

if __name__ == "__main__":
    main()