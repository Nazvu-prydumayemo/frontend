from textual.app import ComposeResult
from tuiapp.screens.base import BaseScreen
from tuiapp.widgets.register_form import RegisterForm

class RegisterScreen(BaseScreen):
   
    CSS_PATH = "../styles/styles.tcss"

    def compose(self) -> ComposeResult:
        yield RegisterForm()

    def on_button_pressed(self, event) -> None:
        form = self.query_one(RegisterForm)
        
        if event.button.id == "register_btn":
            data = form.get_data()

            if not all(data.values()):
                self.toast("Заповніть всі поля!")
                return

            if data["password"] != data["confirm"]:
                self.toast("Паролі не збігаються!")
                return

            self.toast("Реєстрація успішна!")

        elif event.button.id == "back_btn":
            self.go_back()


if __name__ == "__main__":
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(RegisterScreen())

    app = TestApp()
    app.run()