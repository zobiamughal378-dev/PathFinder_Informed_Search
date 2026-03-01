"""
AI 2002 - Artificial Intelligence | Assignment 2 - Question 6
Dynamic Pathfinding Agent with GBFS and A* Search
Author: [Your Name] | Registration: [Your Reg No]

Requirements:  pip install pygame
Usage:         python pathfinding_agent.py
"""

import pygame, heapq, math, time, random
from collections import defaultdict

# ═══════════════════════════════════════════════
#  SIZING  — fixed window so panel never clips
# ═══════════════════════════════════════════════
ROWS       = 20
COLS       = 22
CELL_SIZE  = 26
PANEL_W    = 300
WIN_W      = COLS * CELL_SIZE + PANEL_W
WIN_H      = 680          # tall enough for all content
FPS        = 60
ANIM_DELAY = 25

# ═══════════════════════════════════════════════
#  COLOURS
# ═══════════════════════════════════════════════
BG         = (15,  15,  26)
GRID_LINE  = (36,  36,  54)
C_EMPTY    = (26,  26,  42)
C_WALL     = (58,  58,  78)
C_START    = (52, 211, 153)
C_GOAL     = (251,191,  36)
C_FRONTIER = (250,204,  21)
C_VISITED  = (99, 102, 241)
C_PATH     = (34, 197,  94)
C_TEXT     = (220,228,240)
C_SUBTEXT  = (130,145,165)
C_ACCENT   = (99, 102, 241)
C_BTN      = (40,  52,  72)
C_BTN_HOV  = (58,  72,  95)
C_BTN_ACT  = (76,  68, 225)
C_PANEL_BG = (12,  18,  36)
C_SUCCESS  = (52, 211, 153)
C_FAIL     = (239,  68,  68)
C_WARN     = (251,191,  36)
C_BORDER   = (48,  60,  82)
C_BOX      = (28,  38,  58)

# ═══════════════════════════════════════════════
#  COMPLEXITY INFO — updates live when algo changes
# ═══════════════════════════════════════════════
COMPLEXITY = {
    "A*": [
        ("Algorithm",   "A* Search"),
        ("Eval f(n)",   "g(n) + h(n)"),
        ("Optimal",     "YES  (admissible h)"),
        ("Complete",    "YES"),
        ("Time Best",   "O(b^d)"),
        ("Time Worst",  "O(b^d)  exponential"),
        ("Space",       "O(b^d)"),
        ("Strategy",    "Expands lowest f first"),
        ("Note",        "Optimal if h admissible.\nUses more memory than GBFS."),
    ],
    "GBFS": [
        ("Algorithm",   "Greedy Best-First"),
        ("Eval f(n)",   "h(n)  only  [no g]"),
        ("Optimal",     "NO"),
        ("Complete",    "YES  (visited list)"),
        ("Time Best",   "O(b x m)"),
        ("Time Worst",  "O(b^m)"),
        ("Space",       "O(b x m)"),
        ("Strategy",    "Expands lowest h first"),
        ("Note",        "Fast but not optimal.\nCan miss shorter paths."),
    ],
}

# ═══════════════════════════════════════════════
#  HEURISTICS
# ═══════════════════════════════════════════════
def manhattan(a, b): return abs(a[0]-b[0]) + abs(a[1]-b[1])
def euclidean(a, b): return math.hypot(a[0]-b[0], a[1]-b[1])

# ═══════════════════════════════════════════════
#  SEARCH
# ═══════════════════════════════════════════════
def _nbrs(pos, rows, cols, grid):
    r, c = pos
    for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
        nr, nc = r+dr, c+dc
        if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==0:
            yield (nr, nc)

def _rebuild(came, node):
    p=[]
    while node is not None: p.append(node); node=came[node]
    p.reverse(); return p

def gbfs(grid, start, goal, hfn):
    rows,cols=len(grid),len(grid[0]); tie=0
    heap=[(hfn(start,goal),tie,start)]; came={start:None}
    seen={start}; order=[]; exp=0
    while heap:
        _,_,cur=heapq.heappop(heap); order.append(cur); exp+=1
        if cur==goal: return _rebuild(came,goal),order,exp
        for nb in _nbrs(cur,rows,cols,grid):
            if nb not in seen:
                seen.add(nb); came[nb]=cur; tie+=1
                heapq.heappush(heap,(hfn(nb,goal),tie,nb))
    return None,order,exp

