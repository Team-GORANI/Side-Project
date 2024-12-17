import reflex as rx

def create_radio_input(radio_value):
    """Create a radio input element with specified value and styling."""
    return rx.el.input(
        class_name="form-radio",
        type="radio",
        name="object",
        value=radio_value,
        height="1.25rem",
        color="#2563EB",
        width="1.25rem",
    )


def create_span_text(span_content):
    """Create a span element with the given text content and color."""
    return rx.text.span(span_content, color="#374151")


def create_radio_label(radio_value, label_text):
    """Create a label element containing a radio input and text span."""
    return rx.el.label(
        create_radio_input(radio_value=radio_value),
        create_span_text(span_content=label_text),
        display="flex",
        align_items="center",
        column_gap="0.5rem",
    )


def create_upload_button():
    """Creates a styled label element for image upload."""
    return rx.el.label(
        " Upload Image ",
        background_color="#3B82F6",
        cursor="pointer",
        transition_duration="300ms",
        _hover={"background-color": "#2563EB"},
        padding_left="1rem",
        padding_right="1rem",
        padding_top="0.5rem",
        padding_bottom="0.5rem",
        border_radius="0.25rem",
        color="#ffffff",
        transition_property="background-color, border-color, color, fill, stroke, opacity, box-shadow, transform",
        transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
    )

def create_object_selection_form():
    """Create a form with radio buttons for object selection and a canvas."""
    return rx.form(
        rx.flex(
            create_radio_label(radio_value="tree", label_text="Tree"),
            create_radio_label(radio_value="house", label_text="House"),
            create_radio_label(radio_value="person", label_text="Person"),
            display="flex",
            flex_direction="column",
            gap="0.5rem",
        ),
        rx.flex(
            create_upload_button(),
            rx.el.input(
                id="image-upload",
                type="file",
                accept="image/*",
                display="none",
            ),
            display="flex",
            flex_direction="column",
            align_items="center",
        ),
        display="flex",
        flex_direction="column",
        gap="1rem",
    )


def create_detected_objects_section():
    """Create a section displaying detected objects with a heading and list."""
    return rx.box(
        rx.heading(
            "Detected Objects:",
            font_weight="600",
            margin_bottom="1rem",
            font_size="1.25rem",
            line_height="1.75rem",
            as_="h2",
        ),
        rx.list(
            rx.el.li("No objects detected yet"),
            list_style_type="disc",
            list_style_position="inside",
            color="#374151",
        ),
        margin_top="2rem",
    )


def create_object_detection_container():
    """Create the main container for the object detection interface."""
    return rx.box(
        rx.heading(
            "Object Detection",
            font_weight="700",
            margin_bottom="1.5rem",
            font_size="1.5rem",
            line_height="2rem",
            text_align="center",
            as_="h1",
        ),
        create_object_selection_form(),
        create_detected_objects_section(),
        background_color="#ffffff",
        padding="2rem",
        border_radius="0.5rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    )


def index():
    """Render the complete object detection page with all components."""
    return rx.fragment(
        rx.box(
            rx.flex(
                create_object_detection_container(),
                background_color="#F3F4F6",
                display="flex",
                flex_direction="column",
                align_items="center",
                justify_content="center",
                min_height="100vh",
            )
        )
    )