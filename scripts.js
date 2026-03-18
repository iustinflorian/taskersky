const API_URL = "http://127.0.0.1:8000/tasks";

function toggleModal(show){
    const modal = document.getElementById('task-modal');
    modal.style.display = show ? 'flex' : 'none';
}

async function loadTasks(){
    const response = await fetch(API_URL);
    const tasks = await response.json();

    const container = document.getElementById('tasks-container');
    container.innerHTML = ""; //for clearing the loading

    tasks.forEach( task => {
        const div = document.createElement('div');
        div.className = 'task-card';
        const titleClass = task.completed ? 'done' : '';

        div.innerHTML = `
            <h3 class="${titleClass}">${task.title}</h3>
            <p>${task.description || "No description provided"}</p>
            <div class="button-row">
                ${!task.completed ? `
                    <button class="btn-done" onClick="updateTask('${task._id}')">Done</button>
                ` : ''}
                <button class="btn-delete" onClick="deleteTask('${task._id}')">Delete</button>
            </div>
            `;
        container.appendChild(div);
    });
}

async function createTask(){
    const titleInput = document.getElementById('task-title');
    const descriptionInput = document.getElementById('task-desc');

    const newTask = {
        title: titleInput.value,
        description: descriptionInput.value || null,
        completed: false
    };

    if (newTask.title.length < 3){
        alert("Title should contain more than 3 characters.")
        return;
    }

    try {
        const response = await fetch(API_URL + '/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newTask)
        });

        if (response.ok) {
            titleInput.value = "";
            descriptionInput.value = "";
            toggleModal(false);
            loadTasks();
        }
        else {
            console.error("Couldn't save task.");
        }
    } catch (erro) {
        console.error("Error", error);
    }
}

async function updateTask(id){
    await fetch(`${API_URL}/update/${id}`, {method: 'PUT'});
    loadTasks();
}

async function deleteTask(id){
    if(confirm("Confirm task deletion.")){
        await fetch(`${API_URL}/delete/${id}`, {method: 'DELETE'});
        loadTasks();
    }
}

loadTasks();