import { Box, Text, Icon } from "@chakra-ui/react";
import { FileNode } from "../../helpers/FileNode";
import { FaFolder, FaFile } from "react-icons/fa";

interface FileTreeProps {
    node: FileNode;
    setReadFile: (file: any) => void;
}

function FileTree({ node, setReadFile }: FileTreeProps) {
    const selectFile = () => {
        if (!node.isDirectory) {
            setReadFile(node);
        }
    };
    return (
        <Box ml={1} onClick={selectFile} className="fileTree">
            <Box display="flex" alignItems="center">
                <Icon as={node.isDirectory ? FaFolder : FaFile} mr={2} />
                <Text>{node.name}</Text>
            </Box>
            {node.children.map((child, index) => (
                <FileTree key={index} node={child} setReadFile={setReadFile} />
            ))}
        </Box>
    );
}

export { type FileTreeProps, FileTree };
