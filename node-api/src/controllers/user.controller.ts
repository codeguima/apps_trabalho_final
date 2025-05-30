import { Request, Response } from 'express'
import { UserService } from '../services/user.service'

const userService = new UserService()

export class UserController {
  async create(req: Request, res: Response) {
    const { name, lastname, password, email } = req.body

    try {
      const user = await userService.createUser({
        name,
        lastname,
        email,
        password,
        status: true,
      })
      return res.status(201).json(user)
    } catch (error) {
      return res.status(400).json({ error: 'Erro ao criar usuário' })
    }
  }

  async findAll(req: Request, res: Response) {
    const users = await userService.getUsers()
    return res.json(users)
  }

  async findOne(req: Request, res: Response) {
    const id = Number(req.params.id)
    const user = await userService.findById(id)
    if (!user) return res.status(404).json({ error: 'Usuário não encontrado' })
    return res.json(user)
  }

  async update(req: Request, res: Response) {
    const id = Number(req.params.id)
    try {
      const user = await userService.updateUser(id, req.body)
      return res.json(user)
    } catch (error) {
      return res.status(400).json({ error: 'Erro ao atualizar usuário' })
    }
  }

  async delete(req: Request, res: Response) {
    const id = Number(req.params.id)
    try {
      await userService.deleteUser(id)
      return res.status(204).send()
    } catch (error) {
      return res.status(400).json({ error: 'Erro ao deletar usuário' })
    }
  }
}
