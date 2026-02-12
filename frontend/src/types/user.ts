export type UserBase = {
  id: number
  username: string
}

export type UserCreate = {
  email: string
  username: string
  password: string
}
