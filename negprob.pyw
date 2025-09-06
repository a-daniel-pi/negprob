#!/usr/bin/python3

# This file renders the UI

import tkinter
import tkinter.ttk as ttk
from decimal import Decimal as D

from sample import sample, sample3000, LEFT, RIGHT, SAME

init = False # Need this so things aren't called before everything is done initialising

class Window:
    '''Holds the entire window'''
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Negative Probability Calculator")

        self.inputframe = ProbInputFrame(self)
        self.outputframe = ProbOutputFrame(self.inputframe, self)
        self.sampleframe = SampleFrame(self.outputframe, self)
        self.sample3000 = Sample3000Frame(self)

class ProbInputFrame:
    '''Holds all the probability inputs'''
    def __init__(self, window):
        self.window = window
        self.frame = ttk.Frame(window.root, borderwidth=2, relief='sunken', padding=5)
        self.frame.grid(column=0, row=1, sticky='nsew', padx=4, pady=4)

        self.prob00 = ProbInput(self.frame, '00', D('-0.5'), self)
        self.prob00.grid(column=0, row=0)

        self.prob01 = ProbInput(self.frame, '01', D('0.5'), self)
        self.prob01.grid(column=0, row=1)

        self.prob10 = ProbInput(self.frame, '10', D('0.5'), self)
        self.prob10.grid(column=0, row=2)

        self.prob11 = ProbInput(self.frame, '11', D('0.5'), self)
        self.prob11.grid(column=0, row=3)

        style = ttk.Style()
        style.configure('Red.Label', foreground='red')

        self.error_text = ttk.Label(self.frame, text='', style='Red.Label')
        self.error_text.grid(column=0, row=4, sticky='w', padx=15)

    def verify_all(self):
        '''Check that the probabilities are valid:
1. They add up to 1
2. If there is an invalid probability (<0 or >1), disable that button'''
        valid = True
        # Check that they are all numbers
        if not self.prob00.verified or not self.prob01.verified \
            or not self.prob10.verified or not self.prob11.verified:
            self.error_text.configure(text='')
            self.window.sampleframe.disable_buttons()
            valid = False
        # Check that they add to 1
        elif (self.prob00.value+
              self.prob01.value+
              self.prob10.value+
              self.prob11.value) != 1:
            self.error_text.configure(text="Probabilities must add to 1")
            valid = False
            self.window.sampleframe.disable_buttons()
        # If they do, enable all the buttons
        else:
            self.window.sampleframe.sample_left.state(['!disabled'])
            self.window.sampleframe.sample_same.state(['!disabled'])
            self.window.sampleframe.sample_right.state(['!disabled'])
            self.window.sample3000.sample3000_button.state(['!disabled'])
            self.error_text.configure(text='')
        self.window.outputframe.setprob(valid)

