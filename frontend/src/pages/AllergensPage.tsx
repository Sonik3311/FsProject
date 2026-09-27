import Box from '@mui/material/Box'
import { dishes, ingredients } from '../data/mock'
import { AllergenMatrix } from '../components/AllergenMatrix'
import { PageHeader } from '../components/PageHeader'

export function AllergensPage() {
  return (
    <Box>
      <PageHeader title="Матрица аллергенов" subtitle="Аллергены по блюдам" />
      <AllergenMatrix dishes={dishes} ingredients={ingredients} />
    </Box>
  )
}