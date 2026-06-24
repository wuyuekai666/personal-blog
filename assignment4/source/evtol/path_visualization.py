from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from .path_planning import PlannerResult, make_obstacle_mask


def _add_heatmap(
    fig: go.Figure,
    field: np.ndarray,
    name: str,
    colorscale: str,
    opacity: float,
    colorbar_x: float,
    colorbar_y: float,
) -> None:
    axis = np.linspace(0.0, 100.0, field.shape[0])
    fig.add_trace(
        go.Contour(
            x=axis,
            y=axis,
            z=field,
            name=name,
            colorscale=colorscale,
            opacity=opacity,
            contours=dict(showlines=False),
            colorbar=dict(
                title=dict(text=name, side="top"),
                len=0.30,
                thickness=18,
                x=colorbar_x,
                y=colorbar_y,
                xpad=12,
                ypad=8,
            ),
            hovertemplate=f"{name}: %{{z:.3f}}<extra></extra>",
        )
    )


def _add_obstacles(fig: go.Figure, risk_field: np.ndarray, obstacle_threshold: float) -> None:
    mask = make_obstacle_mask(risk_field, obstacle_threshold, 0).astype(float)
    axis = np.linspace(0.0, 100.0, mask.shape[0])
    fig.add_trace(
        go.Contour(
            x=axis,
            y=axis,
            z=mask,
            name="障碍/禁飞区域",
            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(20,20,20,0.72)"]],
            showscale=False,
            contours=dict(start=0.5, end=1.0, size=0.5, showlines=False),
            hoverinfo="skip",
        )
    )


def _add_selected_sites(
    fig: go.Figure,
    selected_sites: pd.DataFrame,
    start_id: int,
    airport: tuple[float, float],
) -> None:
    other = selected_sites[selected_sites["candidate_id"] != start_id]
    if len(other):
        fig.add_trace(
            go.Scatter(
                x=other["x"],
                y=other["y"],
                mode="markers+text",
                text=other["candidate_id"],
                textposition="top center",
                name="其他客户起降点",
                marker=dict(symbol="star", size=15, color="#64748b", line=dict(color="white", width=1)),
            )
        )

    start_row = selected_sites[selected_sites["candidate_id"] == start_id]
    if len(start_row):
        fig.add_trace(
            go.Scatter(
                x=start_row["x"],
                y=start_row["y"],
                mode="markers+text",
                text=["起点"],
                textposition="top center",
                name="当前起点",
                marker=dict(symbol="circle", size=18, color="#16a34a", line=dict(color="white", width=2)),
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[airport[0]],
            y=[airport[1]],
            mode="markers+text",
            text=["机场"],
            textposition="top center",
            name="机场接驳终点",
            marker=dict(symbol="diamond", size=20, color="#dc2626", line=dict(color="white", width=2)),
        )
    )


def _add_astar_trace(fig: go.Figure, result: PlannerResult, frame_fraction: float) -> None:
    explored_count = max(1, int(len(result.explored) * frame_fraction))
    frontier_count = max(1, int(len(result.frontier) * frame_fraction))
    explored = result.explored[:explored_count]
    frontier = result.frontier[:frontier_count]

    if explored:
        xs, ys = zip(*explored)
        fig.add_trace(
            go.Scattergl(
                x=xs,
                y=ys,
                mode="markers",
                name="A* 已探索 closed list",
                marker=dict(size=4, color="rgba(59,130,246,0.35)"),
            )
        )
    if frontier:
        xs, ys = zip(*frontier)
        fig.add_trace(
            go.Scattergl(
                x=xs,
                y=ys,
                mode="markers",
                name="A* 搜索边界 open list",
                marker=dict(size=4, color="rgba(245,158,11,0.45)"),
            )
        )


