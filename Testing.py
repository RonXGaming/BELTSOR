from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import bluetooth
from threading import Thread
from kivy.metrics import sp
from kivy.metrics import dp

from kivy.core.window import Window
Window.clearcolor = (0.9, 0.9, 0.9, 1)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=(0, 50))

        # Add spacer widget to center the buttons vertically
        layout.add_widget(Label())

        layout_buttons = BoxLayout(orientation='vertical', size_hint_y=None, height=600, spacing=20)
        
        open_calculator_button = Button(text='Open One Rep Max Calculator', size_hint=(None, None), size=(300, 100), background_color=(0.2, 0.6, 0.8, 1), pos_hint={'center_x': 0.5})
        open_calculator_button.bind(on_press=self.open_calculator)
        layout_buttons.add_widget(open_calculator_button)

        connect_to_beltsor_button = Button(text='Connect to BELTSOR', size_hint=(None, None), size=(300, 100), background_color=(0.8, 0.6, 0.2, 1), pos_hint={'center_x': 0.5})
        connect_to_beltsor_button.bind(on_press=self.connect_to_beltsor)
        layout_buttons.add_widget(connect_to_beltsor_button)

        close_button = Button(text='Close Application', size_hint=(None, None), size=(300, 100), background_color=(0.8, 0.2, 0.2, 1), pos_hint={'center_x': 0.5})
        close_button.bind(on_press=App.get_running_app().stop)
        layout_buttons.add_widget(close_button)
        
        layout.add_widget(layout_buttons)
        
        layout.add_widget(Label())

        self.add_widget(layout)

    def open_calculator(self, instance):
        self.manager.current = 'calculator'

    def connect_to_beltsor(self, instance):
        status_message = 'Connecting to BELTSOR...'
        self.manager.get_screen('connection_status').update_status(status_message)
        self.manager.current = 'connection_status'

        Thread(target=self.check_beltsor_connection).start()

    def check_beltsor_connection(self):
        mac_address = '00:21:13:00:46:62'
        nearby_devices = bluetooth.discover_devices()
        connected = any(mac_address == addr for addr in nearby_devices)

        status_message = 'BELTSOR is connected, please read instructions before using BELTSOR' if connected else 'Please connect to BELTSOR using Bluetooth'
        Clock.schedule_once(lambda dt:  self.manager.get_screen('connection_status').update_status(status_message))
    
