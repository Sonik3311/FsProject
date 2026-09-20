import { useState } from 'react'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import { ingredients, wastage } from '../data/mock'
import { WastageTable } from '../components/WastageTable'
import { WastageForm } from '../components/WastageForm'
import type { WastageEntry } from '../types'

export function WastagePage() {
  const [entries, setEntries] = useState(wastage)

  const handleSubmit = (entry: Omit<WastageEntry, 'id' | 'date'>) => {
    const next: WastageEntry = {
      ...entry,
      id: entries.length ? Math.max(...entries.map((e) => e.id)) + 1 : 1,
      date: new Date().toISOString().slice(0, 10),
    }
    setEntries([...entries, next])
  }

  return (
    <Box>
      <Typography variant="h5">Журнал списаний</Typography>
      <Typography variant="subtitle1">Новое списание</Typography>
      <WastageForm ingredients={ingredients} onSubmit={handleSubmit} />
      <Divider sx={{ my: 3 }} />
      <WastageTable entries={entries} ingredients={ingredients} />
    </Box>
  )
}