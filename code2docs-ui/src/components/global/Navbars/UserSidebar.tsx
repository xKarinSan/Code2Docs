import { ReactNode } from "react";
import TransparentLogo from "../../../assets/TransparentLogo.png";

import {
    IconButton,
    Box,
    CloseButton,
    Flex,
    Icon,
    Image,
    useColorModeValue,
    Drawer,
    DrawerContent,
    useDisclosure,
    BoxProps,
    FlexProps,
} from "@chakra-ui/react";
import {
    FiCode,
    FiHome,
    FiFileText,
    FiUser,
    FiLogOut,
    FiMenu,
} from "react-icons/fi";
import { IconType } from "react-icons";
import { Link } from "react-router-dom";

interface LinkItemProps {
    name: string;
    route: string;
    icon: IconType;
}

const LinkItems: Array<LinkItemProps> = [
    { name: "Home", route: "/home", icon: FiHome },
    { name: "Codebases", route: "/codebases", icon: FiCode },
    { name: "Documentations", route: "/documentations", icon: FiFileText },
    { name: "Account", route: "/profile", icon: FiUser },
    { name: "Logout", route: "/logout", icon: FiLogOut },
];

export default function UserSidebar({ children }: { children: ReactNode }) {
    const { isOpen, onOpen, onClose } = useDisclosure();
    return (
        <Box minH="100vh" bg={useColorModeValue("gray.100", "gray.900")}>
            <SidebarContent
                onClose={onClose}
                display={{ base: "none", md: "block" }}
            />
            <Drawer
                isOpen={isOpen}
                placement="left"
                onClose={onClose}
                returnFocusOnClose={false}
                onOverlayClick={onClose}
                size="full"
            >
                <DrawerContent>
                    <SidebarContent onClose={onClose} />
                </DrawerContent>
            </Drawer>
            {/* Mobile navigation */}
            <MobileNav display={{ base: "flex", md: "none" }} onOpen={onOpen} />
            <Box ml={{ base: 0, md: 60 }} p="4">
                {children}
            </Box>
        </Box>
    );
}

interface SidebarProps extends BoxProps {
    onClose: () => void;
}

const SidebarContent = ({ onClose, ...rest }: SidebarProps) => {
    return (
        <Box
            bg={useColorModeValue("white", "gray.900")}
            borderRight="1px"
            borderRightColor={useColorModeValue("gray.200", "gray.700")}
            w={{ base: "full", md: 60 }}
            pos="fixed"
            h="full"
            {...rest}
        >
            <Flex
                h="20"
                alignItems="center"
                mx={{ base: "8", md: "0" }}
                justifyContent="space-between"
            >
                <Image
                    src={TransparentLogo}
                    margin={"auto"}
                    width={{ base: "100px", md: "150px" }}
                />
                <CloseButton
                    display={{ base: "flex", md: "none" }}
                    onClick={onClose}
                />
            </Flex>
            {LinkItems.map((link) => (
                <NavItem key={link.name} route={link.route} icon={link.icon}>
                    {link.name}
                </NavItem>
            ))}
        </Box>
    );
};

interface NavItemProps extends FlexProps {
    icon: IconType;
    route: string;
    children: ReactNode;
}

const NavItem = ({ icon, route, children, ...rest }: NavItemProps) => {
    return (
        <Link to={route}>
            <Box
                as="a"
                href="#"
                style={{ textDecoration: "none" }}
                _focus={{ boxShadow: "none" }}
            >
                <Flex
                    align="center"
                    p="4"
                    mx="4"
                    borderRadius="lg"
                    role="group"
                    cursor="pointer"
                    _hover={{
                        bg: "black",
                        color: "white",
                    }}
                    {...rest}
                >
                    {icon && (
                        <Icon
                            mr="4"
                            fontSize="16"
                            _groupHover={{
                                color: "white",
                            }}
                            as={icon}
                        />
                    )}
                    {children}
                </Flex>
            </Box>
        </Link>
    );
};

interface MobileProps extends FlexProps {
    onOpen: () => void;
}

const MobileNav = ({ onOpen, ...rest }: MobileProps) => {
    return (
        <Flex
            ml={{ base: 0, md: 60 }}
            px={{ base: 4, md: 24 }}
            height="20"
            alignItems="center"
            bg={useColorModeValue("white", "gray.900")}
            borderBottomWidth="1px"
            borderBottomColor={useColorModeValue("gray.200", "gray.700")}
            justifyContent="flex-start"
            {...rest}
        >
            <IconButton
                variant="outline"
                onClick={onOpen}
                aria-label="open menu"
                icon={<FiMenu />}
            />
            <Image
                src={TransparentLogo}
                margin={"auto"}
                width={{ base: "100px", md: "150px" }}
            />
        </Flex>
    );
};
