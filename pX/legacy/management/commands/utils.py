def verbose_message(verbosity, messages):

    if messages.get(str(verbosity), None) is not None:
        print(messages[str(verbosity)])
