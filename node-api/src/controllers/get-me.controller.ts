import { Request, Response } from 'express'
import { UserService } from '../services/user.service'

const userService = new UserService()

export class GetMeController {
  async handle(req: Request, res: Response) {
    const { id } = req.user

    const user = await userService.findById(id)

    if (!user) return res.status(404).json({ error: 'Usuário não encontrado' })

    return res.json(user)
  }
}
