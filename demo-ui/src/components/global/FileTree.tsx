import { Box, Text, Icon } from "@chakra-ui/react";
import { FileNode } from "../../helpers/FileNode";
import { FaFolder, FaFile } from "react-icons/fa";

interface FileTreeProps {
    node: FileNode;
    setReadFile: (file: FileNode) => void;
    setReadDirectory: (file: FileNode) => void;
}

function FileTree({ node, setReadFile, setReadDirectory }: FileTreeProps) {
    const selectFile = (currentNode: FileNode) => {
        if (node.children.length > 0) {
            setReadDirectory(currentNode);
            return;
        }
        setReadFile(currentNode);
    };
    return (
        <Box ml={1} className="fileTree" margin="10px">
            <Box
                display="flex"
                alignItems="center"
                onClick={() => {
                    selectFile(node);
                }}
            >
                <Icon as={node.isDirectory ? FaFolder : FaFile} mr={2} />
                <Text>{node.name}</Text>
            </Box>
            {node.children.map((child, index) => (
                <FileTree
                    key={index}
                    node={child}
                    setReadFile={setReadFile}
                    setReadDirectory={setReadDirectory}
                />
            ))}
        </Box>
    );
}

export { type FileTreeProps, FileTree };
