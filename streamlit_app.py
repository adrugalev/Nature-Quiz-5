from pathlib import Path
import shutil

import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).parent
HTML_PATH = ROOT / "outputs" / "nature-image-quiz.html"
ASSETS_PATH = ROOT / "outputs" / "assets"
STATIC_ASSETS_PATH = ROOT / "static" / "assets"


def ensure_static_assets():
    STATIC_ASSETS_PATH.parent.mkdir(exist_ok=True)

    if not STATIC_ASSETS_PATH.exists():
        shutil.copytree(ASSETS_PATH, STATIC_ASSETS_PATH)
        return

    source_files = sorted(path.relative_to(ASSETS_PATH) for path in ASSETS_PATH.rglob("*.png"))
    static_files = sorted(path.relative_to(STATIC_ASSETS_PATH) for path in STATIC_ASSETS_PATH.rglob("*.png"))

    if source_files != static_files:
        shutil.rmtree(STATIC_ASSETS_PATH)
        shutil.copytree(ASSETS_PATH, STATIC_ASSETS_PATH)


@st.cache_data
def load_quiz_html():
    html = HTML_PATH.read_text(encoding="utf-8")

    html = html.replace(
        "<script>",
        (
            "<script>"
            "function streamlitAssetUrl(path) {"
            "return `./app/static/${path}`;"
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
ensure_static_assets()
components.html(load_quiz_html(), height=960, scrolling=True)
