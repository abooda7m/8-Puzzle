import streamlit as st
import heapq
import time
import random
import pandas as pd

# --- CSS Styling ---
st.markdown("""
    <style>
    .puzzle-wrapper { display: flex; justify-content: center; }
    .puzzle-container {
        padding: 10px;
        background-color: #223a5e;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 0 8px rgba(0,0,0,0.3);
    }
    .puzzle-row { display: flex; justify-content: center; }
    .tile {
        width: 55px;
        height: 55px;
        font-size: 20px;
        font-weight: bold;
        background-color: #4a72a5;
        color: #ffffff;
        border: 1px solid #6b8bbd;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 4px;
        margin: 1px;
    }
    .blank { background-color: #1a2a40; }
    </style>
""", unsafe_allow_html=True)

def manhattan_distance(state, goal):
    distance = 0
    for i, tile in enumerate(state):
        if tile == 0: continue
        goal_index = goal.index(tile)
        x1, y1 = divmod(i, 3)
        x2, y2 = divmod(goal_index, 3)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def count_inversions(puzzle):
    inv_count = 0
    arr = [num for num in puzzle if num != 0]
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv_count += 1
    return inv_count

def is_solvable_pair(start, goal):
    return count_inversions(start) % 2 == count_inversions(goal) % 2

def generate_solvable_puzzle():
    puzzle = list(range(9))
    while True:
        random.shuffle(puzzle)
        if count_inversions(puzzle) % 2 == 0:
            return puzzle

def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    x, y = divmod(zero_index, 3)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            ni = nx * 3 + ny
            new_state = state.copy()
            new_state[zero_index], new_state[ni] = new_state[ni], new_state[zero_index]
            neighbors.append(new_state)
    return neighbors

def a_star(start, goal):
    open_list = []
    heapq.heappush(open_list, (manhattan_distance(start, goal), 0, start, [start]))
    visited = set()
    start_time = time.time()
    while open_list:
        _, cost, current, path = heapq.heappop(open_list)
        if tuple(current) in visited: continue
        visited.add(tuple(current))
        if current == goal:
            return path, time.time() - start_time
        for neighbor in get_neighbors(current):
            if tuple(neighbor) not in visited:
                heapq.heappush(open_list, (cost + 1 + manhattan_distance(neighbor, goal), cost + 1, neighbor, path + [neighbor]))
    return None, time.time() - start_time

def hill_climbing(start, goal):
    current = start
    path = [current]
    start_time = time.time()
    while True:
        neighbors = get_neighbors(current)
        current_h = manhattan_distance(current, goal)
        next_state = current
        for neighbor in neighbors:
            h = manhattan_distance(neighbor, goal)
            if h < current_h:
                next_state = neighbor
                current_h = h
        if next_state == current:
            break
        current = next_state
        path.append(current)
        if current == goal:
            return path, time.time() - start_time
    return path if current == goal else path, time.time() - start_time

def display_puzzle(state):
    html = "<div class='puzzle-wrapper'><div class='puzzle-container'>"
    for i in range(0, 9, 3):
        html += "<div class='puzzle-row'>"
        for j in range(3):
            val = state[i + j]
            tile_class = "tile blank" if val == 0 else "tile"
            html += f"<div class='{tile_class}'>{'' if val == 0 else val}</div>"
        html += "</div>"
    html += "</div></div>"
    st.markdown(html, unsafe_allow_html=True)

st.title("8-Puzzle Solver with A* and Hill Climbing")
st.markdown("Enter the start and goal state as a 3x3 grid using numbers (0–8) and **0** represents the blank tile.")

if "start_state" not in st.session_state:
    st.session_state.start_state = generate_solvable_puzzle()

if st.button("🎲 Generate Random Puzzle"):
    st.session_state.start_state = generate_solvable_puzzle()

start_state = []
goal_state = []

