import Box from '@mui/material/Box'
import { ingredients } from '../data/mock'
import { IngredientTable } from '../components/IngredientTable'
import { PageHeader } from '../components/PageHeader'

export function IngredientsPage() {
  return (
    <Box>
      <PageHeader title="Справочник ингредиентов" subtitle="Цены и аллергены" />
      <IngredientTable ingredients={ingredients} />
    </Box>
  )
}