import reflex as rx
from styles.typography import Typography
from styles.colors import Colors
from styles.spacing import Spacing

class DetectedObjectsSection:
    @staticmethod
    def create() -> rx.Component:
        return rx.box(
            rx.heading(
                "Detected Objects:",
                margin_bottom=Spacing.MARGIN["md"],
                **Typography.HEADING["h2"],
                as_="h2"
            ),
            rx.list(
                rx.el.li("No objects detected yet"),
                list_style_type="disc",
                list_style_position="inside",
                color=Colors.TEXT["primary"]
            ),
            margin_top=Spacing.MARGIN["xl"]
        )