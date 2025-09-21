# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, StringProperty
import pyrebase
from config import firebase_config

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

# ----------------- Screens -----------------
class WelcomeScreen(Screen):
    pass

class LoginScreen(Screen):
    def login_user(self, email, password):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print("Login successful", user['email'])
            self.manager.current = "home"
        except Exception as e:
            print("Login failed:", e)

class SignupScreen(Screen):
    def signup_user(self, email, password):
        try:
            auth.create_user_with_email_and_password(email, password)
            print("User created")
            self.manager.current = "login"
        except Exception as e:
            print("Signup failed:", e)

class HomeScreen(Screen):
    medicines = ListProperty([])

    def on_enter(self):
        self.get_medicines()

    def get_medicines(self):
        try:
            meds = db.child("medicines").get()
            self.medicines = [med.val() for med in meds.each()]
            print("Medicines loaded:", self.medicines)
        except Exception as e:
            print("Error loading medicines:", e)

class CartScreen(Screen):
    cart_items = ListProperty([])

    def add_to_cart(self, medicine):
        self.cart_items.append(medicine)
        print(f"{medicine['name']} added to cart")

    def place_order(self):
        if self.cart_items:
            print(f"Order placed for {len(self.cart_items)} items (Payment stub)")
            self.cart_items.clear()
        else:
            print("Cart is empty!")

# ----------------- Screen Manager -----------------
sm = ScreenManager()
sm.add_widget(WelcomeScreen(name='welcome'))
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(SignupScreen(name='signup'))
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(CartScreen(name='cart'))

# ----------------- App -----------------
class MedCareApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MedCareApp().run()
