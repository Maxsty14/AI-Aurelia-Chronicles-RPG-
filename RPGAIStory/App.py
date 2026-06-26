import json
import os
from pathlib import Path

import streamlit as st

from AI.Client import AskModel, GetModel
from AI.Prompts import BuildPrompt
from Data.State import PlayerState, WorldState
from Engine.Game import restore_world, save_current_world
from Engine.UIHelper import ApplyStatChanges, DisplayEnemyData

WORLD_DIR = Path(__file__).resolve().parent / "Data" / "Worlds"


def load_world(world_id: str):
    world_file = WORLD_DIR / f"{world_id}_world.json"
    return json.loads(world_file.read_text(encoding="utf-8"))


def start_world(world_id: str):
    world_data = load_world(world_id)

    if restore_world(world_id):
        st.session_state.game_started = True
        return

    st.session_state.player = PlayerState()
    st.session_state.world = WorldState()
    st.session_state.world.current_storyline = world_data["current_storyline"]
    st.session_state.world.location = world_data["location"]
    st.session_state.story = world_data["intro"]
    st.session_state.selected_world = world_id
    st.session_state.game_started = True
    st.session_state.enemies = None
    st.session_state.terrain = None
    st.session_state.button_debounce = False


if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.world_saves = st.session_state.get("world_saves", {})

st.set_page_config(page_title="AI RPG Adventure", layout="wide")
st.markdown("""
<style>
    .stApp { max-width: 1100px; margin: 0 auto; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .story-panel { text-align: center; }
</style>
""", unsafe_allow_html=True)
st.title("AI RPG Adventure")

api_key = os.getenv("api_key")
chat = GetModel(api_key) if api_key else None

if not st.session_state.get("game_started", False):
    st.markdown("### Main Menu")
    st.write("Choose a world to start your adventure.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Elderwood Watch**")
        st.write("A misty village at the edge of a haunted forest.")
        saved_label = "Resume Elderwood Watch" if st.session_state.get("world_saves", {}).get("elderwood") else "Start Elderwood Watch"
        if st.button(saved_label):
            start_world("elderwood")
            st.rerun()
    with col2:
        st.markdown("**Skyreef Drift**")
        st.write("A luminous sea of clouds and floating reefs above the world.")
        saved_label = "Resume Skyreef Drift" if st.session_state.get("world_saves", {}).get("skyreef") else "Start Skyreef Drift"
        if st.button(saved_label):
            start_world("skyreef")
            st.rerun()

    if st.session_state.get("world_saves"):
        st.info("You already have saved progress for one or more worlds in this session.")
    else:
        st.caption("Start a world to create your first saved progress snapshot.")
    st.stop()

st.markdown(f"### World: {st.session_state.selected_world.title()}")
if st.button("Back to Main Menu"):
    save_current_world()
    st.session_state.game_started = False
    st.rerun()

st.markdown("### Story")
st.markdown(f'<div class="story-panel">{st.session_state.story}</div>', unsafe_allow_html=True)

if st.session_state.get("enemies"):
    DisplayEnemyData(json.loads(st.session_state.enemies))

if st.session_state.get("choices"):
    st.markdown("### Possible Choices")
    st.write(st.session_state.choices)

st.markdown("### Stats")
st.json({
    "health": st.session_state.player.health,
    "gold": st.session_state.player.gold,
    "inventory": st.session_state.player.inventory,
    "statuses": st.session_state.player.statuses,
})

if "button_debounce" not in st.session_state:
    st.session_state.button_debounce = False

with st.form("choice_form"):
    choice = st.text_input("What do you do?")
    submit = st.form_submit_button("Continue")

if submit:
    if st.session_state.button_debounce:
        st.warning("Please wait for the current action to process.")
    else:
        st.session_state.button_debounce = True

        prompt = BuildPrompt(
            st.session_state.player,
            st.session_state.world,
            st.session_state.story,
            st.session_state.enemies if "enemies" in st.session_state else None,
            st.session_state.terrain if "terrain" in st.session_state else None,
            choice,
        )

        raw = AskModel(chat, prompt)

        story = raw.split("[STORY]")[1].split("[DATA]")[0].strip() if "[DATA]" in raw else raw.split("[STORY]")[1].split("[STATS]")[0].strip()
        stats = raw.split("[STATS]")[1].split("[CHOICES]")[0].strip()
        enemies = raw.split("[DATA]")[1].split("[STATS]")[0].strip() if "[DATA]" in raw else None
        terrain = raw.split("[DATA]")[1].split("[STATS]")[1].strip() if "[DATA]" in raw else None
        choices = raw.split("[CHOICES]")[1].strip() if "[CHOICES]" in raw else None

        st.session_state.story = story
        st.session_state.world.time_played += 1

        changes = json.loads(stats)

        if enemies:
            st.session_state.enemies = enemies
            DisplayEnemyData(json.loads(enemies))
        else:
            st.session_state.enemies = None

        st.session_state.terrain = terrain if terrain else None
        st.session_state.choices = choices

        if st.session_state.get("choices"):
            st.markdown("### Possible Choices")
            st.write(st.session_state.choices)

        ApplyStatChanges(st.session_state.player, changes)
        save_current_world()

        st.session_state.button_debounce = False
        st.rerun()
