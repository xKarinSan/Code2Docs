import React, { useState } from "react";
import { Box, Icon, Collapse, Text } from "@chakra-ui/react";
import { FileNode } from "../../helpers/FileNode";
import {
    FaFolder,
    FaFolderOpen,
    FaFile,
    FaChevronRight,
    FaChevronDown,
} from "react-icons/fa";

interface FileTreeProps {
    node: FileNode;
    setReadFile: (file: FileNode) => void;
    setReadDirectory: (file: FileNode) => void;
    setReadFilePath: (filePath: string) => void;
}

function FileTree({
    node,
    setReadFile,
    setReadDirectory,
    setReadFilePath,
}: FileTreeProps) {
    const [isOpen, setIsOpen] = useState(true);

    const selectFile = (currentNode: FileNode) => {
        if (currentNode.isDirectory) {
            setReadDirectory(currentNode);
        } else {
            setReadFile(currentNode);
            setReadFilePath(currentNode.path);
        }
    };

    const toggleOpen = (e: React.MouseEvent) => {
        e.stopPropagation();
        setIsOpen(!isOpen);
    };

    return (
        <Box ml={1} className="fileTree">
            <Box display="flex" alignItems="center" cursor="pointer">
                {node.isDirectory && (
                    <Icon
                        as={isOpen ? FaChevronDown : FaChevronRight}
                        mr={2}
                        onClick={toggleOpen}
                    />
                )}
                <Icon
                    as={
                        node.isDirectory
                            ? isOpen
                                ? FaFolderOpen
                                : FaFolder
                            : FaFile
                    }
                    mr={2}
                />
                <Text whiteSpace={"nowrap"} onClick={() => selectFile(node)}>
                    {node.name}
                </Text>
            </Box>
            <Collapse in={isOpen}>
                <Box ml={4} width="100%" overflow={"scroll"}>
                    {node.children.map((child, index) => (
                        <FileTree
                            key={index}
                            node={child}
                            setReadFile={setReadFile}
                            setReadFilePath={setReadFilePath}
                            setReadDirectory={setReadDirectory}
                        />
                    ))}
                </Box>
            </Collapse>
        </Box>
    );
}

export { type FileTreeProps, FileTree };
