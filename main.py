import PySimpleGUI as sg
import datetime
from pygame import mixer

# global variable
font_clock = ('Calibri', 64)
font_time = ('Calibri', 20)
clock = ('hour','min','sec')
hour,minu,sec = 0,0,0
total_seconds = timer = start_time = paused_time = 0
runtime = None
paused = False

# Started
sg.theme('DarkAmber')
mixer.init()

def AlarmWindow():
    layout = [
        [sg.Text('00:00:00',key='output', size=(25,1),justification='center',font=font_clock,pad=(100,(100,45)))],
        [sg.Button('Pause',key='run-pause',size=(8,3),pad=(30,0)),sg.Button('Reset',size=(8,3),pad=(30,0)),sg.Button('Edit',size=(8,3),pad=(30,0)),sg.Exit(size=(8,3),pad=(30,0))]
    ]
    window = sg.Window('Alarm Clock', layout, size=(600,400), finalize=True)
    return window
def EditWindow():
    sec_layout = [[sg.Input(font=font_time,size=(2,1),enable_events=True,key='sec_input'),sg.Slider((0,60),disable_number_display=True,enable_events=True,key='sec_slider')]]
    min_layout = [[sg.Input(font=font_time,size=(2,1),enable_events=True,key='min_input'),sg.Slider((0,60),disable_number_display=True,enable_events=True,key='min_slider')]]
    hour_layout = [[sg.Input(font=font_time,size=(2,1),enable_events=True,key='hour_input'),sg.Slider((0,24),disable_number_display=True,enable_events=True,key='hour_slider')]]
    menu_layout = [[sg.Button('Start',size=(8,3))],[sg.Exit(size=(8,3))]]
    layout = [
        [sg.Text('00:00:00',key='output',size=(8,1),justification='c',font=font_clock,pad=(100,30))],
        [sg.Frame('Hour',hour_layout,pad=(40,0)),sg.Frame('Minute',min_layout,pad=(40,0)),sg.Frame('Second',sec_layout,pad=(40,0)),sg.Column(menu_layout)]
    ]   
    window = sg.Window('Edit Alarm',layout,size=(600,400), finalize=True)
        
    return window

edit_window, alarm_window = EditWindow(), AlarmWindow()
alarm_window.hide()

while True:
    window, event, values = sg.read_all_windows(timeout=runtime)
    if event == 'Exit' or event == sg.WINDOW_CLOSED:
        break

    if window == edit_window:
        for time in clock:
            limit = 0
            if time == 'hour':
                limit = 24
            else:
                limit = 60
            # if values is empty
            if values[f'{time}_input'] == '':
                values[f'{time}_input'] = '0'

            if values[f'{time}_input'][-1] not in ('1','2','3','4','5','6','7','8','9','0') or len(values[f'{time}_input']) > 2 or int(values[f'{time}_input']) > limit:
                values[f'{time}_input'] = values[f'{time}_input'][:-1]
                # if values is empty
                if values[f'{time}_input'] == '':
                    values[f'{time}_input'] = '0'
                window[f'{time}_input'].update(values[f'{time}_input'])

            if event == f'{time}_slider':
                window[f'{time}_input'].update(int(values[f'{time}_slider']))
                
            elif event == f'{time}_input':
                window[f'{time}_slider'].update(values[f'{time}_input'])
        
        if '_input' in event:
            hour = int(values['hour_input'])
            minu = int(values['min_input'])
            sec = int(values['sec_input'])
        elif '_slider' in event:
            hour = int(values['hour_slider'])
            minu = int(values['min_slider'])
            sec = int(values['sec_slider'])
    
        window['output'].update(f'{hour:02d}:{minu:02d}:{sec:02d}')

        if event == 'Start':
            window = alarm_window.un_hide()
            edit_window.hide()
            runtime = 1000
            total_seconds = hour * 3600 + minu * 60 + sec
            timer = datetime.timedelta(seconds=total_seconds)
            start_time = total_seconds
            alarm_window['output'].update(timer)

    else:
        timer = datetime.timedelta(seconds=total_seconds)

        if not paused and window != alarm_window:
            total_seconds -= 1
        
        if event == 'Reset':
            runtime = 1000
            paused = False
            paused_time = start_time
            total_seconds = start_time
            timer = datetime.timedelta(seconds=total_seconds)
            alarm_window['output'].update(timer)
        
        elif event == 'run-pause':
            paused = not paused
            if paused:
                paused_time = total_seconds
                runtime = None
            else:
                runtime = 1000
        
        elif event == 'Edit':
            runtime = None
            alarm_window.hide()
            edit_window.un_hide()
        
        if total_seconds < 0:
            runtime = None
            paused = not paused
            total_seconds = 0
            mixer.music.load('alarm_sound.wav')
            mixer.music.play()

        alarm_window['run-pause'].update('Run' if paused else 'Pause')
        alarm_window['output'].update(timer)