def _add_rrt_trace(fig: go.Figure, result: PlannerResult, frame_fraction: float) -> None:
    edge_count = max(1, int(len(result.tree_edges) * frame_fraction))
    sample_count = max(1, int(len(result.samples) * frame_fraction))
    edges = result.tree_edges[:edge_count]
    samples = result.samples[:sample_count]

    if samples:
        xs, ys = zip(*samples)
        fig.add_trace(
            go.Scattergl(
                x=xs,
                y=ys,
                mode="markers",
                name="RRT* 随机采样点",
                marker=dict(size=4, color="rgba(148,163,184,0.35)"),
            )
        )

    if edges:
        xs: list[float | None] = []
        ys: list[float | None] = []
        for a, b in edges:
            xs.extend([a[0], b[0], None])
            ys.extend([a[1], b[1], None])
        fig.add_trace(
            go.Scattergl(
                x=xs,
                y=ys,
                mode="lines",
                name="RRT* 搜索树",
                line=dict(color="rgba(37,99,235,0.35)", width=1),
            )
        )


def _add_path(fig: go.Figure, path: list[tuple[float, float]], name: str, color: str) -> None:
    if len(path) < 2:
        return
    xs, ys = zip(*path)
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="lines+markers",
            name=name,
            line=dict(color=color, width=5),
            marker=dict(size=6, color=color),
        )
    )


def build_path_figure(
    risk_field: np.ndarray,
    cost_field: np.ndarray,
    selected_sites: pd.DataFrame,
    start_id: int,
    airport: tuple[float, float],
    obstacle_threshold: float,
    result: PlannerResult | None = None,
    comparison_result: PlannerResult | None = None,
    frame_fraction: float = 1.0,
) -> go.Figure:
    fig = go.Figure()
    _add_heatmap(fig, cost_field, "成本场", "Greens", 0.22, 1.03, 0.77)
    _add_heatmap(fig, risk_field, "风险场", "YlOrRd", 0.45, 1.03, 0.28)
    _add_obstacles(fig, risk_field, obstacle_threshold)
    _add_selected_sites(fig, selected_sites, start_id, airport)

    if result is not None:
        if result.algorithm == "A*":
            _add_astar_trace(fig, result, frame_fraction)
            _add_path(fig, result.path, "A* 最终路径", "#7c3aed")
        elif result.algorithm == "RRT*":
            _add_rrt_trace(fig, result, frame_fraction)
            _add_path(fig, result.path, "RRT* 最终路径", "#0891b2")

    if comparison_result is not None:
        if comparison_result.algorithm == "A*":
            _add_path(fig, comparison_result.path, "A* 对比路径", "#7c3aed")
        elif comparison_result.algorithm == "RRT*":
            _add_path(fig, comparison_result.path, "RRT* 对比路径", "#0891b2")

    fig.update_layout(
        title="路径规划动态可视化",
        height=720,
        margin=dict(l=20, r=90, t=55, b=20),
        legend=dict(orientation="h", y=1.01, x=0.0),
        font=dict(family="Microsoft YaHei, SimHei, Arial", size=13),
    )
    fig.update_xaxes(title="X 坐标", range=[0, 100], constrain="domain")
    fig.update_yaxes(title="Y 坐标", range=[0, 100], scaleanchor="x", scaleratio=1)
    return fig


def build_comparison_bar(metrics_df: pd.DataFrame) -> go.Figure:
    shown = metrics_df.copy()
    rename = {
        "path_length": "路径长度",
        "cumulative_risk": "累计风险",
        "cumulative_cost": "累计成本",
        "runtime_s": "计算时间",
        "turn_count": "转折次数",
        "tortuosity": "曲折度",
    }
    long_df = shown.melt(id_vars=["algorithm"], value_vars=list(rename.keys()), var_name="metric", value_name="value")
    long_df["metric"] = long_df["metric"].map(rename)

    fig = go.Figure()
    for algo in long_df["algorithm"].unique():
        part = long_df[long_df["algorithm"] == algo]
        fig.add_trace(go.Bar(x=part["metric"], y=part["value"], name=algo))

    fig.update_layout(
        title="A* 与 RRT* 量化指标对比",
        barmode="group",
        height=380,
        yaxis_title="指标值",
        font=dict(family="Microsoft YaHei, SimHei, Arial", size=13),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig
