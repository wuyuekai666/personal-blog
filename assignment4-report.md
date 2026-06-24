---
layout: default
title: Assignment 4 Report
---

<style>
.report-container {
  max-width: 980px;
  margin: 0 auto;
  line-height: 1.75;
  color: #24292f;
}

.hero-card {
  background: linear-gradient(135deg, #eef5ff, #f7f9fc);
  border-left: 6px solid #0969da;
  padding: 24px 28px;
  border-radius: 14px;
  margin: 24px 0 30px 0;
}

.section-card {
  background: #ffffff;
  border: 1px solid #d8dee4;
  border-radius: 14px;
  padding: 24px 28px;
  margin: 28px 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
}

.report-container h1 {
  font-size: 2.4em;
  margin-bottom: 0.3em;
}

.report-container h2 {
  border-bottom: 2px solid #d8dee4;
  padding-bottom: 8px;
  margin-top: 0;
}

.report-container table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
}

.report-container th {
  background: #f6f8fa;
  font-weight: 700;
}

.report-container th,
.report-container td {
  border: 1px solid #d8dee4;
  padding: 10px 12px;
  vertical-align: top;
}

.report-container code {
  background: #f6f8fa;
  padding: 2px 5px;
  border-radius: 5px;
  font-family: Consolas, Monaco, monospace;
}

.report-container pre {
  background: #f6f8fa;
  padding: 16px;
  border-radius: 10px;
  overflow-x: auto;
  border: 1px solid #d8dee4;
}

.badge {
  display: inline-block;
  background: #e7f0ff;
  color: #0969da;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.9em;
  margin: 6px 6px 0 0;
}
</style>

<div class="report-container">

<h1>Assignment 4: Developing an AI-Assisted Application</h1>

<div class="hero-card">
  <p><strong>Student Name:</strong> WuYuekai</p>
  <p><strong>Student ID:</strong> ZY2557209</p>
  <p><strong>Selected Option:</strong> Option B: Academic / Research Tool</p>
  <p>
    <span class="badge">eVTOL</span>
    <span class="badge">Streamlit</span>
    <span class="badge">K-means</span>
    <span class="badge">Genetic Algorithm</span>
    <span class="badge">A*</span>
    <span class="badge">RRT*</span>
    <span class="badge">Plotly</span>
  </p>
</div>

<div class="section-card">
  <h2>1. Background and Design</h2>
  <p>
    For Assignment 4, I chose Option B and developed an academic research tool related to
    urban low-altitude mobility. The project is a two-dimensional eVTOL landing-site selection
    and path-planning visualization system. It is designed for research discussion, thesis
    demonstration, and algorithm comparison.
  </p>
  <p>
    The reason I chose this topic is that eVTOL operation is not only a vehicle problem.
    It also involves urban demand distribution, risk areas, operating cost, site selection,
    and route planning. A visual tool is useful because it allows users to adjust parameters
    and immediately observe how the final sites and routes change.
  </p>
  <p>The application contains two connected modules:</p>
  <ol>
    <li>
      <strong>Landing-site selection:</strong> generate passenger demand points, create candidate
      sites with K-means, and use a genetic algorithm to select final eVTOL landing sites.
    </li>
    <li>
      <strong>Path planning and algorithm comparison:</strong> use selected sites as origins and
      compare A* and RRT* paths to a fixed airport connection point.
    </li>
  </ol>
</div>

<div class="section-card">
  <h2>2. Functional Software</h2>
  <p>
    The application is implemented as a Streamlit web application. It runs locally in a browser
    and provides interactive sliders, tabs, Plotly charts, route visualizations, metric tables,
    and export buttons.
  </p>
  <p>Local run command:</p>
  <pre><code>pip install -r requirements.txt
streamlit run main.py</code></pre>
  <p>On Windows, the project also provides a one-click startup script:</p>
  <pre><code>run_app.bat</code></pre>
  <p>Project files for review:</p>
  <ul>
    <li><a href="assignment4/">Assignment 4 Project Page</a></li>
    <li><a href="assignment4/eVTOL_site_selection_source.zip">Download Source ZIP</a></li>
    <li><a href="assignment4/eVTOL-System-Overview.pptx">Download Presentation PPTX</a></li>
    <li><a href="assignment4/source/main.py">Main Streamlit Application</a></li>
    <li><a href="assignment4/source/README.md">Project README</a></li>
    <li><a href="assignment4/source/DEPLOYMENT.md">Deployment Instructions</a></li>
  </ul>
