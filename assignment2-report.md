---
layout: default
title: Assignment 2 Report
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

.report-container h3 {
  margin-top: 20px;
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

.link-list li {
  margin: 8px 0;
}
</style>

<div class="report-container">

<h1>Assignment 2: Static Personal Blog Website</h1>

<div class="hero-card">
  <p><strong>Student Name:</strong> WuYuekai</p>
  <p><strong>Student ID:</strong> ZY2557209</p>
  <p>
    <span class="badge">Static Website</span>
    <span class="badge">Git</span>
    <span class="badge">GitHub Pages</span>
    <span class="badge">Jekyll</span>
    <span class="badge">Markdown</span>
  </p>
</div>

<div class="section-card">
  <h2>1. Project Overview</h2>

  <p>
    The objective of this assignment is to set up and deploy a static personal blog website.
    The website is accessible through a public URL and is used to organize course assignments,
    reports, source code, and documentation.
  </p>

  <p>
    In this project, I used GitHub Pages to deploy the website and Git to manage the source files.
    I also integrated my previous Assignment 1 work into the website by providing links to the
    Markdown report, PDF report, and Python source code.
  </p>

  <p>The main goals of this assignment are:</p>

  <ul>
    <li>Build a static personal blog website.</li>
    <li>Use Git for version control.</li>
    <li>Make at least five meaningful commits.</li>
    <li>Deploy the website to a public URL.</li>
    <li>Integrate Assignment 1 files into the website.</li>
    <li>Document the development and deployment process.</li>
  </ul>
</div>

<div class="section-card">
  <h2>2. Tools and Frameworks</h2>

  <table>
    <tr>
      <th>Tool</th>
      <th>Purpose</th>
    </tr>
    <tr>
      <td>HTML</td>
      <td>Basic webpage structure and content layout</td>
    </tr>
    <tr>
      <td>Markdown</td>
      <td>Writing technical documentation</td>
    </tr>
    <tr>
      <td>Git</td>
      <td>Version control and commit history management</td>
    </tr>
    <tr>
      <td>GitHub</td>
      <td>Remote repository hosting</td>
    </tr>
    <tr>
      <td>GitHub Pages</td>
      <td>Static website deployment</td>
    </tr>
    <tr>
      <td>Jekyll</td>
      <td>Rendering Markdown files as styled webpages</td>
    </tr>
  </table>

  <p>
    I chose GitHub Pages because it is free and suitable for hosting static websites.
    I used Jekyll because it can automatically render Markdown files into web pages.
  </p>
</div>

<div class="section-card">
  <h2>3. Website Structure</h2>

  <p>The project structure is shown below:</p>

  <pre><code>personal-blog/
├── _config.yml
├── index.md
├── README.md
├── assignment2-report.md
└── assignment1/
    ├── matrix_multiply.py
    ├── report.md
    └── report.pdf</code></pre>

  <p>
    The homepage introduces the website and provides links to the assignment reports.
    The Assignment 1 folder contains the previous report files and the Python implementation.
  </p>
</div>

<div class="section-card">
  <h2>4. Development Process</h2>

  <h3>4.1 Create the Project Folder</h3>

  <p>I first created a folder for the website project and initialized Git.</p>

  <pre><code>mkdir personal-blog
cd personal-blog
git init</code></pre>

  <h3>4.2 Create the Homepage</h3>

  <p>
    I created the first version of the homepage to introduce the website and list course assignments.
  </p>

  <h3>4.3 Add Assignment 1 Files</h3>

  <p>
    After completing Assignment 1, I added the Markdown report, PDF report, and Python source code
    into the <code>assignment1</code> folder.
  </p>

  <h3>4.4 Add Documentation</h3>

  <p>
    I wrote this Assignment 2 report to explain the setup, Git management process, deployment process,
    and problems encountered during development.
  </p>

  <h3>4.5 Deploy the Website</h3>

  <p>
    Finally, I pushed the project to GitHub and enabled GitHub Pages to make the website accessible online.
  </p>
</div>

<div class="section-card">
  <h2>5. Git Management Process</h2>

  <p>
    Git was used to track changes throughout the project. I made meaningful commits that reflected
    the logical development process of the website.
  </p>

  <table>
    <tr>
      <th>Commit Message</th>
      <th>Purpose</th>
    </tr>
    <tr>
      <td>Initial website homepage</td>
      <td>Created the first version of the website homepage.</td>
    </tr>
    <tr>
      <td>Add assignment 1 report and Python implementation</td>
      <td>Added Assignment 1 report files and Python source code.</td>
    </tr>
    <tr>
      <td>Add project README</td>
      <td>Added a README file to describe the website project.</td>
    </tr>
    <tr>
      <td>Add assignment 2 documentation</td>
      <td>Added the documentation report for Assignment 2.</td>
    </tr>
    <tr>
      <td>Update homepage with assignment links</td>
      <td>Updated the homepage and added links to assignment files.</td>
    </tr>
    <tr>
      <td>Configure Jekyll to render Markdown pages</td>
      <td>Configured Jekyll so Markdown files could be rendered as webpages.</td>
    </tr>
  </table>

  <p>
    These commits show the progress from initial website setup to final deployment and documentation.
  </p>
</div>

<div class="section-card">
  <h2>6. Deployment Process</h2>

  <p>The website was deployed using GitHub Pages. The deployment steps were:</p>

  <ol>
    <li>Create a GitHub repository named <code>personal-blog</code>.</li>
    <li>Push the local Git repository to GitHub.</li>
    <li>Open the repository settings on GitHub.</li>
    <li>Go to the <code>Pages</code> section.</li>
    <li>Select <code>Deploy from a branch</code>.</li>
    <li>Choose the <code>main</code> branch and the root folder.</li>
    <li>Save the settings and wait for GitHub Pages to build the website.</li>
  </ol>

  <p>The website is available at:</p>

  <p>
    <a href="https://wuyuekai666.github.io/personal-blog/">
      https://wuyuekai666.github.io/personal-blog/
    </a>
  </p>
</div>

<div class="section-card">
  <h2>7. Integration of Previous Work</h2>

  <p>
    Assignment 1 is integrated into this website. The website provides links to the previous report
    and source code.
  </p>

  <ul class="link-list">
    <li><a href="assignment1/report">Assignment 1 Report Web Page</a></li>
    <li><a href="assignment1/report.md">Assignment 1 Markdown Source</a></li>
    <li><a href="assignment1/report.pdf?v=5">Assignment 1 PDF Report</a></li>
    <li><a href="assignment1/matrix_multiply.py">Assignment 1 Python Source Code</a></li>
  </ul>
</div>

<div class="section-card">
  <h2>8. Problems and Solutions</h2>

  <h3>8.1 GitHub Network Access</h3>

  <p>
    Sometimes pushing files to GitHub failed because of network connection problems.
    I solved this by retrying the <code>git push</code> command after the network connection became stable.
  </p>

  <h3>8.2 Markdown Rendering</h3>

  <p>
    At first, some Markdown pages were displayed as raw text instead of styled webpages.
    I solved this by using Jekyll front matter and improving the Markdown page structure.
  </p>

  <h3>8.3 PDF Cache</h3>

  <p>
    When I updated the PDF report, the browser sometimes still displayed the old PDF.
    I solved this by adding a version parameter to the PDF link, such as <code>?v=5</code>.
  </p>
</div>

<div class="section-card">
  <h2>9. Conclusion</h2>

  <p>
    Through this assignment, I learned how to create and deploy a static personal website.
    I practiced using Git for version control and GitHub Pages for online deployment.
  </p>

  <p>
    I also learned how to organize course files in a website project and how to link previous assignments
    from a homepage. This assignment helped me understand the basic workflow of website development,
    documentation, version control, and deployment.
  </p>
</div>

<div class="section-card">
  <h2>10. References</h2>

  <ul>
    <li><a href="https://docs.github.com/en/pages">GitHub Pages Documentation</a></li>
    <li><a href="https://jekyllrb.com/docs/">Jekyll Documentation</a></li>
    <li><a href="https://git-scm.com/doc">Git Documentation</a></li>
    <li><a href="https://www.markdownguide.org/">Markdown Guide</a></li>
  </ul>
</div>

</div>
