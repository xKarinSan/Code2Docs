interface FileNode {
    name: string;
    isDirectory: boolean;
    children: FileNode[];
    content?: string;
    path: string; // New property to store the full path
}

function buildFileTree(
    files: { filename: string; content: string }[]
): FileNode {
    const root: FileNode = { name: "root", isDirectory: true, children: [], path: "root" };

    files.forEach((file) => {
        const parts = file.filename.split("/");
        let currentNode = root;
        let currentPath = "root";

        parts.forEach((part, index) => {
            const isLast = index === parts.length - 1;
            currentPath = `${currentPath}/${part}`;
            let child = currentNode.children.find((c) => c.name === part);

            if (!child) {
                child = {
                    name: part,
                    isDirectory: !isLast,
                    children: [],
                    content: isLast ? file.content : undefined,
                    path: currentPath, // Set the full path
                };
                currentNode.children.push(child);
            }

            currentNode = child;
        });
    });

    return root;
}

export { type FileNode, buildFileTree };
