import redis from '@/cache/redis'
import { prisma } from '../database/prisma-client'
import { User } from '@prisma/client'
import bcrypt from 'bcryptjs'

export class UserService {
  private usersCacheKey = 'users:all'

  async createUser({
    name,
    lastname,
    email,
    password,
    status,
  }: Omit<User, 'id'>) {
    const hashedPassword = await bcrypt.hash(password, 10)

    const newUser = await prisma.user.create({
      data: {
        name,
        lastname,
        email,
        password: hashedPassword,
        status,
      },
    })

    // Invalida o cache
    await redis.del(this.usersCacheKey)
    await redis.del(`user:email:${email}`)

    return newUser
  }

  async findById(id: number) {
    const cacheKey = `user:id:${id}`
    const cached = await redis.get(cacheKey)
    if (cached) return JSON.parse(cached)

    const user = await prisma.user.findUnique({ where: { id } })

    if (user) await redis.set(cacheKey, JSON.stringify(user), 'EX', 60 * 60) // 1h

    return user
  }

  async findByEmail(email: string) {
    const cacheKey = `user:email:${email}`
    const cached = await redis.get(cacheKey)
    if (cached) return JSON.parse(cached)

    const user = await prisma.user.findUnique({ where: { email } })

    if (user) await redis.set(cacheKey, JSON.stringify(user), 'EX', 60 * 60) // 1h

    return user
  }

  async getUsers() {
    const cached = await redis.get(this.usersCacheKey)
    if (cached) return JSON.parse(cached)

    const users = await prisma.user.findMany()
    await redis.set(this.usersCacheKey, JSON.stringify(users), 'EX', 60 * 60) // 1h

    return users
  }

  async updateUser(id: number, data: Partial<User>) {
    const updatedUser = await prisma.user.update({ where: { id }, data })

    // Invalida os caches
    await redis.del(`user:id:${id}`)
    if (data.email) await redis.del(`user:email:${data.email}`)
    await redis.del(this.usersCacheKey)

    return updatedUser
  }

  async deleteUser(id: number) {
    const deletedUser = await prisma.user.delete({ where: { id } })

    await redis.del(`user:id:${id}`)
    await redis.del(`user:email:${deletedUser.email}`)
    await redis.del(this.usersCacheKey)

    return deletedUser
  }
}
