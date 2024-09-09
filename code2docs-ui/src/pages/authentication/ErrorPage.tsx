import { Card } from "@chakra-ui/react";

function ErrorPage() {
    return (
        <div>
            <Card padding={10} margin="5px auto" width="fit-content">
                An error occurred, please try again later.
            </Card>
        </div>
    );
}

export default ErrorPage;