</div>

<div class="section-card">
  <h2>3. Tech Stack</h2>
  <table>
    <tr><th>Technology</th><th>Use in the Project</th></tr>
    <tr><td>Python</td><td>Main programming language for algorithms and application logic</td></tr>
    <tr><td>Streamlit</td><td>Interactive web interface and local browser application</td></tr>
    <tr><td>NumPy</td><td>Numerical computation, fields, geometry, and algorithm operations</td></tr>
    <tr><td>Pandas</td><td>Data tables, metrics, and CSV export</td></tr>
    <tr><td>Plotly</td><td>Interactive heatmaps, scatter plots, route plots, and comparison charts</td></tr>
    <tr><td>K-means</td><td>Generate candidate eVTOL landing sites from demand points</td></tr>
    <tr><td>Genetic Algorithm</td><td>Select final landing sites based on demand coverage, risk, and cost</td></tr>
    <tr><td>A*</td><td>Grid-based path planning with risk obstacles and heuristic search</td></tr>
    <tr><td>RRT*</td><td>Sampling-based path planning in continuous 2D space</td></tr>
  </table>
</div>

<div class="section-card">
  <h2>4. Architecture</h2>
  <p>The project structure is modular:</p>
  <pre><code>eVTOL_site_selection/
├── main.py
├── requirements.txt
├── run_app.bat
├── README.md
├── DEPLOYMENT.md
└── evtol/
    ├── scene.py
    ├── fields.py
    ├── clustering.py
    ├── ga.py
    ├── visualization.py
    ├── path_planning.py
    ├── path_analysis.py
    └── path_visualization.py</code></pre>
  <p>
    <code>main.py</code> is the Streamlit entry point. The <code>evtol</code> package contains
    reusable algorithm and visualization modules. This separation made the code easier to test,
    debug, and extend.
  </p>
</div>

<div class="section-card">
  <h2>5. Core Features</h2>
  <h3>5.1 Landing-Site Selection</h3>
  <ul>
    <li>Randomly generates passenger demand points in a 2D city area.</li>
    <li>Creates risk fields and cost fields to simulate real urban constraints.</li>
    <li>Uses K-means to create candidate landing sites.</li>
    <li>Uses a genetic algorithm to choose final sites.</li>
    <li>Displays demand points, candidate sites, selected sites, risk/cost heatmaps, and GA convergence.</li>
  </ul>
  <p>The site-selection objective function is:</p>
  <pre><code>F = w1 * demand_coverage - w2 * average_risk - w3 * average_cost</code></pre>

  <h3>5.2 Path Planning and Algorithm Comparison</h3>
  <ul>
    <li>Uses the selected landing sites as route origins.</li>
    <li>Uses a fixed airport connection point as the destination.</li>
    <li>Runs A*, RRT*, or both algorithms for comparison.</li>
    <li>Visualizes search progress, obstacles, final paths, and selected sites.</li>
    <li>Compares path length, cumulative risk, cumulative cost, runtime, node count, turn count, and tortuosity.</li>
  </ul>
</div>

<div class="section-card">
  <h2>6. AI-Assisted Development Process</h2>
  <p>
    LLMs were used as a development partner rather than a replacement for my own design decisions.
    I used AI mainly in three ways: architecture planning, algorithm debugging, and code explanation.
  </p>
  <table>
    <tr><th>Stage</th><th>How AI Helped</th><th>My Decision / Verification</th></tr>
    <tr>
      <td>Architecture</td>
      <td>AI helped break the project into scene generation, fields, clustering, GA, path planning, and visualization modules.</td>
      <td>I kept the two-module workflow because it matched my research logic: site selection first, route planning second.</td>
    </tr>
    <tr>
      <td>Problem Solving</td>
      <td>AI helped reason about A* grid conversion, obstacle masks, RRT* collision checking, and route metrics.</td>
      <td>I checked whether the algorithms produced visible paths and whether the metrics matched the plotted routes.</td>
    </tr>
    <tr>
      <td>Interface Design</td>
      <td>AI suggested using Streamlit tabs, sliders, metric cards, and download buttons.</td>
      <td>I selected controls that were useful for experiments instead of adding decorative UI only.</td>
    </tr>
    <tr>
      <td>Documentation</td>
      <td>AI helped organize README and deployment instructions.</td>
      <td>I adjusted the documentation to match my local Windows running process and project files.</td>
    </tr>
  </table>
