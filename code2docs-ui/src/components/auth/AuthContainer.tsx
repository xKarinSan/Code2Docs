import { Button, Card, Heading, Link, Text } from "@chakra-ui/react";
import { githubAuthURL } from "../../global/constants";
import { useNavigate } from "react-router-dom";
function AuthContainer({ isLogin }: { isLogin: boolean }) {
    const navigate = useNavigate();
    const authenticateGithubUser = () => {
        window.location.assign(githubAuthURL);
    };

    const togglePage = () => {
        navigate(isLogin ? "/register" : "/login");
    };
    return (
        <Card
            padding="10px"
            margin={"auto"}
            width={{
                base: "100%",
                sm: "80%",
                md: "50%",
                lg: "40%",
            }}
        >
            <Heading margin="5px auto" variant={"h3"}>
                {isLogin ? "Login" : "Registration"}
            </Heading>
            <Button
                background={"black"}
                color="white"
                margin={"20px auto"}
                width={"fit-content"}
                onClick={authenticateGithubUser}
            >
                {isLogin ? "Login" : "Register"} with Github
            </Button>
            <Text margin="10px auto">
                {" "}
                {isLogin
                    ? "Do not have an account? Register "
                    : "Aleady have an account? Login "}
                <Link color="blue" onClick={togglePage}>
                    here
                </Link>
                .
            </Text>
        </Card>
    );
}

export default AuthContainer;
