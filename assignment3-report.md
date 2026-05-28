---
layout: default
title: Assignment 3 Report
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

.screenshot {
  margin: 18px 0 8px 0;
}

.screenshot img {
  width: 100%;
  border: 1px solid #d8dee4;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.screenshot-caption {
  color: #57606a;
  font-size: 0.95em;
  margin-top: 8px;
}
</style>

<div class="report-container">

<h1>Assignment 3: Deployment and Integration of AI Agents</h1>

<div class="hero-card">
  <p><strong>Student Name:</strong> WuYuekai</p>
  <p><strong>Student ID:</strong> ZY2557209</p>
  <p>
    <span class="badge">DeepSeek API</span>
    <span class="badge">Ollama</span>
    <span class="badge">VS Code</span>
    <span class="badge">Continue</span>
    <span class="badge">AI Agent</span>
  </p>
</div>

<div class="section-card">
  <h2>1. Project Overview</h2>
  <p>
    The objective of this assignment is to deploy and compare online and local large language models,
    integrate an LLM into a development environment, and document the complete process. I used
    DeepSeek as the online model provider, Ollama for local model deployment, and the Continue
    extension in VS Code for IDE integration.
  </p>
  <p>The main goals of this assignment are:</p>
  <ul>
    <li>Use an online LLM API to complete an agent-style task.</li>
    <li>Install Ollama and prepare a local model environment.</li>
    <li>Integrate an LLM into VS Code.</li>
    <li>Use the AI assistant to explain or improve code.</li>
    <li>Compare online and local models based on setup, performance, and usefulness.</li>
  </ul>
</div>

<div class="section-card">
  <h2>2. Tools and Environment</h2>
  <table>
    <tr><th>Tool</th><th>Purpose</th></tr>
    <tr><td>DeepSeek API</td><td>Online LLM provider for chat and code assistance</td></tr>
    <tr><td>Python</td><td>Simple API test script and calculator example</td></tr>
    <tr><td>Ollama</td><td>Local LLM runtime</td></tr>
    <tr><td>VS Code</td><td>Development environment</td></tr>
    <tr><td>Continue</td><td>VS Code extension for LLM coding assistance</td></tr>
    <tr><td>pytest</td><td>Testing framework for the calculator example</td></tr>
  </table>
</div>

<div class="section-card">
  <h2>3. Online Agent with DeepSeek</h2>
  <p>
    I obtained a DeepSeek API key and tested the online model with a short request. For security,
    the real API key is not included in this report or in the source code. The Python script reads
    the key from an environment variable named <code>DEEPSEEK_API_KEY</code>.
  </p>
  <p>The model used in this part was:</p>
  <pre><code>deepseek-chat</code></pre>
  <p>I first sent a simple test prompt:</p>
  <pre><code>Reply with exactly: DeepSeek OK</code></pre>
  <p>The API returned:</p>
  <pre><code>DeepSeek OK</code></pre>
  <p>
    After confirming the API connection, I used the model as an online coding assistant. It helped
    explain a pytest file and suggested commands for running the tests. This shows that the online
    agent can analyze project files and provide useful development suggestions.
  </p>
  <div class="screenshot">
    <img src="assignment3/images/vscode_continue.png" alt="DeepSeek Chat used in Continue to analyze pytest code">
    <p class="screenshot-caption">
      Figure 1. DeepSeek Chat was connected in the Continue extension and used to analyze the pytest file.
    </p>
  </div>
</div>

<div class="section-card">
  <h2>4. Local Model Deployment with Ollama</h2>
  <p>I installed Ollama on Windows from the official website:</p>
  <pre><code>https://ollama.com/download/windows</code></pre>
  <p>After installation, I verified the version:</p>
  <pre><code>ollama --version</code></pre>
  <p>The installed version was:</p>
  <pre><code>ollama version is 0.24.0</code></pre>
  <p>I planned to pull a Qwen local model using:</p>
  <pre><code>ollama pull qwen2.5:0.5b
ollama run qwen2.5:0.5b</code></pre>
  <p>
    During the model download step, the local Ollama service worked, but the connection to the Ollama
    model registry timed out. The error message showed an <code>i/o timeout</code> when accessing
    <code>registry.ollama.ai</code>. This means the installation was successful, but the model download
    depended on network stability.
  </p>
