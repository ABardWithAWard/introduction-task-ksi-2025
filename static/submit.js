document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("name").value;
        const description = document.getElementById("description").value;

        if (!name || !description) {
            alert("Please fill in the form.");
            return;
        }

        const taskData = {
            name: name,
            description: description
        };

        try {
            const response = await fetch("http://127.0.0.1:8000/tasks/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(taskData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                new Error(`Error: ${response.status} ${JSON.stringify(errorData)}`);
            }

            const result = await response.json();
            console.log("Task created:", result);
            alert("Success!");

            form.reset();

        } catch (error) {
            console.error("Error creating task:", error);
            alert("Failure");
        }
    });
});