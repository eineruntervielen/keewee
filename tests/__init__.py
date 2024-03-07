import root_user as RootUser

if __name__ == "__main__":

    RootUser.add_new_right("change name")
    RootUser.add_new_right("new right")
    RootUser.print_rights()