</div>

<div class="section-card">
  <h2>5. IDE Integration with Continue</h2>
  <p>
    I installed the Continue extension in VS Code and configured it to use DeepSeek Chat. I also added
    an Ollama local model entry so that VS Code can use a local model after the model is downloaded.
  </p>
  <p>The configured model entries were:</p>
  <ul>
    <li>DeepSeek Chat</li>
    <li>Ollama Local Autodetect</li>
  </ul>
  <p>
    I opened <code>test_calculator.py</code> in VS Code and asked the AI assistant to explain the test file.
    The assistant recognized that the file used pytest and explained the tests for addition, subtraction,
    multiplication, division, factorial, and palindrome checking.
  </p>
  <p>It also suggested a command for running the tests:</p>
  <pre><code>python -m pytest test_calculator.py -v</code></pre>
  <div class="screenshot">
    <img src="assignment3/images/vscode_continue.png" alt="VS Code Continue integration screenshot">
    <p class="screenshot-caption">
      Figure 2. VS Code IDE integration with Continue. The assistant explained the test code and suggested pytest commands.
    </p>
  </div>
</div>

<div class="section-card">
  <h2>6. Code Example Used for IDE Testing</h2>
  <p>
    To test the IDE assistant, I used a small calculator module and a pytest file. The calculator module
    contains basic functions such as <code>add</code>, <code>subtract</code>, <code>multiply</code>, <code>divide</code>,
    <code>factorial</code>, and <code>is_palindrome</code>.
  </p>
  <p>Related files:</p>
  <ul>
    <li><a href="assignment3/deepseek_agent.py">DeepSeek API Test Script</a></li>
    <li><a href="assignment3/calculator.py">Calculator Source Code</a></li>
    <li><a href="assignment3/test_calculator.py">Calculator Test Code</a></li>
  </ul>
</div>

<div class="section-card">
  <h2>7. Problems and Solutions</h2>
  <table>
    <tr><th>Problem</th><th>Solution</th></tr>
    <tr>
      <td>API key should not be exposed in public files.</td>
      <td>I used an environment variable and did not put the real key in the report or source code.</td>
    </tr>
    <tr>
      <td>Ollama model download timed out.</td>
      <td>I verified that Ollama was installed correctly and planned to retry the model pull with a more stable network.</td>
    </tr>
    <tr>
      <td>VS Code needed model configuration before use.</td>
      <td>I installed Continue and configured DeepSeek Chat and Ollama model entries.</td>
    </tr>
  </table>
</div>

<div class="section-card">
  <h2>8. Reflection</h2>
  <p>
    The online model was easier to use after the API key was configured. DeepSeek responded quickly and
    was useful for explaining code and generating test commands. It was especially convenient inside VS Code
    because it did not require downloading a large model file.
  </p>
  <p>
    The local model setup required more work. Ollama itself was easy to install, but downloading a model
    depended on network stability and local computer resources. The advantage of a local model is that it can
    run on my own computer after download, which is better for privacy and offline use.
  </p>
  <p>
    For my current workflow, the online model is more convenient for immediate coding assistance, while the
    local model is useful as a future option when the network and hardware conditions are suitable.
  </p>
</div>

<div class="section-card">
  <h2>9. Conclusion</h2>
  <p>
    Through this assignment, I learned how to connect an online LLM through an API, install a local LLM
    runtime, and integrate an AI assistant into VS Code. I also learned that AI agent deployment is not only
    about chatting with a model. It also includes API management, local runtime setup, IDE configuration,
    troubleshooting, and documentation.
  </p>
</div>

<div class="section-card">
  <h2>10. References</h2>
  <ul>
    <li><a href="https://api-docs.deepseek.com/">DeepSeek API Documentation</a></li>
    <li><a href="https://ollama.com/">Ollama</a></li>
    <li><a href="https://docs.continue.dev/">Continue Documentation</a></li>
    <li><a href="https://code.visualstudio.com/">Visual Studio Code</a></li>
    <li><a href="https://docs.pytest.org/">pytest Documentation</a></li>
  </ul>
</div>

</div>
