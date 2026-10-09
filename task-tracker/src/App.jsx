import React, { useState } from "react";

const storageKey = "simple-task-tracker";

// Read saved tasks once when the app starts. Keep unreadable data untouched.
function readTasks() {
  try {
    const tasks = JSON.parse(localStorage.getItem(storageKey) || "[]");
    if (
      !Array.isArray(tasks) ||
      !tasks.every(
        (task) =>
          typeof task.id === "string" &&
          typeof task.title === "string" &&
          typeof task.dueDate === "string" &&
          typeof task.completed === "boolean",
      )
    )
      throw new Error("Invalid tasks");
    return { tasks, error: "" };
  } catch {
    return {
      tasks: [],
      error:
        "Saved tasks could not be read. Browser storage may be unavailable.",
    };
  }
}

export default function App() {
  const [saved] = useState(readTasks);
  const [tasks, setTasks] = useState(saved.tasks);
  const [title, setTitle] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [filter, setFilter] = useState("All");
  const [message, setMessage] = useState(saved.error);

  // Update the screen and save the same list for the next visit.
  function saveTasks(nextTasks) {
    setTasks(nextTasks);
    if (saved.error) {
      setMessage(
        "Tasks are available for this session only. Saved data could not be read.",
      );
      return;
    }
    try {
      localStorage.setItem(storageKey, JSON.stringify(nextTasks));
      setMessage("");
    } catch {
      setMessage(
        "Unable to save. Your changes will last only for this session.",
      );
    }
  }

  function addTask(event) {
    event.preventDefault();
    if (!title.trim()) {
      setMessage("Please enter a task title.");
      return;
    }
    const task = {
      id: crypto.randomUUID(),
      title: title.trim(),
      dueDate: new FormData(event.currentTarget).get("dueDate") || "",
      completed: false,
    };
    saveTasks([...tasks, task]);
    setTitle("");
    setDueDate("");
    setFilter("All");
  }

  function toggleTask(id) {
    const updated = tasks.map((task) => {
      if (task.id === id) return { ...task, completed: !task.completed };
      return task;
    });
    saveTasks(updated);
  }

  function deleteTask(id) {
    saveTasks(tasks.filter((task) => task.id !== id));
  }

  // Filters change only the displayed list, not the saved tasks.
  const visibleTasks = tasks.filter((task) => {
    if (filter === "Pending") return !task.completed;
    if (filter === "Completed") return task.completed;
    return true;
  });
  const completedCount = tasks.filter((task) => task.completed).length;

  return (
    <main>
      <header>
        <p className="eyebrow">A LITTLE MORE ORGANISED</p>
        <h1>
          Task Tracker<span>.</span>
        </h1>
        <p>Add a task. Take your time. Tick it off.</p>
      </header>

      <section className="panel" aria-labelledby="add-heading">
        <h2 id="add-heading">Add a task</h2>
        <form onSubmit={addTask}>
          <label className="title-field">
            Task title
            <input
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              placeholder="What do you need to do?"
              maxLength={120}
              required
            />
          </label>
          <label>
            Due date <span className="optional">(optional)</span>
            <input
              name="dueDate"
              type="date"
              value={dueDate}
              onChange={(event) => setDueDate(event.target.value)}
            />
          </label>
          <button className="add-button" type="submit">
            Add task
          </button>
        </form>
        {message && (
          <p className="message" role="status">
            {message}
          </p>
        )}
      </section>

      <section className="panel" aria-labelledby="tasks-heading">
        <div className="list-heading">
          <h2 id="tasks-heading">Your tasks</h2>
          <p aria-live="polite">
            {completedCount} of {tasks.length} completed
          </p>
        </div>
        <div className="filters" aria-label="Filter tasks">
          {["All", "Pending", "Completed"].map((option) => (
            <button
              key={option}
              className={filter === option ? "selected" : ""}
              aria-pressed={filter === option}
              onClick={() => setFilter(option)}
            >
              {option}
            </button>
          ))}
        </div>

        <ul className="task-list">
          {visibleTasks.map((task) => (
            <li key={task.id}>
              <label className="task-label">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleTask(task.id)}
                />
                <span>
                  <strong className={task.completed ? "completed" : ""}>
                    {task.title}
                  </strong>
                  <small>
                    {task.dueDate ? `Due ${task.dueDate}` : "No due date"}
                  </small>
                </span>
              </label>
              <button
                className="delete-button"
                aria-label={`Delete ${task.title}`}
                onClick={() => deleteTask(task.id)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
        {visibleTasks.length === 0 && (
          <p className="empty">
            {tasks.length === 0
              ? "No tasks yet. Add your first one above."
              : `No ${filter.toLowerCase()} tasks.`}
          </p>
        )}
      </section>
      <footer>Saved in this browser · SWE40006 Task 4.3</footer>
    </main>
  );
}
