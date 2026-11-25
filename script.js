
POLLING_RATE_MS = 1_000

async function updateResources() {
    const message = document.getElementById("message");

    try {
        const response = await fetch("/resources");
        if (!response.ok) {
            throw new Error(`Request returned status ${response.status}.`);
        }

        const result = await response.json();
        const tbody = document.getElementById("resources");

        const rows = result.data
            .map(resource => {
                const row = document.createElement("tr");

                for (const value of [
                    // Name is optional, ID is not
                    // ID is in form x/y/z -> we want only the end (z in this example)
                    resource.name ?? resource.id.substring(resource.id.lastIndexOf("/") + 1),
                    
                    resource.type,

                    // Only display node for non-node resources (VMs/containers)
                    resource.type == "node" ? "-" : resource.node,

                    resource.status,
                    resource.vmid,
                    bytesToGigabytes(resource.mem),

                    // CPU utilization as a percentage of max
                    resource.maxcpu,
                    resource.cpu != null ? (resource.cpu * 100).toFixed(2) + "%" : "-"
                ]) {
                    const cell = document.createElement("td");
                    cell.textContent = value ?? "-";
                    row.appendChild(cell);
                }

                const statusCell = row.cells[3];
                statusCell.className = ["running", "online"].includes(resource.status) ? "online" : "offline";

                return row;
            });
        tbody.replaceChildren(...rows);

        message.textContent = `Updated ${new Date().toLocaleTimeString()}`;
    } catch (error) {
        message.textContent = `Update failed: ${error.message}`;
    } finally {
        // Update tables every POLLING_RATE_MS
        setTimeout(updateResources, POLLING_RATE_MS);
    }
}
updateResources();

function bytesToGigabytes(bits) {
    if (bits == null) {
        return "-";
    }

    BYTES_PER_GIGABYTE = 1024 ** 3;
    return (bits / BYTES_PER_GIGABYTE).toFixed(2) + " GB";
}