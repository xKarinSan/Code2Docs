import { Box, Button, Image, Heading, Link, Text } from "@chakra-ui/react";
import { githubAuthURL } from "../../global/constants";
import { useNavigate } from "react-router-dom";
import TransparentLogo from "../../assets/TransparentLogo.png";
import TransparentLogoWithSlogan from "../../assets/TransparentLogoWithSlogan.png";

function AuthContainer({ isLogin }: { isLogin: boolean }) {
    const navigate = useNavigate();
    const authenticateGithubUser = () => {
        window.location.assign(githubAuthURL);
    };

    const togglePage = () => {
        navigate(isLogin ? "/register" : "/login");
    };
    return (
        <Box
            padding="10px"
            margin={"auto"}
            width={{
                base: "100%",
                sm: "80%",
                md: "50%",
                lg: "40%",
            }}
        >
            <Image
                src={TransparentLogoWithSlogan}
                margin={"auto"}
                width={{ base: "250px", md: "450px" }}
            />
            <Heading margin="5px auto" variant={"h3"} textAlign={"center"}>
                {isLogin ? "Welcome Back" : "Registration"}
            </Heading>
            <Text margin="10px auto" textAlign={"center"}>
                {" "}
                {isLogin
                    ? "Do not have an account? Register "
                    : "Aleady have an account? Login "}
                <Link
                    onClick={togglePage}
                    textDecoration={"underline"}
                    fontWeight={"bold"}
                >
                    here
                </Link>
                .
            </Text>
            <Button
                display={"flex"}
                background={"black"}
                color="white"
                margin={"20px auto"}
                width={"fit-content"}
                onClick={authenticateGithubUser}
            >
                {isLogin ? "Login" : "Register"} with Github
            </Button>
        </Box>
    );
}

export default AuthContainer;
