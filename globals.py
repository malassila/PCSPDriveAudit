version = "v1.0.0"

THEME = "dark"

num_connected = 0
connected_drives = []
connected_treeview = None

mysql_host = '192.168.1.156'
mysql_database = 'drive-project'

po_chassis_list = []
po_parts_list = []


selected_description = ""
switch_variables = []
department_filter_options_vals = []
filter_options = []

mysql_user = 'python'
mysql_password = 'ghXryPCSP2022!'
api_user = 'pcsp.shared@gmail.com'
api_password = 'ghXryPCSP2022!'


blue = "#34425a"
yellow = "#f39c06"
red = "#d10d05"
purple = "#315954"
dark_blue = "#26538d"
dark_gray = "#222222"
gray = "#989898"
black = "#000000"
white = "#ffffff"

cpu_cart = 'CART-0000'
part_cart = 'CART-0001'
green_cone = 'Cone Green 1'
yellow_cone = 'Cone Yellow 1'
red_cone = 'Cone Red 1'


def get_headers(access_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

def get_hex_color(color_name):
    return colors.get(color_name.lower())

def get_port_name(slot_name):
    return port_dictionary.get(slot_name)

def set_row_status(treeview, item, status):
    # Set the tag for the row depending on the status
    tag = ""
    if status == "Connected" or status == "Disconnected":
        tag = "connected"
    elif status == "Wiping":
        tag = "wiping"
    elif status == "Wiped":
        tag = "wiped"
    elif status == "Wipe Failed":
        tag = "wipe_failed"
    treeview.item(item, tags=(tag,))
    


port_dictionary = {
    "01": "A6",
    "02": "A5",
    "03": "A4",
    "04": "A3",
    "05": "A2",
    "06": "A1",
    "07": "B6",
    "08": "B5",
    "09": "B4",
    "10": "B3",
    "11": "B2",
    "12": "B1",
    "13": "C6",
    "14": "C5",
    "15": "C4",
    "16": "C3",
    "17": "C2",
    "18": "C1",
    "19": "D6",
    "20": "D5",
    "21": "D4",
    "22": "D3",
    "23": "D2",
    "24": "D1"
}

colors = {
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadetblue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "companylightgreen": "#c1d860",
    "coral": "#ff7f50",
    "cornflowerblue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgoldenrod": "#b8860b",
    "darkgray": "#192428",
    "darkgreen": "#006400",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b",
    "darkslategray": "#2f4f4f",
    "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3",
    "deeppink": "#ff1493",
    "deepskyblue": "#00bfff",
    "dimgray": "#696969",
    "dodgerblue": "#1e90ff",
    "firebrick": "#b22222",
    "floralwhite": "#fffaf0",
    "forestgreen": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghostwhite": "#f8f8ff",
    "gold": "#ffd700",
    "goldenrod": "#daa520",
    "gray": "#414c50",
    "darkergray": "#2d383c",
    "green": "#008000",
    "greenyellow": "#adff2f",
    "honeydew": "#f0fff0",
    "hotpink": "#ff69b4",
    "indianred": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5",
    "lawngreen": "#7cfc00",
    "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    "lightcoral": "#f08080",
    "lightcyan": "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgray": "#d3d3d3",
    "lightgreen": "#90ee90",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa",
    "lightslategray": "#778899",
    "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee",
    "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585",
    "midnightblue": "#191970",
    "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "navy": "#000080",
    "oceanblue": "#39ace7",
    "lightoceanblue": "#2e9d4f",
    "darkoceanblue": "#0784b5",
    "oldlace": "#fdf5e6",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa",
    "palegreen": "#98fb98",
    "paleturquoise": "#afeeee",
    "palevioletred": "#d87093",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powderblue": "#b0e0e6",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#ff0000",
    "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1",
    "saddlebrown": "#8b4513",
    "salmon": "#fa8072",
    "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    "seashell": "#fff5ee",
    "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    "slateblue": "#6a5acd",
    "slategray": "#708090",
    "snow": "#fffafa",
    "springgreen": "#00ff7f",
    "steelblue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellowgreen": "#9acd32"
}

