import kivy
import psycopg2

from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRoundFlatButton

hostname = 'bm6khqsqov0isvg8vhkw-postgresql.services.clever-cloud.com'
database = 'bm6khqsqov0isvg8vhkw'
username = 'uvn1dlsxbb8djhqsx9or'
pwd = 'WLgUSCg6u5ltpEXwowZuBCHv3ZTyyU'
port_id = 5432
conn = None
cur = None

KV = '''WindowManager:
    MainMenu:
    LogScreen:
    RegScreen:
    MainScreen:
    
<MainScreen>:
    name: "mainscreen"
    MDScreen:
  
    
    MDBottomNavigation:
  
        
        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Гардероб'
            icon: 'wardrobe'
  
            
            MDLabel:
                text: 'Одежда'
                halign: 'center'
  
        
        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Образы'
            icon: 'hanger'
  
            
            MDLabel:
                text: 'Образы'
                halign: 'center'
  
        
        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'Профиль'
            icon: 'account'
  
            
            MDLabel:
                text: 'Профиль'
                halign: 'center'
<MainMenu>:
    name: "mainmenu"
    GridLayout:
        cols: 1
        size: root.width, root.height

        Button:
            text: "Зарегистрироваться"
            on_release:
                app.root.current = "registrationscreen"
                root.manager.transition.direction = "left"


        Button:
            text: "Войти"
            on_release:
                app.root.current = "loginscreen"
                root.manager.transition.direction = "left"

<LogScreen>:
    name: "loginscreen"
    login: login
    password: password

    GridLayout:
        cols: 1
        size: root.width, root.height
        
        GridLayout:
            cols: 1


            MDTextField:
                id: login
                width: "360dp"
                pos_hint:{'center_x':.5,'center_y':.5}
                mode: "fill"
                size_hint_x: None
                hint_text: "Логин"
                icon_left: "account"
                multiline: False

           

            MDTextField:
                id: password
                width: "360dp"
                mode: "fill"
                pos_hint:{'center_x':.5,'center_y':.5}
                size_hint_x: None
                hint_text: "Пароль"
                icon_left: "lock"
                multiline: False
        GridLayout:
            cols: 2

            MDRoundFlatButton:
                text: "Войти"
                width: "360dp"
                on_release: 
                    root.sumbitb()

            MDRoundFlatButton:
                text: "Назад"
                width: "360dp"
                on_release: 
                    app.root.current = "mainmenu"
                    root.manager.transition.direction = "right"

<RegScreen>
    name: "registrationscreen"
    login: login
    password: password
    email: email

    GridLayout:
        cols: 1
        size: root.width, root.height
        
        GridLayout:
            cols: 2

            MDLabel:
                text: "Логин: "

            TextInput:
                id: login
                multiline: False

            MDLabel:
                text: "Пароль: "

            MDTextField:
                id: password
                multiline: False

            MDLabel:
                text: "Электронная почта: "
            
            MDTextField:
                id: email
                multiline: False

        Button:
            text: "Зарегистрироваться"
            on_release: root.regb()

        Button:
            text: "Назад"
            on_release: 
                app.root.current = "mainmenu"
                root.manager.transition.direction = "right"


     '''

class WindowManager(ScreenManager):
    pass
  
class MainMenu(Screen):
    pass

class LogScreen(Screen):
  login = ObjectProperty(None)
  password = ObjectProperty(None)


  def sumbitb(self):
    try:
      conn = psycopg2.connect(
                    host = hostname,
                    dbname = database,
                    user = username,
                    password = pwd,
                    port = port_id
                    )
      cur = conn.cursor()
      select_script = f'SELECT password FROM public."Users" WHERE login = 'f"'{self.login.text}'"
      cur.execute(select_script)
      record = cur.fetchone()
      if str(record[0]) == self.password.text:
        print("Success")
        self.manager.current = "mainscreen"
      else:
        popup = Popup(title = 'Неправильный пароль', content = Label(text='Вы ввели неправильный пароль! Повторите попытку') , size_hint = (None, None), size=(400, 400))
        popup.open()  
      conn.commit()
    except Exception as error:
            print(error)
    finally:
       if cur is not None:
                cur.close()
       if conn is not None:
                conn.close() 

class RegScreen(Screen):
  def regb(self):
    try:
      conn = psycopg2.connect(
                    host = hostname,
                    dbname = database,
                    user = username,
                    password = pwd,
                    port = port_id
                    )
      cur = conn.cursor()
      exist_script = f'SELECT exists(SELECT 1 FROM public."Users" WHERE login = 'f"'{self.login.text}')"
      insert_script = f'INSERT INTO public."Users"(login, password, email) VALUES ({self.login.text}, {self.password.text}, {self.email.text});'
      cur.execute(exist_script)
      record = cur.fetchone()
      if str(record[0]) == 'True':
        popup = Popup(title = 'Это имя уже занятно', content = Label(text='Это имя уже занятно, придумайте другое') , size_hint = (None, None), size=(400, 400))
        popup.open()
        print("Already exist")
      else:
        cur.execute(insert_script)
        self.manager.current = 'mainmenu'
        self.manager.transition.direction = "right"
      
      conn.commit()
    except Exception as error:
            print(error)
    finally:
       if cur is not None:
                cur.close()
       if conn is not None:
                conn.close() 
          
 

class MainScreen(Screen):
  pass
      


class Acloset(MDApp):
  def build(self):

      screen = Builder.load_string(KV)
      return screen

if __name__ == "__main__":
  Acloset().run()