</div>

<div class="section-card">
  <h2>7. Development Log</h2>
  <ol>
    <li>
      <strong>Initial idea:</strong> I chose eVTOL infrastructure planning as the research direction
      and decided to build a tool instead of a simple static report.
    </li>
    <li>
      <strong>First module:</strong> I implemented demand generation, risk/cost fields, K-means candidate
      sites, GA site selection, and Plotly visualization.
    </li>
    <li>
      <strong>Second module:</strong> I added path planning from selected customer-side landing sites
      to an airport connection point.
    </li>
    <li>
      <strong>Algorithm comparison:</strong> I added A* and RRT* so users can compare grid-based and
      sampling-based planning results.
    </li>
    <li>
      <strong>Metrics and export:</strong> I added quantitative metrics, bar-chart comparison, CSV export,
      and HTML plot export.
    </li>
    <li>
      <strong>Packaging:</strong> I wrote <code>run_app.bat</code>, <code>README.md</code>, and
      <code>DEPLOYMENT.md</code> so the project can be run on another Windows computer.
    </li>
  </ol>
</div>

<div class="section-card">
  <h2>8. Problems and Fixes</h2>
  <table>
    <tr><th>Problem</th><th>Fix</th></tr>
    <tr>
      <td>A* may fail if the start or end point is inside an obstacle cell.</td>
      <td>I added logic to snap points to nearby free grid cells and included obstacle inflation controls.</td>
    </tr>
    <tr>
      <td>RRT* paths may be noisy because of random sampling.</td>
      <td>I added goal bias, neighborhood rewiring, collision checking, and optional path smoothing.</td>
    </tr>
    <tr>
      <td>The path-planning result is hard to understand from only one metric.</td>
      <td>I added multiple metrics including length, risk, cost, runtime, node count, turn count, and tortuosity.</td>
    </tr>
    <tr>
      <td>Users may not know how to run a Streamlit app.</td>
      <td>I added <code>run_app.bat</code> and deployment instructions for Windows.</td>
    </tr>
  </table>
</div>

<div class="section-card">
  <h2>9. Results</h2>
  <p>
    The final application can run locally as a Streamlit web app. It provides an interactive research
    workflow from demand modeling to final route comparison. Users can change parameters and immediately
    see how candidate sites, final sites, and paths respond.
  </p>
  <p>The project supports:</p>
  <ul>
    <li>interactive eVTOL landing-site selection;</li>
    <li>GA convergence visualization;</li>
    <li>A* and RRT* path planning;</li>
    <li>dynamic search-process visualization;</li>
    <li>quantitative algorithm comparison;</li>
    <li>CSV and HTML export.</li>
  </ul>
</div>

<div class="section-card">
  <h2>10. Reflection</h2>
  <p>
    This project helped me understand the difference between using AI for simple prompting and using AI
    as an engineering partner. The most useful part of AI assistance was not just generating code, but
    helping me split a complex research idea into smaller modules and debug each module step by step.
  </p>
  <p>
    I also learned that a research tool needs both algorithms and usability. If the app only has code but
    no clear visualization, it is difficult to explain. If it only has a good interface but no real algorithm,
    it is not useful for research. This project tried to balance both sides.
  </p>
</div>

<div class="section-card">
  <h2>11. References</h2>
  <ul>
    <li><a href="https://streamlit.io/">Streamlit Documentation</a></li>
    <li><a href="https://numpy.org/">NumPy Documentation</a></li>
    <li><a href="https://pandas.pydata.org/">Pandas Documentation</a></li>
    <li><a href="https://plotly.com/python/">Plotly Python Documentation</a></li>
    <li><a href="https://en.wikipedia.org/wiki/A*_search_algorithm">A* Search Algorithm</a></li>
    <li><a href="https://en.wikipedia.org/wiki/Rapidly_exploring_random_tree">Rapidly-exploring Random Tree</a></li>
  </ul>
</div>

</div>
