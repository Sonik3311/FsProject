import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import { dishes, ingredients } from '../data/mock'
import { LabelCard } from '../components/LabelCard'

export function LabelsPage() {
  return (
    <Box>
      <Typography variant="h5">Этикетки блюд</Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
        {dishes.map((dish) => <LabelCard key={dish.id} dish={dish} ingredients={ingredients} />)}
      </Box>
    </Box>
  )
}