import Box from '@mui/material/Box'
import { dishes, ingredients } from '../data/mock'
import { DishCard } from '../components/DishCard'
import { PageHeader } from '../components/PageHeader'

export function DishesPage() {
  return (
    <Box>
      <PageHeader title="Меню" subtitle="Блюда и их себестоимость" />
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, alignItems: 'stretch' }}>
        {dishes.map((dish) => (
          <DishCard key={dish.id} dish={dish} ingredients={ingredients} />
        ))}
      </Box>
    </Box>
  )
}