class ConnectionStatusScreen(Screen):
    def __init__(self, **kwargs):
        super(ConnectionStatusScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        self.status_label = Label(text='', color=(0.2, 0.2, 0.2, 1), halign='center', font_size=sp(14))  # Dark text
        self.status_label.bind(size=self.status_label.setter('text_size'))
        layout.add_widget(self.status_label)

        self.instructions_label = Label(text='Instructions:\n1. Please make sure you are wearing BELTSOR properly\n2. Please do the conventional deadlift when wearing BELTSOR.\n3. Please note that when BELTSOR alarms you, \n it has detected poor lower back posture.', color=(0.2, 0.2, 0.2, 1), halign='center', font_size=sp(14))  # Dark text
        self.instructions_label.bind(size=self.instructions_label.setter('text_size'))
        layout.add_widget(self.instructions_label)
        self.instructions_label.opacity = 0 

        self.warning_label = Label(text='WARNING: If you still continue to do your \n deadlift exercise even when BELTSOR has detected poor \n lower back posture, you are at risk of injuring \n your lower back.This can result in strains, \n sprains, or more serious injuries. It is important \n to maintain a neutral spine throughout the \n lift to prevent injury and maximize the effectiveness \n of the exercise.', color=(0.2, 0.2, 0.2, 1), halign='center', font_size=sp(14))  # Dark text
        self.warning_label.bind(size=self.warning_label.setter('text_size'))
        layout.add_widget(self.warning_label)
        self.warning_label.opacity = 0 

        go_back_button = Button(text='Go Back', size_hint_y=None, height=dp(50), background_color=(0.2, 0.6, 0.8, 1), font_size=sp(14))  # Blue button
        go_back_button.bind(on_press=self.go_back)
        layout.add_widget(go_back_button)

        self.add_widget(layout)

    def update_status(self, status_message):
        self.status_label.text = status_message

        if status_message == 'BELTSOR is connected, please read instructions before using BELTSOR':
            self.instructions_label.opacity = 1
            self.warning_label.opacity = 1 
        else:
            self.instructions_label.opacity = 0
            self.warning_label.opacity = 0 

    def go_back(self, instance):
        self.manager.current = 'main'

class OneRepMaxCalculator(Screen):
    def __init__(self, **kwargs):
        super(OneRepMaxCalculator, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        weight_input_layout = BoxLayout(orientation='horizontal')
        weight_label = Label(text='Enter weight lifted:', color=(0.2, 0.2, 0.2, 1))  # Dark text
        weight_input_layout.add_widget(weight_label)
        self.weight_input = TextInput()
        weight_input_layout.add_widget(self.weight_input)
        self.layout.add_widget(weight_input_layout)

        reps_input_layout = BoxLayout(orientation='horizontal')
        reps_label = Label(text='Enter repetitions:', color=(0.2, 0.2, 0.2, 1))  # Dark text
        reps_input_layout.add_widget(reps_label)
        self.reps_input = TextInput()
        reps_input_layout.add_widget(self.reps_input)
        self.layout.add_widget(reps_input_layout)

        unit_input_layout = BoxLayout(orientation='horizontal')
        unit_label = Label(text='Select unit:', color=(0.2, 0.2, 0.2, 1))  # Dark text
        unit_input_layout.add_widget(unit_label)

        self.unit_dropdown = DropDown()

        for unit in ['kg', 'lbs']:
            button = Button(text=unit, size_hint_y=None, height=40, background_color=(0.8, 0.6, 0.2, 1))  # Yellow button
            button.bind(on_release=lambda btn: self.unit_dropdown.select(btn.text))
            self.unit_dropdown.add_widget(button)

        self.unit_button = Button(text='Select unit', background_color=(0.8, 0.6, 0.2, 1))  # Yellow button
        self.unit_button.bind(on_release=self.unit_dropdown.open)
        self.unit_dropdown.bind(on_select=lambda instance, x: setattr(self.unit_button, 'text', x))
        unit_input_layout.add_widget(self.unit_button)
        self.layout.add_widget(unit_input_layout)

        calculate_button = Button(text='Calculate 1RM', background_color=(0.2, 0.6, 0.8, 1))  # Blue button
        calculate_button.bind(on_press=self.calculate_max)
        self.layout.add_widget(calculate_button)

        self.result_label = Label(text='', color=(0.2, 0.2, 0.2, 1))  # Dark text
        self.layout.add_widget(self.result_label)

        go_back_button = Button(text='Go Back', size_hint_y=None, height=50, background_color=(0.2, 0.6, 0.8, 1))  # Blue button
        go_back_button.bind(on_press=self.go_back)
        self.layout.add_widget(go_back_button)

        self.add_widget(self.layout)

    def calculate_max(self, instance):
        weight_input = self.weight_input.text
        reps_input = self.reps_input.text

        if not weight_input.replace('.', '', 1).isdigit() or not reps_input.isdigit():
            self.result_label.text = 'Please input the weight and repetitions as positive numbers'
        else:
            weight = float(weight_input)
            reps = int(reps_input)

            if weight < 0 or reps < 0:
                self.result_label.text = 'Please input a positive value.'
            else:
                selected_unit = self.unit_button.text

                if selected_unit == 'kg':
                    one_rep_max = weight / (1.0278 - 0.0278 * reps)
                    unit_str = 'kg'
                elif selected_unit == 'lbs':
                    one_rep_max = weight / (1.0278 - 0.0278 * reps)
                    unit_str = 'lbs'
                else:
                    self.result_label.text = 'Invalid unit, please select kg or lbs'
                    return

                self.result_label.text = f'Your one-rep max is: {one_rep_max:.2f} {unit_str}'

    def go_back(self, instance):
        self.manager.current = 'main'

class OneRepMaxApp(App):
    def build(self):
        self.sm = ScreenManager()

        self.main_screen = MainScreen(name='main')
        self.calculator_screen = OneRepMaxCalculator(name='calculator')
        self.connection_status_screen = ConnectionStatusScreen(name='connection_status')

        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.calculator_screen)
        self.sm.add_widget(self.connection_status_screen)

        return self.sm

if __name__ == '__main__':
    connected = True
    app = OneRepMaxApp()
    app.run()