class ProbOutputFrame:
    '''Holds all of the probability outputs (calculations)'''
    def __init__(self, inputframe, window):
        self.inputframe = inputframe
        self.window = window
        self.frame = ttk.Frame(window.root)
        self.frame.grid(column=0, row=2, padx=10)

        self.left_text = ttk.Label(self.frame, text="Left Bit Probabilities")
        self.left_text.grid(column=0, row=0)
        self.left0 = ProbOutput(self.frame, 'Left Bit is 0 (00 or 01):')
        self.left0.grid(column=0, row=1)
        self.left1 = ProbOutput(self.frame, 'Left Bit is 1 (10 or 11):')
        self.left1.grid(column=0, row=2)

        self.same_text = ttk.Label(self.frame, text="Equivilance Probabilities")
        self.same_text.grid(column=2, row=0, columnspan=2)
        self.same = ProbOutput(self.frame, 'Equivilant (00 or 11):')
        self.same.grid(column=2, row=1)
        self.diff = ProbOutput(self.frame, 'Different (01 or 10):')
        self.diff.grid(column=2, row=2)

        self.right_text = ttk.Label(self.frame, text="Right Bit Probabilities")
        self.right_text.grid(column=4, row=0, columnspan=2)
        self.right0 = ProbOutput(self.frame, 'Right Bit is 0 (00 or 10):')
        self.right0.grid(column=4, row=1)
        self.right1 = ProbOutput(self.frame, 'Right Bit is 1 (01 or 11):')
        self.right1.grid(column=4, row=2)

    def setprob(self, valid):
        '''Sets the probability labels'''
        sampleframe = self.window.sampleframe
        self.left0.prob.configure(text=str(self.inputframe.prob00.value + self.inputframe.prob01.value))
        self.left1.prob.configure(text=str(self.inputframe.prob10.value + self.inputframe.prob11.value))
        if (0 <= self.inputframe.prob00.value + self.inputframe.prob01.value <= 1) and valid:
            sampleframe.sample_left.state(['!disabled'])
        else:
            sampleframe.sample_left.state(['disabled'])
    
        self.same.prob.configure(text=str(self.inputframe.prob00.value + self.inputframe.prob11.value))
        self.diff.prob.configure(text=str(self.inputframe.prob01.value + self.inputframe.prob10.value))
        if (0 <= self.inputframe.prob00.value + self.inputframe.prob11.value <= 1) and valid:
            sampleframe.sample_same.state(['!disabled'])
        else:
            sampleframe.sample_same.state(['disabled'])
    
        self.right0.prob.configure(text=str(self.inputframe.prob00.value + self.inputframe.prob10.value))
        self.right1.prob.configure(text=str(self.inputframe.prob01.value + self.inputframe.prob11.value))
        if (0 <= self.inputframe.prob00.value + self.inputframe.prob10.value <= 1) and valid:
            sampleframe.sample_right.state(['!disabled'])
        else:
            sampleframe.sample_right.state(['disabled'])


class SampleFrame:
    '''Holds the single-sample UI'''
    def __init__(self, outputframe, window):
        self.window = window
        self.sample_result = ttk.Label(window.root, text='Result: Left Bit is 1 (10 or 11)')
        self.sample_result.grid(column=0, row=5)

        prob_output = outputframe.frame

        self.sample_text = ttk.Label(prob_output, text="Each sample works on a new pair of bits"
                        , justify='center')
        self.sample_text.grid(column=0, row=3, columnspan=5)

        self.sample_left = ttk.Button(prob_output, text='Sample Left Bit of Next Pair',
                         command=self.press_sample_button(LEFT, 'Left Bit is 1 (10 or 11)',
                                                     'Left Bit is 0 (00 or 01)'))
        self.sample_left.grid(column=0, row=4)

        self.sample_same = ttk.Button(prob_output, text='Sample Equivilance of Next Pair',
                         command=self.press_sample_button(SAME, 'Equivilant (00 or 11)',
                                                     'Different (01 or 10)'))
        self.sample_same.grid(column=2, row=4)

        self.sample_right = ttk.Button(prob_output, text='Sample Right Bit of Next Pair',
                          command=self.press_sample_button(RIGHT, 'Right Bit is 1 (01 or 11)',
                                                      'Right Bit is 0 (00 or 01)'))
        self.sample_right.grid(column=4, row=4)

    def disable_buttons(self):
        '''Disables all the sampling buttons'''
        self.sample_left.state(['disabled'])
        self.sample_same.state(['disabled'])
        self.sample_right.state(['disabled'])
        self.window.sample3000.sample3000_button.state(['disabled'])

    def press_sample_button(self, form, iftrue, iffalse):
        probs = self.window.inputframe
        '''Returns a function that sets the result of the sampling operation'''
        def make_sample():
            result = sample(probs.prob00.value, probs.prob01.value, probs.prob10.value, probs.prob11.value, form)
            self.sample_result.configure(text=f'Result: {iftrue if result else iffalse}')
        return make_sample

