# Copyright 2023 CherryOverBoard
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import tkinter as tk
import time
import subprocess


class Timer:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Timer")
        self.window.geometry("200x100")

        self.start_date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.start_time = time.time_ns()

        self.lbl_screen_total = tk.Label()
        self.lbl_screen_total.pack()
        self.lbl_screen_on = tk.Label()
        self.lbl_screen_on.pack()
        self.lbl_screen_off = tk.Label()
        self.lbl_screen_off.pack()

        self.screen_on = True
        self.screen_lock_start = time.time_ns()
        self.screen_off_time = 0

        self.update_timer()
        self.log_time()

        self.window.protocol("WM_DELETE_WINDOW", self.on_destroy)
        self.window.mainloop()

    def check_screen(self):
        processes = str(subprocess.check_output('TASKLIST'))
        if 'LogonUI.exe' in processes:
            if self.screen_on:
                self.screen_lock_start = time.time_ns()
            self.screen_on = False
        else:
            if not self.screen_on:
                self.screen_off_time += int((time.time_ns() - self.screen_lock_start) / 1000000000)
            self.screen_on = True

    def update_timer(self):
        self.check_screen()
        time_passed = int((time.time_ns() - self.start_time) / 1000000000)
        self.lbl_screen_total.configure(text="Total time: " + self.format_time(time_passed))
        self.lbl_screen_on.configure(text="Time on: " + self.format_time(time_passed - self.screen_off_time))
        self.lbl_screen_off.configure(text="Time off: " + self.format_time(self.screen_off_time))
        self.window.after(1000, self.update_timer)

    @staticmethod
    def format_time(ttf):
        secs = int(ttf % 60)
        mins = int(ttf / 60)
        hrs = int(mins / 60)
        mins = int(mins % 60)
        return "{:02d}:{:02d}:{:02d}".format(hrs, mins, secs)

    def on_destroy(self):
        self.check_screen()
        time_passed = int((time.time_ns() - self.start_time) / 1000000000)
        print("Total time: " + self.format_time(time_passed))
        print("Time on: " + self.format_time(time_passed - self.screen_off_time))
        print("Time off: " + self.format_time(self.screen_off_time))
        self.log_time()
        self.window.destroy()

    def log_time(self):
        time_passed = int((time.time_ns() - self.start_time) / 1000000000)
        f = open("timer_log_" + self.start_date + ".log", "a")
        f.write("\nTotal time: " + self.format_time(time_passed))
        f.write("\nTime on: " + self.format_time(time_passed - self.screen_off_time))
        f.write("\nTime off: " + self.format_time(self.screen_off_time))
        f.write("\n---------------------------------------------------")
        f.close()
        self.window.after(300000, self.log_time)


app = Timer()
