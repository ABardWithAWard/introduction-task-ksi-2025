document.addEventListener("DOMContentLoaded", async () => {
    const countSpan = document.getElementById("task-count");
    const taskList = document.getElementById("task-list");

    try {
        const tasksResponse = await fetch("http://127.0.0.1:8000/tasks/");
        const tasks = await tasksResponse.json();

        tasks.forEach(task => {
            const li = document.createElement("li");
            li.textContent = `${task.name}: ${task.description} `;

            const button = document.createElement("button");
            button.textContent = `Delete task ${task.id}`;
            button.id = `task-btn-${task.id}`;
            button.dataset.taskId = task.id;
            button.addEventListener("click", () => {
                alert(`Clicked!`);
            });

            li.appendChild(button);
            taskList.appendChild(li);
        });

    } catch (error) {
        console.error("Error fetching tasks:", error);
        countSpan.textContent = "Error";
        taskList.innerHTML = "<li>Could not load tasks.</li>";
    }
});