class Sample3000Frame:
    '''Holds the sample 3000 times UI'''
    def __init__(self, window):
        self.window = window
        self.frame = ttk.Frame(window.root, borderwidth=2, relief='groove')
        self.frame.grid(column=0, row=10, pady=5)

        self.sample3000_button = ttk.Button(self.frame, text='Sample 3000 Pairs', command=self.sample1000each)
        self.sample3000_button.grid(column=0, row=0)

        self.sample1000_left = ttk.Label(self.frame, text='Left Bit: ')
        self.sample1000_left.grid(column=0, row=1)

        self.sample1000_same = ttk.Label(self.frame, text='')
        self.sample1000_same.grid(column=0, row=2)

        self.sample1000_right = ttk.Label(self.frame, text='')
        self.sample1000_right.grid(column=0, row=3)

    def sample1000each(self):
        '''Performs 1000 samples of each question to ask the next pair of bits'''
        probs = self.window.inputframe

        lsample, rsample, ssample = sample3000(probs.prob00.value, probs.prob01.value, 
                                               probs.prob10.value, probs.prob11.value)

        if (0 <= probs.prob00.value + probs.prob01.value <= 1):
            self.sample1000_left.configure(text=f'Left Bit 0: {lsample}/1000, Left Bit 1: {1000-lsample}/1000')
        else:
            self.sample1000_left.configure(text=f'Left Bit is 0: Invalid, Left Bit is 1: Invalid')
        if (0 <= probs.prob00.value + probs.prob11.value <= 1):
            self.sample1000_same.configure(text=f'Equivilant: {ssample}/1000, Different: {1000-ssample}/1000')
        else:
            self.sample1000_same.configure(text=f'Equivilant: Invalid, Different: Invalid')
        if (0 <= probs.prob00.value + probs.prob10.value <= 1):
            self.sample1000_right.configure(text=f'Right Bit 0: {rsample}/1000, Right Bit 1: {1000-rsample}/1000')
        else:
            self.sample1000_right.configure(text=f'Right Bit 0: Invalid, Right Bit 1: Invalid')

class ProbInput:
    '''Represents a probability input field'''
    def __init__(self, parent, label, origvalue, inputframe):
        self.inputframe = inputframe
        self.frame = ttk.Frame(parent, width='450i')
        self.text = ttk.Label(self.frame, text=label)
        self.text.grid(column=0, row=0)
        self.verify_wrapper = (self.frame.register(self.verify_float), '%P')

        self.error_text = ttk.Label(self.frame, text='', width=24, style='Red.Label')
        self.error_text.grid(column=2, row=0, columnspan=2, padx=5)
        
        self.prob = tkinter.StringVar(value=str(origvalue))
        self.field = ttk.Entry(self.frame, textvariable=self.prob,
                                   validate='key', validatecommand=self.verify_wrapper,)
        self.field.grid(column=1, row=0)
        self.verified = True
        self.value = origvalue

    def verify_float(self, val):
        '''Checks whether the value is a number.'''
        if not init:
            return True
        try:
            self.value = D(val)
            self.error_text.configure(text='')
            self.verified = True
        except:
            self.error_text.configure(text="Value must be a number")
            self.verified = False
            self.inputframe.window.sampleframe.disable_buttons()
            return True
        self.inputframe.verify_all()
        return True

    def grid(self, *, column, row):
        '''Place it on the grid'''
        self.frame.grid(column=column, row=row, sticky='W')


class ProbOutput:
    '''Represents an label for the probability'''
    def __init__(self, parent, label):
        self.frame = ttk.Frame(parent, padding=2, borderwidth=1, relief='ridge')
        self.text = ttk.Label(self.frame, text=label)
        self.text.grid(column=0, row=0)
        self.prob = ttk.Label(self.frame, text='0')
        self.prob.grid(column=1, row=0)
    def grid(self, *, column, row):
        self.frame.grid(column=column, row=row, sticky='nsew')

def main():
    global init
    window = Window()
    window.outputframe.setprob(True)
    window.sample3000.sample1000each()
    init = True

    window.root.mainloop()

if __name__ == '__main__':
    main()
