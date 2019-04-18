from psychopy import visual, core, event
import pandas as pd
import os
# My imports
from taskpresenter import TaskPresenter


def run_trial(tp, trials, data, block, aud=False):
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
    block_dir_dict = {0: "clean",
                      1: "25",
                      2: "50",
                      3: "75",
                      }

    # Just for testing
    img_dir = f"./trial_sheets/stims/num_imgs/{block_dir_dict[block[0]]}/"

    if aud:
        from psychopy import sound
        s_dir = f"./trial_sheets/stims/num_aud/{block_dir_dict[block[0]]}/"
        # Otherwise I get a weird bug.
        sound_stim = sound.Sound(f"{s_dir}/0.wav")


    # If application is randomly selecting subset of trails,
    # rather than running through the trials directly.
    if tp.rand_select:
        trials = tp.select_trials(trials, block)
    if tp.marking:
        tp.send_mark("task_start")

    # Holds the values to check if value was n presentations back.
    stims = []

    tp.display_n(trials["n"].tolist()[0])

    # For each trial in the set of trials - if the trial matches the block
    # being run.
    for i, trial in enumerate(trials.iterrows()):
        if trial[1]["block"] in block:
            print(trial[1])

            # This will allow the 'prac' col to be removed from the trial sheets.
            if trial[1]["block"] == 0:
                prac = "Yes"
            else:
                prac = "No"

            n_back_num = trial[1]["n"]

            focus_time = int(trial[1]["focus_time"])
            tp.draw_focus(focus_time)

            # If the participant responds during focus time.
            if event.getKeys(keyList=["left", "right"]):
                if tp.marking:
                    tp.send_mark("too_early")
                data.append([i + 1, -1, "Incorrect", "None", "Too Early",
                            prac, trial[1]["block"]])
                if trial[1]["block"] == 0:
                    tp.show_performance(False, too_early=True)

            stim_text = trial[1]["display_item"]
            stims.append(stim_text)

            # while times.getTime() < trial[1]["disp_time"]:
            if tp.marking:
                tp.send_mark("trial_start")

            # Draw the stims - store stim in 'stims' list.
            if aud:
                stim = visual.TextStim(tp.win, text="Listen")
                sound_stim = sound.Sound(f'{s_dir}/{stim_text.upper()}.wav')
                stim.draw()
                tp.win.flip()
                sound_stim.play()
            else:
                # Show picture
                img_stim = f"{img_dir}{trial[1]['display_item']}.png"
                disp = visual.ImageStim(tp.win, image=img_stim)
                disp.draw()
                tp.win.flip()
                # core.wait(display_img_time)
                # stim = visual.TextStim(tp.win, text=stim_text)
                # stim.draw()
                # tp.win.flip()
            timer = core.Clock()

            # Participant can respond.
            while timer.getTime() < 3: # Should there be a variable display time?

                if len(stims) > n_back_num:
                    # Participant Input Right.
                    if event.getKeys(keyList="right"):
                        # True Positive Response.
                        if stims[i - n_back_num] == stim_text:
                            if tp.marking:
                                tp.send_mark("resp_cor")
                            data.append([i + 1, timer.getTime() * 1000, "Correct",
                                        "True Positive", "True Postive",
                                        prac, trial[1]["block"]])
                            if trial[1]["block"] == 0:
                                tp.show_performance(True)
                            break
                        # False Positive Response.
                        else:
                            if tp.marking:
                                tp.send_mark("resp_incor")
                            data.append([i + 1, timer.getTime() * 1000, "Incorrect",
                                        "True Negative", "False Positive",
                                        prac, trial[1]["block"]])
                            if trial[1]["block"] == 0:
                                tp.show_performance(False)
                            break
                    # Participant Input Left.
                    if event.getKeys(keyList="left"):
                        # True Negative Response.
                        if stims[i - n_back_num] != stim_text:
                            if tp.marking:
                                tp.send_mark("resp_cor")
                            data.append([i + 1, timer.getTime() * 1000, "Correct",
                                        "True Negative", "True Negative",
                                        prac, trial[1]["block"]])
                            if trial[1]["block"] == 0:
                                tp.show_performance(True)
                            break
                        # False Negative Response.
                        else:
                            if tp.marking:
                                tp.send_mark("resp_incor")
                            data.append([i + 1, timer.getTime() * 1000, "Incorrect",
                                        "True Positive", "False Negative",
                                        prac, trial[1]["block"]])
                            if trial[1]["block"] == 0:
                                tp.show_performance(False)
                            break
                # Start of trial there are no trials to compare.
                else:
                    if event.getKeys(keyList="left"):
                        if tp.marking:
                            tp.send_mark("resp_cor")
                        data.append([i + 1, timer.getTime() * 1000, "Correct",
                                    "True Negative", "True Negative",
                                    prac, trial[1]["block"]])
                        if trial[1]["block"] == 0:
                            tp.show_performance(True)
                        break
                    if event.getKeys(keyList="right"):
                        if tp.marking:
                            tp.send_mark("resp_incor")
                        data.append([i + 1, timer.getTime() * 1000, "Incorrect",
                                    "True Negative", "False Positive",
                                    prac, trial[1]["block"]])
                        if trial[1]["block"] == 0:
                            tp.show_performance(False)
                        break
            # Participant did not respond in time.
            if timer.getTime() > 3:
                data.append([i + 1, 1, "Incorrect", "None", "Lapse",
                            prac, trial[1]["block"]])
                if trial[1]["block"] == 0:
                    tp.show_performance(False)

            timer.reset()

    if tp.marking:
        tp.send_mark("task_end")
    return data

def main(tp=None, templated=False, **kwargs):
    """Runs the participant through the entire cognigive task.
        Args:
            None
        Returns:
            None
    """

    trials = pd.read_csv("./trial_sheets/n_back_trials.csv")
    data = []

    tp = TaskPresenter(task="anb")
    tp.show_instructions()
    data = run_trial(tp, trials, data, block=[0])
    tp.give_break(prompt_num="1")
    data = run_trial(tp, trials, data, block=[1, 2])
    tp.give_break(prompt_num="2")
    data = run_trial(tp, trials, data, block=[3, 4])
    tp.give_break(prompt_num="3")
    tp.write_to_csv(data)


if __name__ == "__main__":
    if not os.path.exists("./data/n_back/"):
        os.makedirs("./data/n_back/")
    main()
