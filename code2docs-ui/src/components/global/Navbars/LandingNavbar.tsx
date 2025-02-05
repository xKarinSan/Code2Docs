import {
    Box,
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

interface Props {
    children: React.ReactNode;
}

const LandingPageLinks = [
    "Home",
    "About Us",
    "Highlights",
    "How We Work",
    "Demo",
    "Contact Us",
];

const HomepageLinks = ["Home", "Codebases", "Documentations", "Account"];

const NavLink = (props: Props) => {
    const { children } = props;
    return (
        <Box
            as="a"
            px={2}
            py={1}
            rounded={"md"}
            _hover={{
                textDecoration: "none",
                bg: useColorModeValue("gray.200", "gray.700"),
            }}
            href={"#"}
        >
            {children}
        </Box>
    );
};

export default function LandingNavbar({ children }: { children: ReactNode }) {
    const { isOpen, onOpen, onClose } = useDisclosure();

    const [links, setLinks] = useState<string[]>([]);

    useEffect(() => {
        setLinks(LandingPageLinks);
    }, []);

    return (
        <>
            <Box
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
                                width={{
                                    base: "200px",
                                    md: "350px",
                                }}
                            />
                        </Box>
                        <HStack
                            as={"nav"}
                            spacing={4}
                            display={{ base: "none", md: "flex" }}
                        >
                            {links.map((link) => (
                                <NavLink key={link}>{link}</NavLink>
                            ))}
                        </HStack>
                    </HStack>
                </Flex>

                {isOpen ? (
                    <Box pb={4} display={{ md: "none" }}>
                        <Stack as={"nav"} spacing={4}>
                            {links.map((link) => (
                                <NavLink key={link}>{link}</NavLink>
                            ))}
                        </Stack>
                    </Box>
                ) : null}
            </Box>

            <Box p={4}>{children}</Box>
        </>
    );
}
