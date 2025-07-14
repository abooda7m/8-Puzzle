# 8-Puzzle Solver

This is a visual and interactive implementation of the classic **8-puzzle** problem using Streamlit. The application allows users to solve the puzzle using two different algorithms: **A* Search** and **Hill Climbing**, with an intuitive interface for entering custom puzzles or generating random ones.

---

## Features

- **Visual Grid Interface** to input both the start and goal states.
- **Two Algorithms Implemented**:
  - A* Search (with Manhattan Distance heuristic)
  - Hill Climbing (greedy local search)
- **Step-by-Step Visualization** of solution paths.
- **Random Puzzle Generator** with guaranteed solvability.
- **Run 10 Simulations** to compare performance across different randomly generated puzzles.

---

## Technologies Used

- Python
- Streamlit (for interactive UI)
- Pandas (for simulation results table)
- heapq (priority queue for A*)
- Custom CSS styling for tile display

---

## How to Run

1. Clone the repository:
```bash
https://github.com/your_username/8-puzzle-solver.git
cd 8-puzzle-solver
```

2. Create a virtual environment and activate it:
```bash
uv venv my_env
my_env\Scripts\activate  # on Windows
```

3. Install the dependencies:
```bash
uv pip install -r requirements.txt
```

4. Launch the app:
```bash
streamlit run app.py
```

---

## Usage

- Modify the **Start State** and **Goal State** manually or use the **Generate Random Puzzle** button.
- Click **Solve** to run both A* and Hill Climbing and display the solutions.
- Use **Run 10 Random Simulations** to compare success rate and average performance metrics.

---

## Notes

- A* guarantees finding the shortest solution path if solvable.
- Hill Climbing is faster but may get stuck in local minima.
- The puzzle solvability is determined by comparing the parity of inversions in the start and goal states.

---

## License

This project is for educational and demonstration purposes only.