def astar(grid, start, goal, hfn):
    rows,cols=len(grid),len(grid[0])
    g=defaultdict(lambda:float('inf')); g[start]=0; tie=0
    heap=[(hfn(start,goal),tie,start)]; came={start:None}
    closed=set(); order=[]; exp=0
    while heap:
        _,_,cur=heapq.heappop(heap)
        if cur in closed: continue
        closed.add(cur); order.append(cur); exp+=1
        if cur==goal: return _rebuild(came,goal),order,exp
        for nb in _nbrs(cur,rows,cols,grid):
            if nb in closed: continue
            ng=g[cur]+1
            if ng<g[nb]:
                g[nb]=ng; came[nb]=cur; tie+=1
                heapq.heappush(heap,(ng+hfn(nb,goal),tie,nb))
    return None,order,exp

# ═══════════════════════════════════════════════
#  BUTTON
# ═══════════════════════════════════════════════
class Button:
    def __init__(self, rect, label, toggle=False, active=False):
        self.rect=pygame.Rect(rect); self.label=label
        self.toggle=toggle; self.active=active; self.hovered=False

    def draw(self, surf, font):
        col = C_BTN_ACT if (self.toggle and self.active) else (C_BTN_HOV if self.hovered else C_BTN)
        pygame.draw.rect(surf, col,      self.rect, border_radius=5)
        pygame.draw.rect(surf, C_BORDER, self.rect, 1, border_radius=5)
        t=font.render(self.label, True, C_TEXT)
        surf.blit(t, t.get_rect(center=self.rect.center))

    def handle(self, event):
        if event.type==pygame.MOUSEMOTION:
            self.hovered=self.rect.collidepoint(event.pos)
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if self.rect.collidepoint(event.pos):
                if self.toggle: self.active=not self.active
                return True
        return False

