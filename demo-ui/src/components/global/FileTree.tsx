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
    setReadFile: (file: FileNode | null) => void;
    setReadDirectory: (file: FileNode | null) => void;
    setReadFilePath: (filePath: string) => void;
    currentReadFilePath: string;
    currentReadDirectory: FileNode | null;
}

function FileTree({
    node,
    setReadFile,
    setReadDirectory,
    setReadFilePath,
    currentReadFilePath,
    currentReadDirectory,
}: FileTreeProps) {
    const [isOpen, setIsOpen] = useState(true);

    const selectFile = (currentNode: FileNode) => {
        if (currentNode.isDirectory) {
            if (currentReadDirectory != currentNode) {
                setReadDirectory(currentNode);
            } else {
                setReadDirectory(null);
            }
        } else {
            if (currentReadFilePath != currentNode.path) {
                setReadFilePath(currentNode.path);
                setReadFile(currentNode);
            } else {
                setReadFile(null);
                setReadFilePath("");
            }
        }
    };

    const toggleOpen = (e: React.MouseEvent) => {
        e.stopPropagation();
        setIsOpen(!isOpen);
    };

    return (
        <Box ml={1} className="fileTree">
            <Box
                display="flex"
                alignItems="center"
                cursor="pointer"
                borderRadius="5px"
                padding="5px"
                margin="2px"
                background={
                    currentReadDirectory == node ||
                    currentReadFilePath == node.path
                        ? "#4E35E5"
                        : ""
                }
                color={
                    currentReadDirectory == node ||
                    currentReadFilePath == node.path
                        ? "white"
                        : "black"
                }
                onClick={() => selectFile(node)}
            >
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
                <Text whiteSpace={"nowrap"} overflow="scroll">
                    {node.name}
                </Text>
            </Box>
            <Collapse in={isOpen}>
                <Box ml={4} overflow={"scroll"}>
                    {node.children.map((child, index) => (
                        <FileTree
                            key={index}
                            node={child}
                            setReadFile={setReadFile}
                            setReadFilePath={setReadFilePath}
                            setReadDirectory={setReadDirectory}
                            currentReadFilePath={currentReadFilePath}
                            currentReadDirectory={currentReadDirectory}
                        />
                    ))}
                </Box>
            </Collapse>
        </Box>
    );
}

export { type FileTreeProps, FileTree };
