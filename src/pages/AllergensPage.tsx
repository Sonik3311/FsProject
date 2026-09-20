import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import { dishes, ingredients } from '../data/mock'
import { AllergenMatrix } from '../components/AllergenMatrix'

export function AllergensPage() {
  return (
    <Box>
      <Typography variant="h5">Матрица аллергенов</Typography>
      <AllergenMatrix dishes={dishes} ingredients={ingredients} />
    </Box>
  )
}