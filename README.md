

# Design

Separated cli interface layer from business logic layer:

           +----------------------------+
           |         task_cli.py        |
           |  (parses commands, prints) |
           +--------------+-------------+
                          |
                          | uses
                          v
           +----------------------------+
           |      task_manager.py       |
           |   (adds, updates, lists)   |
           |        JSON storage        |
           +----------------------------+


This results in:

* Testing can be executed without the command line
* Testing Driven Development (TDD) can be executed more cleanly
* The CLI becomes a small wrapper that will be simple and readable
* Expanding functionality later for a gui, api, cronjob, etc is easier without changing task logic.
