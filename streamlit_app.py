import base64
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).parent
HTML_PATH = ROOT / "outputs" / "nature-image-quiz.html"
ASSETS_PATH = ROOT / "outputs" / "assets"


def image_data_uri(path):
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


@st.cache_data
def load_quiz_html():
    html = HTML_PATH.read_text(encoding="utf-8")

    asset_map = {
        f"assets/{path.relative_to(ASSETS_PATH).as_posix()}": image_data_uri(path)
        for path in ASSETS_PATH.rglob("*.png")
    }

    html = html.replace(
        "<script>",
        (
            "<script>"
            f"window.__STREAMLIT_ASSETS__ = {json.dumps(asset_map)};"
            "function streamlitAssetUrl(path) {"
            "return window.__STREAMLIT_ASSETS__[path] || path;"
            "}"
            "</script>\n<script>"
        ),
        1,
    )

    replacements = {
        "return `assets/flowers/${item.id}.png`;": "return streamlitAssetUrl(`assets/flowers/${item.id}.png`);",
        "return `assets/trees/${item.id}.png`;": "return streamlitAssetUrl(`assets/trees/${item.id}.png`);",
        "return `assets/birds/${item.id}.png`;": "return streamlitAssetUrl(`assets/birds/${item.id}.png`);",
        "return `assets/animals/${item.id}.png`;": "return streamlitAssetUrl(`assets/animals/${item.id}.png`);",
        "return `assets/fish/${item.id}.png`;": "return streamlitAssetUrl(`assets/fish/${item.id}.png`);",
        "return `assets/modes/${modeId}.png`;": "return streamlitAssetUrl(`assets/modes/${modeId}.png`);",
    }

    for old, new in replacements.items():
        html = html.replace(old, new)

    return html


st.set_page_config(page_title="Nature image quiz", layout="wide")
components.html(load_quiz_html(), height=960, scrolling=True)
