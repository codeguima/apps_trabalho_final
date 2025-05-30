import dotenv from 'dotenv'

import { PrismaClient, User } from '@prisma/client'
import bcrypt from 'bcryptjs'
dotenv.config()

const prisma = new PrismaClient()

async function main(): Promise<void> {
  const enviroment = process.env.NODE_ENV
  console.log('NODE_ENV', enviroment)

  await createUsers()
}

async function createUsers(): Promise<User> {
  const hashedPassword = await bcrypt.hash('systemapps', 10)

  const admin = await prisma.user.upsert({
    where: {
      email: 'kemuel@gmail.com',
    },
    create: {
      name: 'Kemuel',
      lastname: 'Teste',
      email: 'kemuel@gmail.com',
      password: hashedPassword,
      status: true,
    },
    update: {},
  })

  await prisma.user.upsert({
    where: {
      email: 'lukas@gmail.com',
    },
    create: {
      name: 'Lukas',
      lastname: 'Teste',
      email: 'lukas@gmail.com',
      password: hashedPassword,
      status: true,
    },
    update: {},
  })

  await prisma.user.upsert({
    where: {
      email: 'jhonny@gmail.com',
    },
    create: {
      name: 'Jhonny',
      lastname: 'Teste',
      email: 'jhonny@gmail.com',
      password: hashedPassword,
      status: true,
    },
    update: {},
  })

  await prisma.user.upsert({
    where: {
      email: 'vinicius@gmail.com',
    },
    create: {
      name: 'Vinicius',
      lastname: 'Teste',
      email: 'vinicius@gmail.com',
      password: hashedPassword,
      status: true,
    },
    update: {},
  })

  return admin
}

main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch((e) => {
    console.error(e)
    process.exit(1)
  })
