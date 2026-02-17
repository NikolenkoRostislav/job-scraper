export type UserBase = {
    id: number
    username: string
    is_admin: boolean
}

export type UserCreate = {
    email: string
    username: string
    password: string
}
