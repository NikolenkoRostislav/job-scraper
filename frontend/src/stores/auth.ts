import { ref } from 'vue'
import { defineStore } from 'pinia'
import UserService from "@/services/userService"

const useAuthStore = defineStore('auth', () => {
    const loggedIn = ref(false)
    const ready = ref(false)

    const checkAuth = async () => {
        try {
            await UserService.getMe()
            loggedIn.value = true
        } catch {
            loggedIn.value = false
        } finally {
            ready.value = true
        }
    }

    const setLoggedIn = (value: boolean) => {
        loggedIn.value = value
    }

    return { loggedIn, ready, checkAuth, setLoggedIn }
})

export default useAuthStore
