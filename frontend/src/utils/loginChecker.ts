export default function isLoggedIn(): boolean {
    const token = localStorage.getItem("accessToken");
    return Boolean(token);
}