from textual.theme import Theme

tennis_theme = Theme(
    name="tennis",
    primary="#2b332a",
    secondary="#3e473a",
    accent="#EDE8DC",
    foreground="#EDE8DC",
    background="#1E2A2A",
    success="#A3BE8C",
    warning="#963417",
    error="#BF616A",
    surface="#2b332a",
    panel="#3e473a",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#EDE8DC",
        "input-selection-background": "#3A4A4A 35%",
    },
)