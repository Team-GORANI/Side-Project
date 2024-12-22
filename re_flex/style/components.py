# styles/components.py
from .colors import Colors
from .spacing import Spacing
from .layout import Layout

class ComponentStyles:
    RADIO_INPUT = {
        "height": "1.25rem",
        "width": "1.25rem",
        "color": Colors.PRIMARY
    }

    UPLOAD_BUTTON = {
        "background_color": Colors.PRIMARY_LIGHT,
        "padding_left": Spacing.PADDING["md"],
        "padding_right": Spacing.PADDING["md"],
        "padding_top": Spacing.PADDING["sm"],
        "padding_bottom": Spacing.PADDING["sm"],
        "border_radius": Layout.BORDER_RADIUS["sm"],
        "color": Colors.WHITE,
        "cursor": "pointer",
        "transition_duration": "300ms",
        "transition_property": "background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
        "transition_timing_function": "cubic-bezier(0.4, 0, 0.2, 1)",
        "_hover": {
            "background-color": Colors.PRIMARY
        }
    }

    CONTAINER = {
        "background_color": Colors.WHITE,
        "padding": Spacing.PADDING["xl"],
        "border_radius": Layout.BORDER_RADIUS["md"],
        "box_shadow": Layout.SHADOWS["md"]
    }
