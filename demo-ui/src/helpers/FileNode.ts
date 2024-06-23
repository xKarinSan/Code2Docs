interface FileNode {
    name: string;
    isDirectory: boolean;
    children: FileNode[];
    content?: string;
}

function buildFileTree(
    files: { filename: string; content: string }[]
): FileNode {
    const root: FileNode = { name: "root", isDirectory: true, children: [] };

    files.forEach((file) => {
        const parts = file.filename.split("/");
        let currentNode = root;

        parts.forEach((part, index) => {
            const isLast = index === parts.length - 1;
            let child = currentNode.children.find((c) => c.name === part);

            if (!child) {
                child = {
                    name: part,
                    isDirectory: !isLast,
                    children: [],
                    content: isLast ? file.content : undefined,
                };
                currentNode.children.push(child);
            }

            currentNode = child;
        });
    });

    return root;
}

export { type FileNode, buildFileTree };
