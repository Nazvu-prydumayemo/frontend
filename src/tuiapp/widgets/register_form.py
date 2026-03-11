from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Vertical
from .inputs import CustomInput, PasswordInput
from .buttons import PrimaryButton, SecondaryButton

class RegisterForm(Widget):
    def compose(self) -> ComposeResult:
        with Vertical(id="card"):
            yield Static("Registration", id="title")

            yield Static("Name - Lastname", classes="label")
            yield CustomInput(placeholder="Your Name-Lastname", id="name")

            yield Static("Email", classes="label")
            yield CustomInput(placeholder="Your Email", id="email")

            yield Static("Password", classes="label")
            yield PasswordInput(placeholder="Password", id="password")

            yield Static("Confirm Password", classes="label")
            yield PasswordInput(placeholder="Confirm Password", id="confirm")

            yield PrimaryButton("Register", id="register_btn")
            yield SecondaryButton("Back", id="back_btn")

    def get_data(self) -> dict:
        """Повертає словник з усіма введеними даними"""
        return {
            "name": self.query_one("#name", CustomInput).value,
            "email": self.query_one("#email", CustomInput).value,
            "password": self.query_one("#password", PasswordInput).value,
            "confirm": self.query_one("#confirm", PasswordInput).value,
        }