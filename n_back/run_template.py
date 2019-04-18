import pandas as pd
import sys
from sys import platform

from taskpresenter import TaskPresenter

def check_platform():

    if platform == "linux" or platform == "linux2":
        return "ln"
    elif platform == "darwin":
        return "osx"
    elif platform == "win32":
        print("Ayyo, this is not supported for Windows at this time. "
              "Use Linix. Closing Applicaiton.")
        sys.exit()


def check_cmd_line_session_info(sub_id, session_num):
    """Checks for validity of command line arguements passed to the
    program.
    Args:
        sub_id(str): the 4-digit subject id.
    Returns:
        None.
    Raises: 'ValueError'"""

    if len(sub_id) == 4 and sub_id.isdigit():
        if len(session_num) == 1 and session_num.isdigit():
            return True
        raise ValueError(f"session_num: {session_num} invalid."
                         " (1 - 9 are valid sessions.)")
        sys.exit()
    raise ValueError(f"Sub_ID: {sub_id} invalid. (9999 > Four Digits < 1000)")
    sys.exit()


def get_task_template(sub_id, session_num, exper_tmp_file_name):
    """Finds task template for session for all of the subjects in mindfulness study
    particiular study.
    Args:
        sub_id(str): The subject """

    f_path = f"./templates/exper_temps/{exper_tmp_file_name}"

    table = pd.read_csv(f_path)
    table = table[(table["subject_id"] == int(sub_id))
                  & (table["session_num"] == int(session_num))]
    print(table)
    try:
        return(int(table["template"]))
    except:
        raise ValueError(f"Session {session_num} not found for Subject: "
                         f"{sub_id}")
        sys.exit()


def main(sub_id, session_num, marking, exper_tmp_file_name="n_back_demo.csv"):
    """Locates experiment and partcipant template file - feeds the list of
    tasks to be presented to a TaskPresenter() object.
    Args:
        sub_id(str): subject's participant ID number (four digits).
        session_num(str): subject's session number (one digit).
        marking(bool): whether or not the physiological data will be marked.
        exper_tmp_file_name(string): the name of the experiment template file.
    Returns:
        None
    """

    platform = check_platform()
    check_cmd_line_session_info(sub_id, session_num)
    temp_num = get_task_template(sub_id, session_num, exper_tmp_file_name)

    try:
        template_file = pd.read_csv(f"./templates/{exper_tmp_file_name[:-4]}"
                                    f"/{exper_tmp_file_name[:-4]}{temp_num}.csv")
    except FileNotFoundError as e:
        print(e)
        print(f"Either the file ./templates/mndful_template{temp_num}.csv"
              " could not be located, or you did not enter the promper template"
              " number.")
        sys.exit()

    task_list = template_file["task"].tolist()
    block_list = template_file["block"].tolist()

    if platform == "ln":
        fullscreen = True
    else:
        fullscreen = False


    tp = TaskPresenter(task_list=task_list, block_list=block_list,
                       templated=True, sub_id=sub_id,
                       session_num=session_num, marking=marking,
                       fullscr=fullscreen)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv) == 4:
            main(sys.argv[1], sys.argv[2], sys.argv[3])
        elif len(sys.argv) == 5:
            main(sys.argv[1], sys.argv[2], sys.argv[3],
                 exper_tmp_file_name=sys.argv[4])
        elif len(sys.argv) == 3:
            print("Marking Set to False.")
            print("No Template File given. "
                  "Using default: 'mindfulness.csv' template file.")
            main(sys.argv[1], sys.argv[2], marking="f")
        else:
            raise AttributeError("Invalid number of command line args. Provide "
                                 "both subject ID and session number.")
    else:
        print("No arguments given - please refer to documentation "
              "'Command Line Interface'")
        sys.exit()
