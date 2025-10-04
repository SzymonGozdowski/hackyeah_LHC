from folium.features import DivIcon


def set_icon_with_color(value_of_interest):
    green_intensity = value_of_interest
    red_intensity = 255 - green_intensity
    icon = DivIcon(
        html=f"""
        <div style="opacity: 0.5; background-color: rgb({red_intensity},{green_intensity},0); width: 30px; height: 30px; border-radius: 50%;"></div>
        """,
        icon_anchor=(15, 15),
    )
    return icon
