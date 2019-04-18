from psychopy import visual, core, event
import pandas as pd
import os
# My imports
from taskpresenter import TaskPresenter

def run_trial(tp, rest_time):
    """Searches the stim list for the practice trials and runs the participant
    through them. Trials that are practice trials are coded as '1' in the
    'rt_trials.csv' file.
        Args:
            win: The Psychopy window in which the instuctions will be displayed
            trials(DataFrame): The set of all the trials for the experiment.
        Returns:
            data(list): A two dimensional list containing all the trial
            information
    """

    if tp.marking:
        tp.send_mark("rest_start")

    tp.draw_focus(focus_time=rest_time)

    if tp.marking:
        tp.send_mark("rest_end")


def main(tp=None, templated=False, **kwargs):
    """Runs the participant through the entire cognigive task.
        Args:
            None
        Returns:
            None
    """

    # Running the trial file in order.
    tp = TaskPresenter(task="cr")
    tp.show_instructions()
    rt_data = run_trial(tp, trials, rt_data, block=[0])
    tp.give_break(prompt_num="1")
    rt_data = run_trial(tp, trials, rt_data, block=[1])
    tp.give_break(prompt_num="2")
    rt_data = run_trial(tp, trials, rt_data, block=[3])
    tp.give_break(prompt_num="3")
    tp.write_to_csv(rt_data)


if __name__ == "__main__":
    if not os.path.exists("./data/reaction_time/"):
        os.makedirs("./data/reaction_time/")
    main()
