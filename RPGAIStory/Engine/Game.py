import streamlit as st

from Data.State import PlayerState, WorldState

def save_current_world():
    st.session_state.world_saves = st.session_state.get("world_saves", {})
    st.session_state.world_saves[st.session_state.get("selected_world", "elderwood")] = {
        "player": {
            "health": st.session_state.player.health,
            "gold": st.session_state.player.gold,
            "inventory": st.session_state.player.inventory,
            "statuses": st.session_state.player.statuses,
        },
        "world": {
            "current_storyline": st.session_state.world.current_storyline,
            "location": st.session_state.world.location,
            "time_played": st.session_state.world.time_played,
        },
        "story": st.session_state.story,
        "enemies": st.session_state.get("enemies"),
        "terrain": st.session_state.get("terrain"),
        "choices": st.session_state.get("choices"),
    }


def restore_world(world_id: str):
    saved = st.session_state.get("world_saves", {}).get(world_id)
    if not saved:
        return False

    st.session_state.player = PlayerState()
    st.session_state.player.health = saved["player"].get("health", st.session_state.player.health)
    st.session_state.player.gold = saved["player"].get("gold", st.session_state.player.gold)
    st.session_state.player.inventory = saved["player"].get("inventory", st.session_state.player.inventory)
    st.session_state.player.statuses = saved["player"].get("statuses", st.session_state.player.statuses)

    st.session_state.world = WorldState()
    st.session_state.world.current_storyline = saved["world"].get("current_storyline", st.session_state.world.current_storyline)
    st.session_state.world.location = saved["world"].get("location", st.session_state.world.location)
    st.session_state.world.time_played = saved["world"].get("time_played", st.session_state.world.time_played)

    st.session_state.story = saved.get("story", "")
    st.session_state.enemies = saved.get("enemies")
    st.session_state.terrain = saved.get("terrain")
    st.session_state.choices = saved.get("choices")
    st.session_state.selected_world = world_id
    st.session_state.button_debounce = False
    return True
