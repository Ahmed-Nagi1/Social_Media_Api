export default function getAuthToken() {
    const token = localStorage.getItem("authToken");
    return token;
}