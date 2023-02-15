from ipywidgets import widgets
#from ipywidgets import interact,interactive, interact_manual, Button, Output, HBox, VBox, Layout

style = {'description_width': 'initial'}
bw = '90%'
#------------------------widget templates-----------------------------------------------------

def create_datepicker(param, param_name, tag=''):
    if tag=='':
        tag = param_name
    param[param_name] = None
    def datepicker_f(change):
        param[param_name] = change.new
        #print(param[param_name])
    datepicker_w = widgets.DatePicker(
        description=tag,
        disabled=False,
        layout={'width': bw}, style=style
    )
    datepicker_w.observe(datepicker_f,'value')
    return datepicker_w




def create_dropdown(param, param_name, param_list, param_value, tag=''):
    if tag=='':
        tag = param_name
    param[param_name] = param_value
    def dropdown_f(change):
        param[param_name] = change.new
    #tradeDirection_w = interactive(tradeDirection_f, tradeDirection=['BOTH','LONG','SHORT'])
    dropdown_w=widgets.Dropdown(
        options=param_list,
        value=param[param_name],
        decription=tag,
        layout={'width': bw}, style=style
    )
    dropdown_w.observe(dropdown_f, 'value')
    return dropdown_w



def create_checkbox(param, param_name, param_value, tag=''):
    if tag=='':
        tag = param_name
    param[param_name] = param_value
    def checkbox_f(change):
        param[param_name] = change.new
    checkbox_w = widgets.Checkbox(
        value=param[param_name],
        description=tag,
        disabled=False,
        indent=False,
        layout={'width': bw}
    )
    checkbox_w.observe(checkbox_f, 'value')
    return checkbox_w



class create_inttext2():
    def __init__(self, param, param_name, param_value, tag=''):
        self.param = param
        self.param_name = param_name
        self.param_value = param_value
        self.tag = tag
        if self.tag=='':
            self.tag = self.param_name
        self.param[self.param_name] = self.param_value
    def inttext_f(self, change):
        #print("I am in class")
        self.param[self.param_value] = change.new
    def create(self):
        inttext_w=widgets.IntText(value=self.param[self.param_name],description=self.tag, disabled=False, layout={'width': bw}, style=style)
        inttext_w.observe(self.inttext_f,'value')
        return inttext_w


def create_inttext(param, param_name, param_value, tag=''):
    if tag=='':
        tag = param_name
    param[param_name] = param_value
    def inttext_f(change):
        #print("I am in method")
        #print("1-->",param_value, change.new)
        param[param_name] = change.new
        #print("2-->",param_value)
    inttext_w=widgets.IntText(value=param[param_name],description=tag,\
                                  disabled=False, layout={'width': bw}, style=style)
    inttext_w.observe(inttext_f,'value')
    return inttext_w



def create_floattext(param, param_name, param_value, tag=''):
    if tag=='':
        tag = ''
    param[param_name] = param_value
    #def floattext_f(change):
    #    param[param_name] = change.new
    floattext_w=widgets.FloatText(value=param[param_name],description=tag,\
                                  disabled=False, layout={'width': bw}, style=style)
    #floattext_w.observe(floattext_f,'value')
    return floattext_w



def create_button(param, param_name, param_value, tag='',color='gray'):
    if tag=='':
        tag = param_name
    param[param_name] = param_value
    button = widgets.Button(description=tag,layout={'width': bw})
    button.style.button_color = color
    #def on_button_clicked(b):
    #    print(param)
    #button.on_click(on_button_clicked)
    return button

