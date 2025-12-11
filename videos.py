#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import gurobipy as gp
from gurobipy import GRB



def read_dataset(path):
    print("[INFO] Reading dataset:", path)

    with open(path, "r") as f:
        first = f.readline().split()
        V, E, R, C, X = map(int, first)

        video_sizes = list(map(int, f.readline().split()))

        endpoints = []
        for e in range(E):
            lat_dc, K = map(int, f.readline().split())
            cache_latencies = {}
            for _ in range(K):
                cid, lat = map(int, f.readline().split())
                cache_latencies[cid] = lat
            endpoints.append((lat_dc, cache_latencies))

        requests = []
        for _ in range(R):
            v, e, n = map(int, f.readline().split())
            requests.append((v, e, n))

    print("[INFO] Dataset loaded.")
    return V, E, R, C, X, video_sizes, endpoints, requests



def build_model(V, E, R, C, X, video_sizes, endpoints, requests):
    print("[INFO] Building Gurobi model...")

    model = gp.Model("videos")


    model.Params.OutputFlag = 1
    model.Params.MIPGap = 0.005         # <= 0.5% as required
    model.Params.NumericFocus = 1       # stabilize objective coefficients
    model.Params.Presolve = 2           # aggressive presolve
    model.Params.MIPFocus = 1           # focus on improving the bound


    x = model.addVars(V, C, vtype=GRB.BINARY, name="x")   # video stored in cache
    y = model.addVars(R, C, vtype=GRB.BINARY, name="y")   # request served by cache


    obj = gp.LinExpr()

    for r in range(R):
        v, e, n = requests[r]
        lat_dc, caches = endpoints[e]

        for c, lat_cache in caches.items():
            saving = lat_dc - lat_cache
            if saving > 0:
                obj += n * saving * y[r, c]

    model.setObjective(obj, GRB.MAXIMIZE)


    for c in range(C):
        model.addConstr(
            gp.quicksum(video_sizes[v] * x[v, c] for v in range(V)) <= X,
            name=f"capacity_{c}"
        )


    for r in range(R):
        v, e, n = requests[r]
        lat_dc, caches = endpoints[e]

        model.addConstr(
            gp.quicksum(y[r, c] for c in caches.keys()) <= 1,
            name=f"assign_{r}"
        )

    # y <= x
    for r in range(R):
        v, e, n = requests[r]
        lat_dc, caches = endpoints[e]
        for c in caches.keys():
            model.addConstr(
                y[r, c] <= x[v, c],
                name=f"link_r{r}_c{c}"
            )

    print("[INFO] Model ready.")
    return model, x


# ----------------------------------------------------------------------
# WRITE videos.out (HashCode format)
# ----------------------------------------------------------------------
def write_solution(V, C, x, outfile="videos.out"):
    print("[INFO] Writing solution file:", outfile)

    with open(outfile, "w") as f:
        used = []
        for c in range(C):
            videos_in_cache = [v for v in range(V) if x[v, c].X > 0.5]
            if videos_in_cache:
                used.append((c, videos_in_cache))

        f.write(str(len(used)) + "\n")
        for c, vids in used:
            f.write(str(c) + " " + " ".join(map(str, vids)) + "\n")

    print("[INFO] videos.out created.")


# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------
def main():
    if len(sys.argv) != 2:
        print("Usage: python videos.py path/to/dataset")
        sys.exit(1)

    dataset_path = sys.argv[1]


    if os.path.exists("videos.out"):
        os.remove("videos.out")


    V, E, R, C, X, video_sizes, endpoints, requests = read_dataset(dataset_path)


    model, x = build_model(V, E, R, C, X, video_sizes, endpoints, requests)


    print("[INFO] Exporting videos.mps...")
    model.write("videos.mps")


    print("[INFO] Solving model...")
    model.optimize()

    if model.status == GRB.INFEASIBLE:
        print("[ERROR] Model infeasible. Writing empty videos.out")
        open("videos.out", "w").write("0\n")
        return


    write_solution(V, C, x)


if __name__ == "__main__":
    main()
