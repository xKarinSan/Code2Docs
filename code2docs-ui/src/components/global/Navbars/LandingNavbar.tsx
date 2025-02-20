import {
    Box,
    Button,
    Flex,
    HStack,
    IconButton,
    useDisclosure,
    useColorModeValue,
    Image,
    Stack,
} from "@chakra-ui/react";
import { HamburgerIcon, CloseIcon } from "@chakra-ui/icons";
import { ReactNode, useEffect, useState } from "react";

import TransparentLogo from "../../../assets/TransparentLogo.png";
import { Link, useNavigate } from "react-router-dom";

type NavigationLink = {
    label: string;
    href: string;
};

const LandingPageLinks: NavigationLink[] = [
    {
        label: "Home",
        href: "#home",
    },
    {
        label: "Highlights",
        href: "#highlights",
    },
    {
        label: "How We Work",
        href: "#howwework",
    },
    {
        label: "Demo",
        href: "#demo",
    },
    {
        label: "Contact Us",
        href: "#contactus",
    },
];

const NavLink = ({ label, href }: NavigationLink) => {
    const navigate = useNavigate();
    const handleClick = (
        event: React.MouseEvent<HTMLAnchorElement, MouseEvent>
    ) => {
        event.preventDefault(); // Prevent default anchor behavior
        navigate("/");
        const targetElement = document.getElementById(href.replace("#", "")); // Get the element by ID
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: "smooth" });
        }
    };
    return (
        <Box
            as="a"
            px={2}
            py={1}
            rounded="md"
            _hover={{
                textDecoration: "none",
                bg: useColorModeValue("gray.200", "gray.700"),
            }}
            href={href}
            onClick={handleClick}
        >
            {label}
            {/* <Link to={""}>{label}</Link> */}
        </Box>
    );
};

export default function LandingNavbar({ children }: { children: ReactNode }) {
    const { isOpen, onOpen, onClose } = useDisclosure();
    const navigate = useNavigate();

    const [links, setLinks] = useState<NavigationLink[]>([]);

    const goToLogin = () => {
        navigate("/login");
    };

    useEffect(() => {
        setLinks(LandingPageLinks);
    }, []);

    return (
        <>
            <Box
                position={"sticky"}
                bg={"white"}
                px={4}
                boxShadow={"0px 1px 3px rgba(0, 0, 0, 0.25)"}
            >
                <Flex
                    h={16}
                    alignItems={"center"}
                    justifyContent={"space-between"}
                >
                    <IconButton
                        size={"md"}
                        icon={isOpen ? <CloseIcon /> : <HamburgerIcon />}
                        aria-label={"Open Menu"}
                        display={{ md: "none" }}
                        onClick={isOpen ? onClose : onOpen}
                    />
                    <HStack spacing={8} alignItems={"center"}>
                        <Box>
                            <Image
                                src={TransparentLogo}
                                margin={"auto"}
                                width={{ base: "80px", md: "100px" }}
                            />
                        </Box>
                        <HStack
                            as={"nav"}
                            spacing={4}
                            display={{ base: "none", md: "flex" }}
                        >
                            {links.map((link: NavigationLink) => (
                                <NavLink label={link.label} href={link.href} />
                            ))}
                            <Button
                                background={"black"}
                                color="white"
                                onClick={() => {
                                    goToLogin();
                                }}
                            >
                                Login
                            </Button>
                        </HStack>
                    </HStack>
                </Flex>

                {isOpen ? (
                    <Box pb={4} display={{ md: "none" }}>
                        <Stack as={"nav"} spacing={4}>
                            {links.map((link: NavigationLink) => (
                                <NavLink label={link.label} href={link.href} />
                            ))}
                            <Button
                                background={"black"}
                                color="white"
                                onClick={() => {
                                    goToLogin();
                                }}
                            >
                                Login
                            </Button>
                        </Stack>
                    </Box>
                ) : null}
            </Box>
            <Box>{children}</Box>
        </>
    );
}