# ═══════════════════════════════════════════════
#  APP
# ═══════════════════════════════════════════════
class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Dynamic Pathfinding Agent  |  AI 2002 – Assignment 2  Q6")
        self.clock  = pygame.time.Clock()

        # fonts
        self.f_xs  = pygame.font.SysFont("Segoe UI", 11)
        self.f_sm  = pygame.font.SysFont("Segoe UI", 12)
        self.f_md  = pygame.font.SysFont("Segoe UI", 13)
        self.f_btn = pygame.font.SysFont("Segoe UI", 13, bold=True)
        self.f_hdr = pygame.font.SysFont("Segoe UI", 14, bold=True)

        self.rows, self.cols = ROWS, COLS
        self.grid  = [[0]*self.cols for _ in range(self.rows)]
        self.start = (0, 0)
        self.goal  = (self.rows-1, self.cols-1)

        self.algo      = "A*"
        self.hname     = "Manhattan"
        self.placing   = "wall"
        self.path      = []
        self.visited   = []
        self.anim_idx  = 0
        self.animating = False
        self.dynamic   = False
        self.agent_pos = None
        self.agent_idx = 0
        self.metrics   = dict(nodes=0, cost=0, ms=0.0, status="Ready")
        self.dyn_obs   = set()

        self._build_ui()
        self.generate_maze()

    # ── build UI  (all Y are absolute screen coords) ──
    def _build_ui(self):
        gx = COLS * CELL_SIZE
        P  = 8
        W  = PANEL_W - P*2
        H2 = (W-6)//2
        H3 = (W-8)//3

        def B(xo,y,w,h,lbl,tog=False,act=False):
            return Button((gx+P+xo, y, w, h), lbl, toggle=tog, active=act)

        # ── buttons (Y positions chosen so nothing overlaps) ──
        self.btn_gbfs  = B(0,     8,  H2, 28, "GBFS",         tog=True, act=False)
        self.btn_astar = B(H2+6,  8,  H2, 28, "A* Search",    tog=True, act=True)

        self.btn_manh  = B(0,     44, H2, 28, "Manhattan",    tog=True, act=True)
        self.btn_eucl  = B(H2+6,  44, H2, 28, "Euclidean",    tog=True, act=False)

        self.btn_wall  = B(0,        78, H3, 26, "Wall",  tog=True, act=True)
        self.btn_start = B(H3+4,     78, H3, 26, "Start", tog=True, act=False)
        self.btn_goal  = B((H3+4)*2, 78, H3, 26, "Goal",  tog=True, act=False)

        self.btn_run    = B(0,    112, W,  32, "▶  Run Search")
        self.btn_clear  = B(0,    152, H2, 26, "Clear Path")
        self.btn_reset  = B(H2+6, 152, H2, 26, "Reset Grid")
        self.btn_gen    = B(0,    186, W,  26, "Generate Maze")
        self.btn_dyn    = B(0,    220, W,  26, "Dynamic Mode: OFF", tog=True, act=False)
        self.btn_step   = B(0,    254, H2, 26, "Step Fwd")
        self.btn_replay = B(H2+6, 254, H2, 26, "Replay")

        self.all_buttons = [
            self.btn_gbfs, self.btn_astar,
            self.btn_manh, self.btn_eucl,
            self.btn_wall, self.btn_start, self.btn_goal,
            self.btn_run,  self.btn_clear, self.btn_reset,
            self.btn_gen,  self.btn_dyn,   self.btn_step, self.btn_replay,
        ]

    # ── helpers ──────────────────────────────
    def hfn(self): return manhattan if self.hname=="Manhattan" else euclidean

    def cell_at(self, mx, my):
        c,r = mx//CELL_SIZE, my//CELL_SIZE
        if 0<=r<self.rows and 0<=c<self.cols: return (r,c)
        return None

    def generate_maze(self, density=0.27):
        self.grid=[[0]*self.cols for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                if (r,c) not in (self.start,self.goal):
                    self.grid[r][c]=1 if random.random()<density else 0
        self.reset_search(); self.dyn_obs.clear()

    def reset_search(self):
        self.path=[]; self.visited=[]
        self.anim_idx=0; self.animating=False
        self.agent_pos=None; self.agent_idx=0
        self.metrics=dict(nodes=0,cost=0,ms=0.0,status="Ready")

    def run_search(self):
        self.reset_search()
        fn = gbfs if self.algo=="GBFS" else astar
        t0 = time.perf_counter()
        path,vis,nodes = fn(self.grid, self.start, self.goal, self.hfn())
        ms = round((time.perf_counter()-t0)*1000, 3)
        self.visited=vis; self.path=path or []
        self.metrics=dict(
            nodes=nodes,
            cost=len(self.path)-1 if self.path else 0,
            ms=ms,
            status="Path Found!" if path else "No Path Found",
        )
        self.animating=True
        if self.path: self.agent_pos=self.start; self.agent_idx=0

    def spawn_dynamic_obstacle(self):
        if not self.path: return
        cands=[(r,c) for r in range(self.rows) for c in range(self.cols)
               if self.grid[r][c]==0 and (r,c) not in (self.start,self.goal)
               and (r,c) not in self.path[:self.agent_idx+1]]
        if not cands: return
        cell=random.choice(cands)
        self.grid[cell[0]][cell[1]]=1; self.dyn_obs.add(cell)
        if cell in set(self.path[self.agent_idx:]):
            cur=self.path[self.agent_idx]
            fn=gbfs if self.algo=="GBFS" else astar
            np_,_,_=fn(self.grid,cur,self.goal,self.hfn())
            if np_:
                self.path=self.path[:self.agent_idx]+np_
                self.metrics["status"]="Re-planned!"
            else:
                self.metrics["status"]="Path Blocked!"

    # ── draw grid ────────────────────────────
    def draw_grid(self):
        vis_set  = set(self.visited[:self.anim_idx])
        show_path= not self.animating or self.anim_idx>=len(self.visited)
        path_set = set(self.path) if show_path else set()
        for r in range(self.rows):
            for c in range(self.cols):
                pos=(r,c)
                if   self.grid[r][c]==1:                                   col=C_WALL
                elif pos==self.start:                                       col=C_START
                elif pos==self.goal:                                        col=C_GOAL
                elif pos in path_set and pos not in (self.start,self.goal): col=C_PATH
                elif pos in vis_set:                                        col=C_VISITED
                else:                                                       col=C_EMPTY
                pygame.draw.rect(self.screen,col,
                    (c*CELL_SIZE+1,r*CELL_SIZE+1,CELL_SIZE-2,CELL_SIZE-2),border_radius=2)
        if self.agent_pos:
            r,c=self.agent_pos
            cx,cy=c*CELL_SIZE+CELL_SIZE//2,r*CELL_SIZE+CELL_SIZE//2
            pygame.draw.circle(self.screen,(255,255,255),(cx,cy),CELL_SIZE//3)
            pygame.draw.circle(self.screen,C_START,(cx,cy),CELL_SIZE//3-3)
        for r in range(self.rows+1):
            pygame.draw.line(self.screen,GRID_LINE,(0,r*CELL_SIZE),(COLS*CELL_SIZE,r*CELL_SIZE))
        for c in range(self.cols+1):
            pygame.draw.line(self.screen,GRID_LINE,(c*CELL_SIZE,0),(c*CELL_SIZE,ROWS*CELL_SIZE))

    # ── draw panel ───────────────────────────
    def draw_panel(self):
        gx = COLS*CELL_SIZE
        P  = 8
        W  = PANEL_W - P*2
        tx = gx+P

        # background
        pygame.draw.rect(self.screen, C_PANEL_BG, (gx,0,PANEL_W,WIN_H))
        pygame.draw.line(self.screen, C_BORDER,   (gx,0),(gx,WIN_H), 2)

        # micro section labels (above each button row)
        for y,lbl in [(0,"ALGORITHM"),(36,"HEURISTIC"),(70,"PLACEMENT MODE")]:
            self.screen.blit(self.f_xs.render(lbl,True,C_SUBTEXT),(tx,y))

        # all buttons
        for btn in self.all_buttons:
            btn.draw(self.screen, self.f_btn)

        # ────────────────────────────────────────
        #  METRICS BOX  y=288
        # ────────────────────────────────────────
        MY, MH = 288, 122
        pygame.draw.rect(self.screen,C_BOX,   (gx+P,MY,W,MH),border_radius=7)
        pygame.draw.rect(self.screen,C_BORDER,(gx+P,MY,W,MH),1,border_radius=7)
        self.screen.blit(self.f_hdr.render("Metrics",True,C_ACCENT),(tx+4,MY+5))

        st=self.metrics["status"]
        sc=(C_SUCCESS if "Found"   in st else
            C_FAIL    if ("No Path" in st or "Blocked" in st) else
            C_WARN    if "Re-plan" in st else C_SUBTEXT)

        mdata=[
            ("Status",    st,                              sc),
            ("Algorithm", f"{self.algo}  ({self.hname})",  C_TEXT),
            ("Nodes",     str(self.metrics["nodes"]),       C_TEXT),
            ("Path Cost", f"{self.metrics['cost']} steps",  C_TEXT),
            ("Exec Time", f"{self.metrics['ms']} ms",       C_TEXT),
        ]
        for i,(lbl,val,col) in enumerate(mdata):
            y=MY+24+i*19
            self.screen.blit(self.f_sm.render(lbl+":",True,C_SUBTEXT),(tx+4,y))
            self.screen.blit(self.f_md.render(val,True,col),(tx+88,y))

        # ────────────────────────────────────────
        #  COMPLEXITY BOX  — live update on algo switch
        # ────────────────────────────────────────
        CY = MY+MH+6
        CH = WIN_H-CY-36          # leaves 36 px for legend at bottom
        pygame.draw.rect(self.screen,C_BOX,   (gx+P,CY,W,CH),border_radius=7)
        pygame.draw.rect(self.screen,C_BORDER,(gx+P,CY,W,CH),1,border_radius=7)

        # header
        self.screen.blit(self.f_hdr.render("Complexity Analysis",True,C_ACCENT),(tx+4,CY+5))
        # algo name badge
        badge=self.f_btn.render(f"[ {self.algo} ]",True,C_WARN)
        self.screen.blit(badge,(gx+P+W-badge.get_width()-6,CY+5))
        # divider
        pygame.draw.line(self.screen,C_BORDER,(gx+P+4,CY+22),(gx+P+W-4,CY+22))

        info=COMPLEXITY[self.algo]
        cy=CY+26
        for lbl,val in info:
            if lbl=="Note":
                # draw note with word wrap in remaining space
                pygame.draw.line(self.screen,C_BORDER,(gx+P+4,cy-1),(gx+P+W-4,cy-1))
                cy+=3
                for line in val.split('\n'):
                    t=self.f_xs.render(line,True,C_SUBTEXT)
                    self.screen.blit(t,(tx+4,cy)); cy+=14
                break

            # colour coding
            if   lbl=="Optimal":  vc=C_SUCCESS if "YES" in val else C_FAIL
            elif lbl=="Complete": vc=C_SUCCESS
            elif lbl=="Eval f(n)":vc=C_WARN
            else:                 vc=C_TEXT

            self.screen.blit(self.f_xs.render(lbl+":",True,C_SUBTEXT),(tx+4,cy))
            self.screen.blit(self.f_sm.render(val,True,vc),(tx+88,cy))
            cy+=18

        # ────────────────────────────────────────
        #  LEGEND  (bottom 36 px)
        # ────────────────────────────────────────
        LY=WIN_H-26
        legend=[(C_START,"Start"),(C_GOAL,"Goal"),(C_PATH,"Path"),
                (C_VISITED,"Visited"),(C_FRONTIER,"Frontier"),(C_WALL,"Wall")]
        lx=tx
        for col,lbl in legend:
            pygame.draw.rect(self.screen,col,(lx,LY+4,10,10),border_radius=2)
            t=self.f_xs.render(lbl,True,C_SUBTEXT)
            self.screen.blit(t,(lx+13,LY+3))
            lx+=t.get_width()+22

    # ── events ───────────────────────────────
    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: return False
            for btn in self.all_buttons:
                if btn.handle(ev): self._on_button(btn)
            if ev.type in (pygame.MOUSEBUTTONDOWN,pygame.MOUSEMOTION):
                if pygame.mouse.get_pressed()[0]:
                    cell=self.cell_at(*pygame.mouse.get_pos())
                    if cell: self._place(cell)
        return True

    def _on_button(self,b):
        if   b is self.btn_gbfs:  self.algo="GBFS"; self.btn_gbfs.active=True;  self.btn_astar.active=False
        elif b is self.btn_astar: self.algo="A*";   self.btn_astar.active=True; self.btn_gbfs.active=False
        elif b is self.btn_manh:  self.hname="Manhattan"; self.btn_manh.active=True;  self.btn_eucl.active=False
        elif b is self.btn_eucl:  self.hname="Euclidean"; self.btn_eucl.active=True;  self.btn_manh.active=False
        elif b is self.btn_wall:  self.placing="wall";  self.btn_wall.active=True;  self.btn_start.active=False; self.btn_goal.active=False
        elif b is self.btn_start: self.placing="start"; self.btn_start.active=True; self.btn_wall.active=False;  self.btn_goal.active=False
        elif b is self.btn_goal:  self.placing="goal";  self.btn_goal.active=True;  self.btn_wall.active=False;  self.btn_start.active=False
        elif b is self.btn_run:    self.run_search()
        elif b is self.btn_clear:  self.reset_search()
        elif b is self.btn_reset:
            self.grid=[[0]*self.cols for _ in range(self.rows)]; self.dyn_obs.clear(); self.reset_search()
        elif b is self.btn_gen:    self.generate_maze()
        elif b is self.btn_dyn:
            self.dynamic=self.btn_dyn.active
            self.btn_dyn.label=f"Dynamic Mode: {'ON' if self.dynamic else 'OFF'}"
        elif b is self.btn_step:
            if self.anim_idx<len(self.visited): self.anim_idx+=1
        elif b is self.btn_replay:
            if self.path: self.anim_idx=0; self.animating=True; self.agent_idx=0; self.agent_pos=self.start

    def _place(self,cell):
        r,c=cell
        if   self.placing=="wall"  and cell not in (self.start,self.goal):
            self.grid[r][c]=1-self.grid[r][c]; self.reset_search()
        elif self.placing=="start":
            self.grid[self.start[0]][self.start[1]]=0; self.start=cell; self.grid[r][c]=0; self.reset_search()
        elif self.placing=="goal":
            self.goal=cell; self.grid[r][c]=0; self.reset_search()

    # ── main loop ────────────────────────────
    def run(self):
        at=dt2=0
        while True:
            dt=self.clock.tick(FPS)
            if not self.handle_events(): break
            at+=dt
            if self.animating and at>=ANIM_DELAY:
                at=0
                if self.anim_idx<len(self.visited):
                    self.anim_idx+=1
                else:
                    if self.path and self.agent_idx<len(self.path)-1:
                        self.agent_idx+=1; self.agent_pos=self.path[self.agent_idx]
                    if self.agent_idx>=len(self.path)-1:
                        self.animating=False
            if self.dynamic and self.animating:
                dt2+=dt
                if dt2>=900: dt2=0; random.random()<0.55 and self.spawn_dynamic_obstacle()
            self.screen.fill(BG)
            self.draw_grid()
            self.draw_panel()
            pygame.display.flip()
        pygame.quit()

if __name__=="__main__":
    App().run()