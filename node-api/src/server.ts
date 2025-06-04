import 'dotenv/config'
import express from 'express'
import { router } from './routes'
import { prisma } from './database/prisma-client'

const app = express()
const port = process.env.PORT || 3000

app.use(express.json())
app.use(router)

app.get('/', (req, res) => {
  res.send('Node-API is running')
})

async function startServer() {
  try {
    // Espera 5 segundos (5000ms) antes de tentar conectar (ajuste o tempo se quiser)
    await new Promise(resolve => setTimeout(resolve, 5000))

    // Conecta com o banco usando prisma
    await prisma.$connect()
    console.log('Conectado ao banco de dados com sucesso!')

    // Só inicia o servidor depois da conexão
    app.listen(port, () => {
      console.log(`Servidor rodando na porta ${port}`)
    })
  } catch (error) {
    console.error('Erro ao conectar ao banco:', error)
  }
}

startServer()