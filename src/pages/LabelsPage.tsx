import Box from '@mui/material/Box'
import { dishes, ingredients } from '../data/mock'
import { LabelCard } from '../components/LabelCard'
import { PageHeader } from '../components/PageHeader'

export function LabelsPage() {
  return (
    <Box>
      <PageHeader title="Этикетки блюд" subtitle="Просмотр и печать" />
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, alignItems: 'stretch' }}>
        {dishes.map((dish) => <LabelCard key={dish.id} dish={dish} ingredients={ingredients} />)}
      </Box>
    </Box>
  )
}