let items = [];
let statusMessage = document.getElementById('statusMessage');

window.onload = () => {
    fetchItems();
};

async function fetchItems() {
    statusMessage.textContent = "Loading items...";
    try {
        const response = await fetch('http://localhost:50010/api/items');
        if (!response.ok) {
            throw new Error(response.status === 404 ? "Items not found." : "Network response was not ok");
        }
        items = await response.json();
        renderItems();
    } catch (error) {
        handleError(error);
    } finally {
        statusMessage.textContent = "";
    }
}

function renderItems() {
    const itemsList = document.getElementById('itemsList');
    itemsList.innerHTML = '';

    const fragment = document.createDocumentFragment();

    items.forEach((item, index) => {
        const row = document.createElement('tr');

        const nameCell = document.createElement('td');
        nameCell.textContent = item.name;

        const actionsCell = document.createElement('td');

        const editBtn = document.createElement('button');
        editBtn.innerHTML = '<i class="fas fa-edit"></i> Edit';
        editBtn.className = 'btn';
        editBtn.setAttribute('aria-label', `Edit item: ${item.name}`);
        editBtn.onclick = () => editItem(index);

        const deleteBtn = document.createElement('button');
        deleteBtn.innerHTML = '<i class="fas fa-trash"></i> Delete';
        deleteBtn.className = 'btn btn-danger';
        deleteBtn.setAttribute('aria-label', `Delete item: ${item.name}`);
        deleteBtn.onclick = () => deleteItem(index);

        actionsCell.appendChild(editBtn);
        actionsCell.appendChild(deleteBtn);
        row.appendChild(nameCell);
        row.appendChild(actionsCell);
        fragment.appendChild(row);
    });

    itemsList.appendChild(fragment);
}

document.getElementById('crudForm').onsubmit = async function (event) {
    event.preventDefault();
    const itemName = document.getElementById('itemName').value.trim();
    const itemId = document.getElementById('itemId').value;

    if (itemName.length === 0) {
        statusMessage.textContent = "Item name cannot be empty.";
        return;
    }

    try {
        if (itemId) {
            statusMessage.textContent = "Updating the item...";
            const response = await fetch(`http://localhost:50010/api/items/${itemId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: itemName })
            });

            if (!response.ok) throw new Error("Failed to update item");
            items[itemId].name = itemName;
            renderItems();
            resetForm();
            statusMessage.textContent = "Item updated successfully!";
        } else {
            statusMessage.textContent = "Creating a new item...";
            const response = await fetch('http://localhost:50010/api/items', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: itemName })
            });

            if (!response.ok) throw new Error("Failed to create item");
            const newItem = await response.json();
            items.push(newItem);
            renderItems();
            resetForm();
            statusMessage.textContent = "Item created successfully!";
        }
    } catch (error) {
        handleError(error);
    }
};

function deleteItem(index) {
    if (confirm(`Are you sure you want to delete "${items[index].name}"?`)) {
        statusMessage.textContent = "Deleting the item...";
        fetch(`http://localhost:50010/api/items/${items[index].id}`, { method: 'DELETE' })
            .then(response => {
                if (!response.ok) throw new Error("Failed to delete item");
                items.splice(index, 1);
                renderItems();
                statusMessage.textContent = "Item deleted successfully!";
            })
            .catch(handleError);
    }
}

function editItem(index) {
    const item = items[index];
    document.getElementById('itemName').value = item.name;
    document.getElementById('itemId').value = item.id;
}

function resetForm() {
    document.getElementById('itemName').value = '';
    document.getElementById('itemId').value = '';
}

function handleError(error) {
    console.error("Error:", error);
    statusMessage.textContent = `An error occurred: ${error.message || "Unknown error."}`;
}
