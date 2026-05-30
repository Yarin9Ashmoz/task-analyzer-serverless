// API Configuration (We will update this URL once AWS API Gateway is deployed)
const API_BASE_URL = "https://l7wa68iehd.execute-api.eu-north-1.amazonaws.com/prod"; 

// Executed when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    fetchTasks();
    
    // Attach event listener to the task creation form
    const taskForm = document.getElementById("task-form");
    taskForm.addEventListener("submit", handleTaskSubmit);
});

/**
 * Fetches the task list from the backend API.
 * Falls back to local mock data if the API URL is not configured yet.
 */
async function fetchTasks() {
    const container = document.getElementById("tasks-container");
    const loadingMessage = document.getElementById("loading-message");

    // If no API URL is provided yet, simulate data loading for testing the UI
    if (!API_BASE_URL) {
        console.log("API URL not configured. Loading local mock data...");
        const mockTasks = [
            { id: "1", title: "Setup GitHub Repo", description: "Initialize git, add .gitignore, and push baseline structure.", status: "done" },
            { id: "2", title: "Configure AWS Lambda", description: "Write standard Python handlers for task management.", status: "in-progress" }
        ];
        
        setTimeout(() => {
            loadingMessage.style.display = "none";
            renderTasks(mockTasks);
        }, 800); // Simulated network delay
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/tasks`);
        if (!response.ok) throw new Error("Failed to fetch tasks from server.");
        
        const data = await response.json();
        loadingMessage.style.display = "none";
        renderTasks(data.tasks);
    } catch (error) {
        console.error("Error fetching tasks:", error);
        loadingMessage.innerText = "Error loading tasks from AWS. Please try again later.";
    }
}

/**
 * Dynamically injects tasks into the HTML container.
 * @param {Array} tasks - List of task objects
 */
function renderTasks(tasks) {
    const container = document.getElementById("tasks-container");
    container.innerHTML = ""; // Clear existing content

    if (tasks.length === 0) {
        container.innerHTML = "<p>No tasks found. Create one above!</p>";
        return;
    }

    tasks.forEach(task => {
        // Sanitize status string for CSS class mapping
        const statusClass = task.status.toLowerCase().replace(" ", "-");
        
        const taskCard = document.createElement("div");
        taskCard.className = `task-card ${statusClass}`;
        
        taskCard.innerHTML = `
            <h3>${task.title}</h3>
            <p>${task.description || "No description provided."}</p>
            <span class="status-badge">${task.status}</span>
        `;
        
        container.appendChild(taskCard);
    });
}

/**
 * Handles the submission of a new task form.
 */
async function handleTaskSubmit(event) {
    event.preventDefault();

    const titleInput = document.getElementById("task-title");
    const descInput = document.getElementById("task-desc");
    const submitBtn = document.getElementById("submit-btn");

    const payload = {
        title: titleInput.value,
        description: descInput.value
    };

    // UI Feedback
    submitBtn.innerText = "Creating...";
    submitBtn.disabled = true;

    // Local simulation if API is not deployed
    if (!API_BASE_URL) {
        setTimeout(() => {
            // Dynamically add the new task to the UI directly for preview
            const newTask = {
                id: Date.now().toString(),
                title: payload.title,
                description: payload.description,
                status: "pending"
            };
            
            appendSingleTask(newTask);
            
            // Reset form
            titleInput.value = "";
            descInput.value = "";
            submitBtn.innerText = "Add Task";
            submitBtn.disabled = false;
        }, 500);
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Failed to create task.");

        const data = await response.json();
        
        // Add the returned task from Lambda to the view
        appendSingleTask(data.task);

        // Reset form fields
        titleInput.value = "";
        descInput.value = "";
    } catch (error) {
        console.error("Error creating task:", error);
        alert("Failed to create task. Check console for details.");
    } finally {
        submitBtn.innerText = "Add Task";
        submitBtn.disabled = false;
    }
}

/**
 * Helper to append a single task card to the grid immediately.
 */
function appendSingleTask(task) {
    const container = document.getElementById("tasks-container");
    const statusClass = task.status.toLowerCase().replace(" ", "-");
    
    const taskCard = document.createElement("div");
    taskCard.className = `task-card ${statusClass}`;
    taskCard.innerHTML = `
        <h3>${task.title}</h3>
        <p>${task.description || "No description provided."}</p>
        <span class="status-badge">${task.status}</span>
    `;
    container.appendChild(taskCard);
}