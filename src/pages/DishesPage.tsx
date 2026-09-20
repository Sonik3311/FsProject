import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import { dishes } from '../data/mock'
import { DishCard } from '../components/DishCard'

export function DishesPage() {
  return (
    <Box>
      <Typography variant="h5">Меню</Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
        {dishes.map((dish) => <DishCard key={dish.id} dish={dish} />)}
      </Box>
    </Box>
  )
}