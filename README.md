# 🤖 Dynamic Pathfinding Agent
### AI 2002 – Artificial Intelligence | Assignment 2 – Question 6 | Spring 2026
### National University of Computer & Emerging Sciences – Chiniot-Faisalabad Campus

---

## 📌 Overview

A fully interactive, GUI-based **Dynamic Pathfinding Agent** that visualizes **Greedy Best-First Search (GBFS)** and **A\* Search** on a live grid. Supports real-time obstacle spawning and automatic re-planning when the path is blocked.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Algorithms** | GBFS (`f = h(n)`) and A* (`f = g(n) + h(n)`) |
| 📐 **Heuristics** | Manhattan Distance & Euclidean Distance (toggle via GUI) |
| 💥 **Dynamic Mode** | Randomly spawns new obstacles while agent moves; triggers instant re-planning |
| 🖱️ **Interactive Editor** | Click/drag to place or remove walls; move Start/Goal nodes |
| 🌀 **Maze Generator** | One-click random maze with configurable obstacle density |
| 🎨 **Visualization** | Yellow = Frontier, Indigo = Visited, Green = Final Path, White dot = Agent |
| 📊 **Metrics Dashboard** | Nodes Expanded, Path Cost, Execution Time (ms), Live Status |
| 🪜 **Step Mode** | Manually step through the search frame-by-frame |

---

## 🛠️ Installation

### Requirements
- Python **3.8** or higher
- `pygame` library

### Install Dependencies

```bash
pip install pygame
```

> No other external libraries required.

---

## ▶️ Running the Application

```bash
python pathfinding_agent.py
```

---

## 🎮 Controls

### Mouse Controls

| Action | Result |
|---|---|
| **Left Click** on empty cell | Place wall (in Wall mode) |
| **Left Click** on wall | Remove wall |
| **Click + Drag** | Place/remove walls continuously |
| **Click** Start/Goal button then click grid | Move Start or Goal node |

### GUI Buttons

| Button | Action |
|---|---|
| **GBFS** | Switch to Greedy Best-First Search |
| **A\*** | Switch to A* Search |
| **Manhattan** | Use Manhattan Distance heuristic |
| **Euclidean** | Use Euclidean Distance heuristic |
| **Wall / Start / Goal** | Switch placement mode |
| **▶ Run Search** | Execute selected algorithm and animate path |
| **Step Fwd** | Advance animation one frame at a time |
| **Replay** | Replay the last search animation |
| **Clear Path** | Remove visualization, keep walls intact |
| **Reset Grid** | Clear everything (walls + path) |
| **Generate Maze** | Auto-generate random maze (28% wall density) |
| **Dynamic Mode** | Toggle real-time obstacle spawning + auto re-planning |

---

## 🧠 Algorithm Details

### 🔵 Greedy Best-First Search (GBFS)

| Property | Value |
|---|---|
| **Evaluation Function** | `f(n) = h(n)` |
| **Node Strategy** | Strict Visited List – nodes never re-opened |
| **Optimal?** | No – finds *a* path, not necessarily the shortest |
| **Fast?** | Yes – very quick in open grids |
| **Best Case** | Open grids with clear line-of-sight to goal |
| **Worst Case** | U-shaped walls or dead ends the heuristic cannot detect |

### 🟢 A\* Search

| Property | Value |
|---|---|
| **Evaluation Function** | `f(n) = g(n) + h(n)` |
| **Node Strategy** | Expanded List – nodes re-opened if better path found |
| **Optimal?** | Yes – guaranteed optimal when heuristic is admissible |
| **Fast?** | Efficient with good heuristic |
| **Best Case** | Sparse grids where heuristic strongly guides toward goal |
| **Worst Case** | Dense mazes requiring near-exhaustive exploration |

### 📐 Heuristic Functions

| Heuristic | Formula | Use Case |
|---|---|---|
| **Manhattan Distance** | `h = |dx| + |dy|` | 4-directional grid movement |
| **Euclidean Distance** | `h = sqrt(dx^2 + dy^2)` | Free or diagonal movement |

> Both heuristics are **admissible** for 4-directional grids — they never overestimate the true cost.

---

## 💥 Dynamic Re-planning Logic

When **Dynamic Mode** is enabled:

| Step | What Happens |
|---|---|
| **1. Spawn** | New obstacles appear randomly every ~800ms while agent is moving |
| **2. Check** | Agent checks if any new obstacle blocks its remaining planned path |
| **3. Trigger** | If blocked, re-planning is triggered immediately |
| **4. Re-plan** | Algorithm re-runs from agent's current position to goal |
| **5. Optimize** | Only remaining path is recalculated – prior visited cells unchanged |

---

## 🎨 Color Legend

| Color | Meaning |
|---|---|
| **Green** | Final optimal path |
| **Yellow** | Frontier nodes (currently in priority queue) |
| **Indigo/Blue** | Visited / Expanded nodes |
| **Black** | Wall / Obstacle |
| **Blue cell** | Start node |
| **Red cell** | Goal node |
| **White dot** | Agent's current position |

---

AI 2002 – Artificial Intelligence
National University of Computer & Emerging Sciences
Chiniot-Faisalabad Campus
