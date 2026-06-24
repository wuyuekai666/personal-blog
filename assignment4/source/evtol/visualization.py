from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def _base_layout(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title=title,
        height=720,
        margin=dict(l=20, r=90, t=58, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0.0),
        font=dict(family="Microsoft YaHei, SimHei, Arial", size=13),
    )
    fig.update_xaxes(title="X 坐标", range=[0, 100], constrain="domain")
    fig.update_yaxes(title="Y 坐标", range=[0, 100], scaleanchor="x", scaleratio=1)
    return fig


def add_field_heatmap(
    fig: go.Figure,
    xx,
    yy,
    field,
    name: str,
    colorscale: str,
    opacity: float,
    colorbar_x: float,
    colorbar_y: float,
) -> None:
    fig.add_trace(
        go.Contour(
            x=xx[0],
            y=yy[:, 0],
            z=field,
            name=name,
            colorscale=colorscale,
            opacity=opacity,
            showscale=True,
            colorbar=dict(
                title=dict(text=name, side="top"),
                len=0.34,
                thickness=18,
                x=colorbar_x,
                y=colorbar_y,
                xpad=12,
                ypad=8,
            ),
            contours=dict(showlines=False),
            hovertemplate=f"{name}: %{{z:.3f}}<extra></extra>",
        )
    )


def add_demand_points(fig: go.Figure, demand_df: pd.DataFrame, colored_by_cluster: bool = False) -> None:
    marker = dict(
        size=6 + demand_df["demand_weight"] * 2.5,
        opacity=0.82,
        line=dict(width=0.5, color="#25313f"),
    )
    if colored_by_cluster and "cluster" in demand_df.columns:
        marker.update(color=demand_df["cluster"], colorscale="Turbo", showscale=False)
        name = "需求点（按聚类着色）"
    else:
        marker.update(
            color=demand_df["demand_weight"],
            colorscale="YlGnBu",
            showscale=True,
            colorbar=dict(
                title=dict(text="需求权重", side="top"),
                len=0.25,
                thickness=18,
                x=1.03,
                y=0.82,
                xpad=12,
                ypad=8,
            ),
        )
        name = "需求点（大小/颜色=需求）"

    fig.add_trace(
        go.Scatter(
            x=demand_df["x"],
            y=demand_df["y"],
            mode="markers",
            name=name,
            marker=marker,
            customdata=demand_df[["id", "demand_weight"]].round(3),
            hovertemplate="需求点 #%{customdata[0]}<br>x=%{x:.2f}<br>y=%{y:.2f}<br>需求权重=%{customdata[1]:.2f}<extra></extra>",
        )
    )


def add_assignment_lines(fig: go.Figure, demand_df: pd.DataFrame, candidates: pd.DataFrame) -> None:
    if "cluster" not in demand_df.columns:
        return
    xs: list[float | None] = []
    ys: list[float | None] = []
    for _, row in demand_df.iterrows():
        center = candidates.loc[int(row["cluster"])]
        xs.extend([row["x"], center["x"], None])
        ys.extend([row["y"], center["y"], None])
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="lines",
            name="需求-候选点归属",
            line=dict(color="rgba(80,80,80,0.22)", width=1),
            hoverinfo="skip",
        )
    )


def add_candidates(fig: go.Figure, candidates: pd.DataFrame, selected_ids: set[int] | None = None) -> None:
    selected_ids = selected_ids or set()
    unselected = candidates[~candidates["candidate_id"].isin(selected_ids)]
    if len(unselected):
        fig.add_trace(
            go.Scatter(
                x=unselected["x"],
                y=unselected["y"],
                mode="markers+text",
                name="候选起降点",
                text=unselected["candidate_id"],
                textposition="top center",
                marker=dict(symbol="circle", size=14, color="#2563eb", line=dict(width=2, color="white")),
                hovertemplate="候选点 #%{text}<br>x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>",
            )
        )

    selected = candidates[candidates["candidate_id"].isin(selected_ids)]
    if len(selected):
        hover_cols = ["candidate_id", "coverage", "risk", "cost", "single_score"]
        customdata = selected[hover_cols].round(4)
        fig.add_trace(
            go.Scatter(
                x=selected["x"],
                y=selected["y"],
                mode="markers+text",
                name="GA 最终选址",
                text=selected["candidate_id"],
                textposition="top center",
                marker=dict(symbol="star", size=23, color="#dc2626", line=dict(width=2, color="white")),
                customdata=customdata,
                hovertemplate=(
                    "最终点 #%{customdata[0]}<br>x=%{x:.2f}<br>y=%{y:.2f}"
                    "<br>覆盖需求=%{customdata[1]:.2f}<br>风险=%{customdata[2]:.3f}"
                    "<br>成本=%{customdata[3]:.3f}<br>单点评分=%{customdata[4]:.3f}<extra></extra>"
                ),
            )
        )


def build_scene_figure(
    title: str,
    demand_df: pd.DataFrame,
    candidates: pd.DataFrame | None = None,
    selected_ids: set[int] | None = None,
    xx=None,
    yy=None,
    risk=None,
    cost=None,
    show_risk: bool = False,
    show_cost: bool = False,
    show_demand: bool = True,
    show_clusters: bool = False,
    show_lines: bool = False,
) -> go.Figure:
    fig = go.Figure()
    if show_cost and cost is not None:
        add_field_heatmap(fig, xx, yy, cost, "成本场", "Greens", 0.38, 1.03, 0.51)
    if show_risk and risk is not None:
        add_field_heatmap(fig, xx, yy, risk, "风险场", "YlOrRd", 0.48, 1.03, 0.18)

    if candidates is not None and show_lines:
        add_assignment_lines(fig, demand_df, candidates)
    if show_demand:
        add_demand_points(fig, demand_df, colored_by_cluster=show_clusters)
    if candidates is not None:
        add_candidates(fig, candidates, selected_ids)

    return _base_layout(fig, title)


def build_convergence_figure(history: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=history["generation"],
            y=history["best_fitness"],
            mode="lines",
            name="历史最优适应度",
            line=dict(color="#dc2626", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=history["generation"],
            y=history["mean_fitness"],
            mode="lines",
            name="种群平均适应度",
            line=dict(color="#2563eb", width=2, dash="dot"),
        )
    )
    fig.update_layout(
        title="GA 收敛曲线",
        height=350,
        xaxis_title="迭代代数",
        yaxis_title="适应度",
        font=dict(family="Microsoft YaHei, SimHei, Arial", size=13),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig
