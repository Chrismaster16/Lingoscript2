from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

with open('nederlands3.txt', encoding="latin-1") as f:
    word_list = f.read().splitlines()

class Lingoscript:
    def __init__(self, total_letters, substring_list, substring_position_list):
        self.total_letters = total_letters
        self.substring_list = substring_list
        self.substring_position_list = substring_position_list

        known_letters = len(self.substring_list)

        suggestion_list = []

        loop_amount = known_letters
        max_loop_amount = known_letters
        end_suggestions = []
        while loop_amount > 0:
            substring = substring_list[loop_amount - 1]
            if substring == "_" and loop_amount == max_loop_amount:
                end_suggestions = word_list
                loop_amount = loop_amount - 1
                continue
            elif substring == "_":
                loop_amount = loop_amount - 1
                continue
            elif loop_amount == max_loop_amount:
                for s in filter(lambda x: substring in x, word_list): suggestion_list.append(s)
            else:
                for s in filter(lambda x: substring in x, end_suggestions): suggestion_list.append(s)
            end_suggestions = suggestion_list
            suggestion_list = []
            loop_amount = loop_amount - 1

        end_suggestions = (list(filter(lambda x: len(x) == total_letters, end_suggestions)))
        i = 0
        pre_end_suggestions = []
        pre_end_suggestions = end_suggestions.copy()

        loop_amount = len(end_suggestions)
        while i < loop_amount:
            current_check = pre_end_suggestions[i]
            j = 0
            while j < len(substring_list):
                if substring_list[j] == "_":
                    drop = False
                else:
                    letter_position = int(substring_position_list[j])
                    word_converted_to_list = Convert(current_check)
                    if word_converted_to_list[letter_position - 1] == substring_list[j]:
                        drop = False
                    else:
                        drop = True
                if drop == True:
                    end_suggestions.remove(current_check)
                    break
                j = j + 1
            i = i + 1
        self.end_suggestions = end_suggestions

    def get_word_list(self):
        return self.end_suggestions


def Convert(string):
    list1 = []
    list1[:0] = string
    return list1

class MyGridLayout(GridLayout):
    #Initialize infinity keywords
    def __init__(self, **kwargs):
        # Call grid layout constructor
        super(MyGridLayout, self).__init__(**kwargs)

        # Set columns
        self.cols = 1

        # Add widget
        self.add_widget(Label(text = "Type your word with _ for your missing letters",
                              font_size = 60,
                              size_hint_y = None,
                              height = 400
                              ))
        #Add inputbox
        self.input = TextInput(multiline = False,
                               font_size=60,
                               size_hint_y=None,
                               height=400)
        self.add_widget(self.input)

        self.output_text = "Nothing"
        self.label = Label(text=str(self.output_text), font_size = 30, height = 200)
        self.add_widget(self.label)

    def add_money(self):
        self.money += 1
        self.label.text = str(self.money)

    def press(self):
        letter_input = self.input.text
        substring_list = Convert(letter_input)
        substring_position_list = []
        k = 1
        while k < len(substring_list) + 1:
            substring_position_list.append(k)
            k = k + 1

        output = Lingoscript(len(substring_list), substring_list, substring_position_list)
        if len(output.get_word_list()) > 36:
            self.label.text = "Not enough info to make a suggestion"
        else:
            self.output_text = (', '.join(output.get_word_list()))
            # Add widget
            self.label.text = self.output_text

Builder.load_string('''
<MyGridLayout>:
    name: "MyGridLayout"

    Button:
        on_release: root.press()
        text: "Press"
        font_size: 60
        height: 400
        
    ''')

class TestApp(App):
    def build(self):
        return MyGridLayout()

if __name__ == '__main__':
    TestApp().run()