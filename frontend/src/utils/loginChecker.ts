import UserService from "@/services/userService";

export default async function isLoggedIn(): Promise<boolean> {
    try {
        await UserService.getMe();
        return true;
    } catch (err) {
        return false;
    }
}