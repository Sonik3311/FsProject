import { useState } from 'react'
import Box from '@mui/material/Box'
import TextField from '@mui/material/TextField'
import MenuItem from '@mui/material/MenuItem'
import Button from '@mui/material/Button'
import type { Ingredient, WastageEntry } from '../types'

interface WastageFormProps {
  ingredients: Ingredient[]
  onSubmit: (entry: Omit<WastageEntry, 'id' | 'date'>) => void
}

export function WastageForm({ ingredients, onSubmit }: WastageFormProps) {
  const [ingredientId, setIngredientId] = useState<number | ''>('')
  const [qty, setQty] = useState('')
  const [reason, setReason] = useState('')

  const handleSubmit = () => {
    if (ingredientId === '' || qty === '') return
    const ing = ingredients.find((i) => i.id === ingredientId)
    if (!ing) return
    onSubmit({ ingredientId, qty: Number(qty), unit: ing.unit, reason })
    setIngredientId('')
    setQty('')
    setReason('')
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, width: 320 }}>
      <TextField select label="Ингредиент" value={ingredientId} onChange={(e) => setIngredientId(Number(e.target.value))}>
        {ingredients.map((i) => (
          <MenuItem key={i.id} value={i.id}>
            {i.name}
          </MenuItem>
        ))}
      </TextField>
      <TextField label="Количество" type="number" value={qty} onChange={(e) => setQty(e.target.value)} />
      <TextField label="Причина" value={reason} onChange={(e) => setReason(e.target.value)} />
      <Button variant="contained" onClick={handleSubmit}>
        Записать списание
      </Button>
    </Box>
  )
}