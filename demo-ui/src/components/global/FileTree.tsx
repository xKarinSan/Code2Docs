import { Box, Text, Icon } from "@chakra-ui/react";
import { FileNode } from "../../helpers/FileNode";
import { FaFolder, FaFile } from "react-icons/fa";

interface FileTreeProps {
    node: FileNode;
}

function FileTree({ node }: FileTreeProps) {
    return (
        <Box ml={1}>
            <Box display="flex" alignItems="center">
                <Icon as={node.isDirectory ? FaFolder : FaFile} mr={2} />
                <Text>{node.name}</Text>
            </Box>
            {node.children.map((child, index) => (
                <FileTree key={index} node={child} />
            ))}
        </Box>
    );
}

export { type FileTreeProps, FileTree };