st.subheader("Start State")
start_state = []
for i in range(3):
    cols = st.columns([1, 1, 1], gap="small")
    for j in range(3):
        idx = i * 3 + j
        with cols[j]:
            start_state.append(
                st.number_input(f"S{idx}", 0, 8, key=f"s{idx}", value=st.session_state.start_state[idx], label_visibility="collapsed"))

st.subheader("Goal State")
goal_state = []
goal_default = [1, 2, 3, 4, 5, 6, 7, 8, 0]
for i in range(3):
    cols = st.columns([1, 1, 1], gap="small")
    for j in range(3):
        idx = i * 3 + j
        with cols[j]:
            goal_state.append(
                st.number_input(f"G{idx}", 0, 8, key=f"g{idx}", value=goal_default[idx], label_visibility="collapsed"))
# --- Duplicate check before Solve ---
if len(set(start_state)) < 9:
    st.error("⚠️ Duplicate values in Start State! Make sure each number from 0 to 8 appears once.")
elif len(set(goal_state)) < 9:
    st.error("⚠️ Duplicate values in Goal State! Make sure each number from 0 to 8 appears once.")
elif st.button("Solve"):
    if not is_solvable_pair(start_state, goal_state):
        st.error("⚠️ The inversion count parity between start and goal does not match. Puzzle is unsolvable.")
    else:
        with st.spinner("Solving with A*..."):
            a_path, a_time = a_star(start_state, goal_state)
        with st.spinner("Solving with Hill Climbing..."):
            h_path, h_time = hill_climbing(start_state, goal_state)

        st.subheader("A* Result")
        if a_path:
            st.success(f"Solved in {len(a_path) - 1} steps, Time: {round(a_time, 4)} sec")
            for i, step in enumerate(a_path):
                g = i
                h = manhattan_distance(step, goal_state)
                f = g + h
                st.markdown(f"<h4 style='text-align: center;'>Step {i} — f(n) = g(n) + h(n) = {g} + {h} = {f}</h4>", unsafe_allow_html=True)
                display_puzzle(step)
        else:
            st.error("A* failed to solve.")

        st.subheader("Hill Climbing Result")
        if h_path:
            if h_path[-1] == goal_state:
                st.success(f"Hill Climbing solved in {len(h_path) - 1} steps, Time: {round(h_time, 4)} sec")
            else:
                st.warning(f"Hill Climbing stuck in local minimum. Steps: {len(h_path)-1}, Time: {round(h_time, 4)} sec")
            for i, step in enumerate(h_path):
                st.markdown(f"<h4 style='text-align: center;'>Step {i}</h4>", unsafe_allow_html=True)
                display_puzzle(step)
        else:
            st.error("Hill Climbing failed to solve.")

if st.button("🔁 Run 10 Random Simulations"):
    results = []
    for i in range(1, 11):
        while True:
            start = generate_solvable_puzzle()
            goal = generate_solvable_puzzle()
            if is_solvable_pair(start, goal):
                break
        a_path, a_time = a_star(start, goal)
        h_path, h_time = hill_climbing(start, goal)

        results.append({
            "Instance": i,
            "Start State": start,
            "Goal State": goal,
            "A*_Steps": len(a_path)-1 if a_path else "Fail",
            "A*_Time": round(a_time, 4),
            "HC_Steps": len(h_path)-1 if h_path else "Fail",
            "HC_Time (till stop)": round(h_time, 4),
            "Solved by A*": a_path is not None,
            "Solved by HC": h_path is not None and h_path[-1] == goal
        })

    df = pd.DataFrame(results)
    st.subheader("🔍 Simulation Results (10 Random Runs)")
    st.dataframe(df)
    st.write(f"- A* Success Rate: {df['Solved by A*'].mean() * 100:.1f}%")
    st.write(f"- Hill Climbing Success Rate: {df['Solved by HC'].mean() * 100:.1f}%")
    st.write(f"- A* avg steps: {df['A*_Steps'].mean()} — HC avg steps: {df['HC_Steps'].mean()}")
