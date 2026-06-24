from __future__ import annotations

import pandas as pd
import streamlit as st

from evtol.clustering import run_kmeans
from evtol.fields import cost_grid, create_risk_hotspots, risk_grid
from evtol.ga import GAConfig, run_ga
from evtol.path_analysis import metrics_to_frame
from evtol.path_planning import AStarConfig, RRTStarConfig, run_astar, run_rrtstar
from evtol.path_visualization import build_comparison_bar, build_path_figure
from evtol.scene import DemandConfig, generate_demand_points, make_grid
from evtol.visualization import build_convergence_figure, build_scene_figure


st.set_page_config(
    page_title="二维平面 eVTOL 起降点选址与路径规划",
    page_icon="",
    layout="wide",
)


AIRPORT_POINT = (92.0, 12.0)


def csv_download(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")


@st.cache_data(show_spinner=False)
def compute_pipeline(params: dict):
    demand = generate_demand_points(
        DemandConfig(
            num_points=params["num_points"],
            seed=params["seed"],
            weight_min=params["weight_min"],
            weight_max=params["weight_max"],
            hotspot_count=params["demand_hotspots"],
            hotspot_spread=params["demand_spread"],
        )
    )

    clustered, candidates = run_kmeans(demand, params["cluster_count"], params["seed"])
    hotspots = create_risk_hotspots(
        count=params["risk_hotspots"],
        intensity=params["risk_intensity"],
        seed=params["seed"],
    )
    xx, yy = make_grid(params["grid_size"])
    risk = risk_grid(xx, yy, hotspots)
    cost = cost_grid(xx, yy, params["cost_mode"])

    ga_result = run_ga(
        candidates=candidates,
        demand=clustered,
        hotspots=hotspots,
        cost_mode=params["cost_mode"],
        config=GAConfig(
            selected_count=params["selected_count"],
            population_size=params["population_size"],
            generations=params["generations"],
            crossover_prob=params["crossover_prob"],
            mutation_prob=params["mutation_prob"],
            w_demand=params["w_demand"],
            w_risk=params["w_risk"],
            w_cost=params["w_cost"],
            service_radius=params["service_radius"],
            seed=params["seed"],
        ),
    )

    metrics = ga_result.candidate_metrics.copy()
    selected_ids = set(metrics.iloc[ga_result.best_indices]["candidate_id"].astype(int).tolist())
    metrics["is_selected"] = metrics["candidate_id"].isin(selected_ids)
    return clustered, metrics, hotspots, xx, yy, risk, cost, ga_result, selected_ids


def build_sidebar() -> dict:
    st.sidebar.title("参数设置")
    st.sidebar.caption("调整参数后，系统会重新生成选址结果，路径规划模块会自动复用这些结果。")

    if "scenario_shift" not in st.session_state:
        st.session_state.scenario_shift = 0

    if st.sidebar.button("切换随机场景", use_container_width=True):
        st.session_state.scenario_shift += 1
        st.session_state.pop("planner_results", None)

    st.sidebar.subheader("需求点")
    seed = st.sidebar.number_input("随机种子", min_value=0, max_value=999999, value=42, step=1)
    num_points = st.sidebar.slider("需求点数量", 30, 500, 180, 10)
    weight_min, weight_max = st.sidebar.slider("需求权重范围", 0.1, 10.0, (1.0, 5.0), 0.1)
    demand_hotspots = st.sidebar.slider("需求热点数量", 1, 8, 4, 1)
    demand_spread = st.sidebar.slider("需求热点离散程度", 3.0, 24.0, 10.0, 1.0)

    st.sidebar.subheader("K-means")
    cluster_count = st.sidebar.slider("聚类数 K / 候选点数量", 3, 40, 14, 1)

    st.sidebar.subheader("GA 优化")
    selected_count = st.sidebar.slider("最终选址数量", 1, min(12, cluster_count), min(5, cluster_count), 1)
    population_size = st.sidebar.slider("种群规模", 10, 200, 70, 5)
    generations = st.sidebar.slider("最大迭代次数", 10, 300, 100, 10)
    crossover_prob = st.sidebar.slider("交叉概率", 0.0, 1.0, 0.85, 0.05)
    mutation_prob = st.sidebar.slider("变异概率", 0.0, 0.5, 0.06, 0.01)
    service_radius = st.sidebar.slider("服务覆盖半径", 5.0, 35.0, 18.0, 1.0)

    st.sidebar.subheader("选址目标函数权重")
    w_demand = st.sidebar.slider("需求覆盖权重 w1", 0.0, 5.0, 2.0, 0.1)
    w_risk = st.sidebar.slider("风险惩罚权重 w2", 0.0, 5.0, 1.0, 0.1)
    w_cost = st.sidebar.slider("成本惩罚权重 w3", 0.0, 5.0, 0.8, 0.1)

    st.sidebar.subheader("场景")
    risk_hotspots = st.sidebar.slider("风险热点数量", 1, 8, 4, 1)
    risk_intensity = st.sidebar.slider("风险热点强度", 0.2, 3.0, 1.3, 0.1)
    cost_mode = st.sidebar.selectbox(
        "成本分布模式",
        ["中心城区高成本", "靠近交通走廊低成本", "多中心商务区高成本"],
    )
    grid_size = st.sidebar.slider("热力图网格精度", 80, 260, 160, 20)

    return {
        "seed": int(seed) + int(st.session_state.scenario_shift) * 997,
        "num_points": int(num_points),
        "weight_min": float(weight_min),
        "weight_max": float(weight_max),
        "demand_hotspots": int(demand_hotspots),
        "demand_spread": float(demand_spread),
        "cluster_count": int(cluster_count),
        "selected_count": int(selected_count),
        "population_size": int(population_size),
        "generations": int(generations),
        "crossover_prob": float(crossover_prob),
        "mutation_prob": float(mutation_prob),
        "service_radius": float(service_radius),
        "w_demand": float(w_demand),
        "w_risk": float(w_risk),
        "w_cost": float(w_cost),
        "risk_hotspots": int(risk_hotspots),
        "risk_intensity": float(risk_intensity),
        "cost_mode": cost_mode,
        "grid_size": int(grid_size),
    }


def render_siting_module(
    demand: pd.DataFrame,
    candidates: pd.DataFrame,
    hotspots,
    xx,
    yy,
    risk,
    cost,
    ga_result,
    selected_ids: set[int],
) -> None:
    total_demand = demand["demand_weight"].sum()
    selected = candidates[candidates["is_selected"]].copy()
    covered_demand = selected["coverage"].sum()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("需求点数量", f"{len(demand)}")
    kpi2.metric("候选起降点", f"{len(candidates)}")
    kpi3.metric("最终选址", f"{len(selected)}")
    kpi4.metric("最优适应度", f"{ga_result.best_score:.4f}")

    st.info("综合目标函数：F = w1 * 需求覆盖率 - w2 * 平均风险 - w3 * 平均成本。")

    tab_overview, tab_steps, tab_result, tab_data = st.tabs(
        ["综合对比图", "流程分步展示", "GA 与指标", "数据导出"]
    )

    with tab_overview:
        fig = build_scene_figure(
            title="综合对比：需求点、风险场、成本场、候选点与最终选址",
            demand_df=demand,
            candidates=candidates,
            selected_ids=selected_ids,
            xx=xx,
            yy=yy,
            risk=risk,
            cost=cost,
            show_risk=True,
            show_cost=True,
            show_clusters=True,
            show_lines=True,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.download_button(
            "保存综合对比图 HTML",
            data=fig.to_html(include_plotlyjs="cdn").encode("utf-8"),
            file_name="evtol_site_selection_overview.html",
            mime="text/html",
        )

    with tab_steps:
        step = st.radio(
            "选择展示步骤",
            [
                "1 仅展示风险场",
                "2 风险场+成本场",
                "3 风险场+成本场+原始需求点",
                "4 加上K-means聚类结果",
                "5 加上GA最终选址",
            ],
            horizontal=True,
        )

        if step.startswith("1"):
            fig = build_scene_figure(
                "步骤1：仅展示风险场",
                demand,
                xx=xx,
                yy=yy,
                risk=risk,
                show_risk=True,
                show_demand=False,
            )
        elif step.startswith("2"):
            fig = build_scene_figure(
                "步骤2：展示风险场与成本场",
                demand,
                xx=xx,
                yy=yy,
                risk=risk,
                cost=cost,
                show_risk=True,
                show_cost=True,
                show_demand=False,
            )
        elif step.startswith("3"):
            fig = build_scene_figure(
                "步骤3：在风险场和成本场上叠加原始需求点",
                demand,
                xx=xx,
                yy=yy,
                risk=risk,
                cost=cost,
                show_risk=True,
                show_cost=True,
            )
        elif step.startswith("4"):
            fig = build_scene_figure(
                "步骤4：加入 K-means 聚类结果与候选起降点",
                demand,
                candidates=candidates,
                xx=xx,
                yy=yy,
                risk=risk,
                cost=cost,
                show_risk=True,
                show_cost=True,
                show_clusters=True,
                show_lines=True,
            )
        else:
            fig = build_scene_figure(
                "步骤5：GA最终选址与最终综合结果",
                demand,
                candidates=candidates,
                selected_ids=selected_ids,
                xx=xx,
                yy=yy,
                risk=risk,
                cost=cost,
                show_risk=True,
                show_cost=True,
                show_clusters=True,
                show_lines=True,
            )
        st.plotly_chart(fig, use_container_width=True)

    with tab_result:
        left, right = st.columns([1.1, 1.0])
        with left:
            st.plotly_chart(build_convergence_figure(ga_result.history), use_container_width=True)
        with right:
            st.subheader("最终起降点指标")
            display_cols = ["candidate_id", "x", "y", "coverage", "coverage_ratio", "risk", "cost", "single_score"]
            st.dataframe(
                selected[display_cols].sort_values("single_score", ascending=False).round(4),
                use_container_width=True,
                hide_index=True,
            )
            st.caption(
                f"总需求权重约 {total_demand:.2f}；表中 coverage 为单点服务半径内的加权需求，"
                f"各点 coverage 简单求和为 {covered_demand:.2f}，可能因覆盖区域重叠而重复计数。"
            )

        st.subheader("风险热点")
        st.dataframe(
            pd.DataFrame([h.__dict__ for h in hotspots]).round(3),
            use_container_width=True,
            hide_index=True,
        )

    with tab_data:
        st.subheader("候选点与最终选址数据")
        st.dataframe(candidates.round(4), use_container_width=True, hide_index=True)
        st.download_button(
            "导出候选点/选址结果 CSV",
            data=csv_download(candidates),
            file_name="evtol_candidates_and_selection.csv",
            mime="text/csv",
        )

        st.subheader("需求点数据")
        st.dataframe(demand.round(4), use_container_width=True, hide_index=True)
        st.download_button(
            "导出需求点 CSV",
            data=csv_download(demand),
            file_name="evtol_demand_points.csv",
            mime="text/csv",
        )

        st.subheader("GA 收敛数据")
        st.dataframe(ga_result.history.round(6), use_container_width=True, hide_index=True)
        st.download_button(
            "导出 GA 收敛曲线 CSV",
            data=csv_download(ga_result.history),
            file_name="evtol_ga_history.csv",
            mime="text/csv",
        )


def _run_planners(
    mode: str,
    start: tuple[float, float],
    risk,
    cost,
    astar_config: AStarConfig,
    rrt_config: RRTStarConfig,
    smooth_rrt: bool,
) -> dict:
    results = {}
    if mode in ("A*", "算法对比"):
        results["A*"] = run_astar(start, AIRPORT_POINT, risk, cost, astar_config)
    if mode in ("RRT*", "算法对比"):
        results["RRT*"] = run_rrtstar(start, AIRPORT_POINT, risk, cost, rrt_config, smooth_rrt)
    return results


def render_path_planning_module(
    candidates: pd.DataFrame,
    risk,
    cost,
    params: dict,
) -> None:
    st.subheader("第二模块：路径规划与 A* / RRT* 算法对比")
    st.caption("本模块直接复用第一模块 GA 输出的最终起降点，用户选择其中一个作为客户侧起点，机场接驳终点固定唯一。")

    selected_sites = candidates[candidates["is_selected"]].copy().sort_values("candidate_id")
    if selected_sites.empty:
        st.warning("当前没有最终起降点，请先在左侧降低约束或重新生成选址结果。")
        return

    left, right = st.columns([0.76, 0.24])
    with right:
        st.markdown("#### 起始终点与算法")
        labels = [
            f"起降点 {int(row.candidate_id)} | ({row.x:.1f}, {row.y:.1f}) | 覆盖{row.coverage:.1f}"
            for row in selected_sites.itertuples()
        ]
        id_values = selected_sites["candidate_id"].astype(int).tolist()
        label_to_id = dict(zip(labels, id_values))
        start_label = st.selectbox("选择客户侧起降点", labels)
        start_id = int(label_to_id[start_label])
        start_row = selected_sites[selected_sites["candidate_id"] == start_id].iloc[0]
        start = (float(start_row["x"]), float(start_row["y"]))

        st.write(f"机场接驳终点：`({AIRPORT_POINT[0]:.1f}, {AIRPORT_POINT[1]:.1f})`")
        run_mode_label = st.radio("运行方式", ["算法对比", "A* 算法", "RRT* 算法"], horizontal=True)
        run_mode = {"算法对比": "算法对比", "A* 算法": "A*", "RRT* 算法": "RRT*"}[run_mode_label]

        st.markdown("#### 通用代价权重")
        alpha = st.slider("路径长度权重 α", 0.0, 5.0, 1.0, 0.1)
        beta = st.slider("风险权重 β", 0.0, 12.0, 4.0, 0.2)
        gamma = st.slider("成本权重 γ", 0.0, 8.0, 1.2, 0.2)
        obstacle_threshold = st.slider("风险障碍阈值", 0.35, 0.95, 0.72, 0.01)

        st.markdown("#### A* 参数")
        grid_resolution = st.slider("网格分辨率", 40, 150, 90, 5)
        heuristic = st.selectbox("启发函数", ["欧氏距离", "曼哈顿距离"])
        obstacle_inflation = st.slider("障碍膨胀半径（格）", 0, 6, 1, 1)

        st.markdown("#### RRT* 参数")
        max_iterations = st.slider("最大迭代次数", 100, 3000, 900, 100)
        step_size = st.slider("步长", 1.0, 12.0, 4.5, 0.5)
        neighbor_radius = st.slider("邻域半径", 3.0, 25.0, 10.0, 0.5)
        goal_bias = st.slider("目标偏置概率", 0.0, 0.5, 0.12, 0.01)
        safety_buffer = st.slider("障碍安全缓冲", 0.5, 6.0, 1.5, 0.5)
        smooth_rrt = st.checkbox("启用 RRT* 路径平滑", value=True)

        frame_fraction = st.slider("动态搜索进度", 0.05, 1.0, 1.0, 0.05)

        run_clicked = st.button("运行 / 重新规划", use_container_width=True, type="primary")
        all_starts_clicked = st.button("一键比较所有起降点", use_container_width=True)

    astar_config = AStarConfig(
        grid_resolution=grid_resolution,
        heuristic=heuristic,
        obstacle_threshold=obstacle_threshold,
        obstacle_inflation=obstacle_inflation,
        alpha_distance=alpha,
        beta_risk=beta,
        gamma_cost=gamma,
    )
    rrt_config = RRTStarConfig(
        max_iterations=max_iterations,
        step_size=step_size,
        neighbor_radius=neighbor_radius,
        goal_bias=goal_bias,
        obstacle_threshold=obstacle_threshold,
        safety_buffer=safety_buffer,
        alpha_distance=alpha,
        beta_risk=beta,
        gamma_cost=gamma,
        seed=params["seed"] + start_id,
    )

    planner_key = (
        start_id,
        run_mode,
        alpha,
        beta,
        gamma,
        obstacle_threshold,
        grid_resolution,
        heuristic,
        obstacle_inflation,
        max_iterations,
        step_size,
        neighbor_radius,
        goal_bias,
        safety_buffer,
        smooth_rrt,
        params["seed"],
    )

    if run_clicked or "planner_results" not in st.session_state or st.session_state.get("planner_key") != planner_key:
        with st.spinner("正在执行路径规划算法..."):
            st.session_state.planner_results = _run_planners(
                run_mode,
                start,
                risk,
                cost,
                astar_config,
                rrt_config,
                smooth_rrt,
            )
            st.session_state.planner_key = planner_key

    results: dict = st.session_state.get("planner_results", {})
    primary = results.get("A*") or results.get("RRT*")
    secondary = results.get("RRT*") if primary and primary.algorithm == "A*" else results.get("A*")

    with left:
        fig = build_path_figure(
            risk_field=risk,
            cost_field=cost,
            selected_sites=selected_sites,
            start_id=start_id,
            airport=AIRPORT_POINT,
            obstacle_threshold=obstacle_threshold,
            result=primary,
            comparison_result=secondary,
            frame_fraction=frame_fraction,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.download_button(
            "保存当前路径图 HTML",
            data=fig.to_html(include_plotlyjs="cdn").encode("utf-8"),
            file_name="evtol_path_planning.html",
            mime="text/html",
        )

    metrics_df = metrics_to_frame([res.metrics for res in results.values()])
    if not metrics_df.empty:
        st.markdown("#### 路径规划量化分析")
        display_cols = [
            "algorithm",
            "success",
            "path_length",
            "cumulative_risk",
            "cumulative_cost",
            "average_risk",
            "min_obstacle_distance",
            "runtime_s",
            "node_count",
            "turn_count",
            "tortuosity",
        ]
        st.dataframe(metrics_df[display_cols].round(4), use_container_width=True, hide_index=True)

        if len(metrics_df) >= 2:
            st.plotly_chart(build_comparison_bar(metrics_df), use_container_width=True)
            best_length = metrics_df.sort_values("path_length").iloc[0]["algorithm"]
            best_risk = metrics_df.sort_values("cumulative_risk").iloc[0]["algorithm"]
            fast = metrics_df.sort_values("runtime_s").iloc[0]["algorithm"]
            st.success(
                f"对比结论：当前参数下，路径最短的是 {best_length}，累计风险最低的是 {best_risk}，计算最快的是 {fast}。"
            )

        st.download_button(
            "导出当前路径指标 CSV",
            data=csv_download(metrics_df),
            file_name="evtol_path_metrics.csv",
            mime="text/csv",
        )

    if all_starts_clicked:
        rows = []
        progress = st.progress(0.0)
        for idx, row in enumerate(selected_sites.itertuples()):
            s = (float(row.x), float(row.y))
            local_rrt = RRTStarConfig(
                max_iterations=max(300, int(max_iterations * 0.65)),
                step_size=step_size,
                neighbor_radius=neighbor_radius,
                goal_bias=goal_bias,
                obstacle_threshold=obstacle_threshold,
                safety_buffer=safety_buffer,
                alpha_distance=alpha,
                beta_risk=beta,
                gamma_cost=gamma,
                seed=params["seed"] + int(row.candidate_id),
            )
            a_res = run_astar(s, AIRPORT_POINT, risk, cost, astar_config)
            r_res = run_rrtstar(s, AIRPORT_POINT, risk, cost, local_rrt, smooth_rrt)
            for res in (a_res, r_res):
                record = res.metrics.copy()
                record["start_candidate_id"] = int(row.candidate_id)
                rows.append(record)
            progress.progress((idx + 1) / len(selected_sites))
        all_df = pd.DataFrame(rows)
        st.markdown("#### 所有起降点到机场的批量对比")
        st.dataframe(all_df.round(4), use_container_width=True, hide_index=True)
        st.download_button(
            "导出所有起点路径对比 CSV",
            data=csv_download(all_df),
            file_name="evtol_all_start_path_comparison.csv",
            mime="text/csv",
        )


def main() -> None:
    st.title("二维平面 eVTOL 起降点选址与路径规划可视化方案")
    st.markdown(
        "系统包含两个连续模块：第一模块完成需求生成、K-means 候选点和 GA 综合选址；"
        "第二模块基于最终起降点，规划到机场接驳终点的航线，并对比 A* 与 RRT*。"
    )

    params = build_sidebar()

    with st.spinner("正在生成需求点、风险/成本场、K-means 候选点并执行 GA 优化..."):
        demand, candidates, hotspots, xx, yy, risk, cost, ga_result, selected_ids = compute_pipeline(params)

    module_tab1, module_tab2 = st.tabs(["第一模块：起降点选址", "第二模块：路径规划与算法对比"])

    with module_tab1:
        render_siting_module(demand, candidates, hotspots, xx, yy, risk, cost, ga_result, selected_ids)

    with module_tab2:
        render_path_planning_module(candidates, risk, cost, params)


if __name__ == "__main__":
    main()
