import { Request, Response } from 'express'
import bcrypt from 'bcryptjs'
import jwt from 'jsonwebtoken'
import { UserService } from '../services/user.service'

const userService = new UserService()

export class AuthController {
  async login(req: Request, res: Response) {
    const { email, password } = req.body

    const user = await userService.findByEmail(email)
    if (!user) return res.status(401).json({ error: 'Credenciais inválidas' })

    const passwordMatch = await bcrypt.compare(password, user.password)
    if (!passwordMatch)
      return res.status(401).json({ error: 'Credenciais inválidas' })

    const token = jwt.sign(
      { userId: user.id, email: user.email },
      process.env.JWT_SECRET as string,
      { expiresIn: '1d' },
    )

    return res.json({ token })
  }
}
