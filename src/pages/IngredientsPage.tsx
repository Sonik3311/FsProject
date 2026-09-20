import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import { ingredients } from '../data/mock'
import { IngredientTable } from '../components/IngredientTable'

export function IngredientsPage() {
  return (
    <Box>
      <Typography variant="h5">Справочник ингредиентов</Typography>
      <IngredientTable ingredients={ingredients} />
    </Box>
  )
}