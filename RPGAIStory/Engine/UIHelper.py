import streamlit as st

def ApplyStatChanges(player, changes):
    player.health = changes.get("health", 0)
    player.gold = changes.get("gold", 0)

    player.inventory = changes.get("inventory", player.inventory)
    player.statuses = changes.get("statuses", player.statuses)

def DisplayEnemyData(enemy_data):

    st.markdown("### Enemies Encountered")
    for enemy in enemy_data.get("enemies", []):
        if enemy.get("inventory"):
            enemy["inventory"] = [item for item in enemy["inventory"] if item]  # Filter out empty items
            
        st.write(f"**{enemy['name']}**")
        st.json({
            "health": enemy['health'],
            "inventory": enemy.get("inventory") or [],
            "statuses": enemy.get("statuses") or []
        })